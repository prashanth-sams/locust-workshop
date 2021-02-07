from locust import HttpUser, between, task, events, SequentialTaskSet
import json

# locust -f src/test/http/exit_deadlock.py -u 1 -r 1 --headless --logfile logs/output.log --loglevel DEBUG --only-summary


class ExitDeadlock(SequentialTaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.session_id = ""
    
    @task
    def login(self):
        with self.client.post(
            "/login/index.php",
            data=json.dumps({ "username": "psamuel", "password": "virus@2020", "anchor": "" }),
            headers={"Content-Type": "application/json", "Origin": "https://moodle.uni-due.de", "Referer": "https://moodle.uni-due.de/login/index.php"},
            name="Login Moodle",
            catch_response=True
        ) as response:
            if response.status_code == 201:
                self.session_id = response.cookies['MoodleSession']
                response.success()
            else:
                response.failure("API failure")
                self.parent.environment.runner.quit()


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

    tasks = [ExitDeadlock]