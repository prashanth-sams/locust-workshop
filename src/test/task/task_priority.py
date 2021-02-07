from locust import HttpUser, between, task, events, TaskSet, SequentialTaskSet

# locust -f src/test/task/task_priority.py -u 1 -r 1 --headless --logfile logs/output.log --loglevel DEBUG --only-summary


class LoadUserSequentialTaskSet(HttpUser):
    wait_time = between(1, 3)
    host = "https://api.todoist.com/rest/v1/projects"

    @task
    class StoreTaskSet(SequentialTaskSet):
        @task
        def task_1(self):
            print('Running index - 1')
            self.client.get("/")
        
        @task
        def task_2(self):
            print('Running index - 2')
            self.client.get("/")
