from locust import HttpUser, between, task, SequentialTaskSet
import json
import uuid

# locust -f src/http/json_data.py  -u 1 -r 1 --logfile logs/output.log --loglevel DEBUG --only-summary --headless


class PerformTask(SequentialTaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.session_id = ""
    
    def on_start(self):
        self.randomid = str(uuid.uuid4())
        print(self.randomid)

    @task
    def login(self):
        with self.client.post(
            "/api/users",
            data=json.dumps({ "name": "Prashanth Sams", "job": "QA Lead"}),
            headers={"Content-Type": "application/json"},
            name="Create User",
            catch_response=True
        ) as response:
            if response.status_code == 201:
                custom_resp = response.json()
                print(custom_resp['name'])
                response.success()


class LoadUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://reqres.in"

    tasks = [PerformTask]