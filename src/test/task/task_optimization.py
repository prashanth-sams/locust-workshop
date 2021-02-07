from locust import HttpUser, between

# locust -f src/test/task/task_optimization.py -u 1 -r 1 --headless --logfile logs/output.log --loglevel DEBUG --only-summary


def index_1(self):
    print('Running index - 1')
    self.client.get("/")


def index_2(self):
    print('Running index - 2')
    self.client.get("/")


class LoadUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://api.todoist.com/rest/v1/projects"
    
    tasks = [index_1, index_2]


class LoadUserWeight(HttpUser):
    wait_time = between(1, 3)
    host = "https://api.todoist.com/rest/v1/projects"

    tasks = {index_1: 1, index_2: 2}
