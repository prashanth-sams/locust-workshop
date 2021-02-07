from locust import HttpUser, between, task, SequentialTaskSet
import json

# locust -f src/test/store/random.py  -u 4 -r 1 --logfile logs/output.log --loglevel DEBUG --only-summary --headless


credentials = [
    ("prashanthsams", "covid@2020"),
    ("psamuel", "virus@2020")
]

class PerformTask(SequentialTaskSet):
    def on_start(self):
        self.username = ""
        self.password = ""
        self.session_id = ""

        if(len(credentials) > 0):
            self.username, self.password = credentials.pop()
            credentials.insert(0, (self.username, self.password))
    
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
                response.status_code

    @task
    def nextstep(self):
        print(self.session_id)
        # self.client.post("", data=json.dumps({}), cookies={"PHPSESSID": self.session_id})
    
    @task
    def stop(self):
        self.interrupt()

class LoadUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://moodle.uni-due.de"

    tasks = [PerformTask]