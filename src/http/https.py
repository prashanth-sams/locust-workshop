from locust import HttpUser, between, task, SequentialTaskSet, tag
import json

# locust -f src/http/https.py -u 1 -r 1 --logfile logs/output.log --loglevel DEBUG --only-summary --tags login --headless


class LoadUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://moodle.uni-due.de"

    @tag('login')
    @task
    def login(self):
        with self.client.post(
            "/login/index.php",
            data=json.dumps({ "username":"prashanthsams", "password":"covid@2020", "anchor":"" }),
            headers={"Content-Type": "application/json", "Origin": "https://moodle.uni-due.de", "Referer": "https://moodle.uni-due.de/login/index.php"},
            name="Login Moodle",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                print('logged in')
                print(response.content)
                print(response.text)
                print(response.headers)
                response.success()
            else:
                response.failure('api failed') ## for custom error - else remove it
                
    @tag('login2')
    @task
    def login2(self):
        req = self.client.post(
            url="/login/index.php",
            data=json.dumps({ "username":"prashanthsams", "password":"covid@2020", "anchor":"" }),
            headers={"Content-Type": "application/json", "Origin": "https://moodle.uni-due.de", "Referer": "https://moodle.uni-due.de/login/index.php"},
            name="Login Moodle",
        )
        print(req.status_code)
        print(req.content)
        print('logged in')