from locust import HttpUser, between, task, events, TaskSet, SequentialTaskSet

# locust -f src/taskset_resuse.py -u 1 -r 1 --headless --logfile logs/output.log --loglevel DEBUG --only-summary


class StoreTaskSet(TaskSet):
    @task()
    def task_1(self):
        print('Running index - 1')
        self.client.get("/")
    
    @task()
    def task_2(self):
        print('Running index - 2')
        self.client.get("/")


class LoadUserTaskSet(HttpUser):
    wait_time = between(1, 3)
    host = "https://api.todoist.com/rest/v1/projects"

    tasks = [StoreTaskSet]
