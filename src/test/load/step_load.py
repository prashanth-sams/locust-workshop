from locust import HttpUser, between, task, SequentialTaskSet, LoadTestShape, constant
import json, csv, random
from src.data.store import credentials
from src.utilities.csvreader import CSVReader
import math
import time

# locust -f src/test/load/step_load.py


data = CSVReader('./src/data/store.csv').read_path()

class PerformTask(SequentialTaskSet):
    def on_start(self):
        self.username = random.choice(data)['Username']
        self.password = random.choice(data)['Password']
        self.session_id = ""
    
    @task
    def login(self):
        with self.client.post(
            "/login/index.php",
            data=json.dumps({ "username": self.username, "password": self.password, "anchor": "" }),
            headers={"Content-Type": "application/json", "Origin": "https://moodle.uni-due.de", "Referer": "https://moodle.uni-due.de/login/index.php"},
            name="Login Moodle",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                self.session_id = response.cookies['MoodleSession']
                response.success()
            else:
                print(response.status_code)

    @task
    def nextstep(self):
        print(self.session_id)
        # self.client.post("", data=json.dumps({}), cookies={"PHPSESSID": self.session_id})
    
    @task
    def stop(self):
        self.interrupt()


class LoadUser(HttpUser):
    # wait_time = constant(0.5)
    wait_time = between(1, 3)
    host = "https://moodle.uni-due.de"

    tasks = [PerformTask]

class StepLoadShape(LoadTestShape):
    """
    A step load shape
    Keyword arguments:
        step_time -- Time between steps
        step_load -- User increase amount at each step
        spawn_rate -- Users to stop/start per second at every step
        time_limit -- Time limit in seconds
    """

    step_time = 30
    step_load = 10
    spawn_rate = 10
    time_limit = 600

    def tick(self):
        run_time = self.get_run_time()

        if run_time > self.time_limit:
            return None

        current_step = math.floor(run_time / self.step_time) + 1
        return (current_step * self.step_load, self.spawn_rate)