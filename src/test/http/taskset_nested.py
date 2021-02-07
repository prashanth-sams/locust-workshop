from locust import HttpUser, between, task, SequentialTaskSet, TaskSet
import json

# locust -f src/test/http/taskset_nested.py -u 1 -r 1 --logfile logs/output.log --loglevel DEBUG --only-summary --headless


class PerformTask(SequentialTaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.session_id = ""

    @task
    class task_1(SequentialTaskSet):
        @task()
        def login(self):
            with self.client.post(
                "/api/users",
                data=json.dumps({ "name": "Prashanth Sams", "job": "QA Lead"}),
                headers={"Content-Type": "application/json"},
                name="Create User",
                catch_response=True
            ) as response:
                if response.status_code == 201:
                    self.response = response.json()
                    response.success()

        @task()
        def nextstep(self):
            print(self.response)
        
        @task()
        def stop(self):
            self.interrupt()
    
    @task
    class task_2(SequentialTaskSet):
        @task
        def login(self):
            print('login')

        @task
        def nextstep(self):
            print('next step')
        
        @task
        def stop(self):
            print('stop')
            self.interrupt()

class LoadUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://reqres.in"

    tasks = [PerformTask]