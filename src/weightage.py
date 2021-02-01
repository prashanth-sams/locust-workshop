from locust import HttpUser, between, task, events

# locust -f src/weightage.py -u 1 -r 1 --headless --logfile logs/output.log --loglevel DEBUG --only-summary


class DesktopUser(HttpUser):
    wait_time = between(1, 3)
    weight = 2

    host = "https://api.todoist.com/rest/v1/projects"

    @task(1)
    def index_1(self):
        print('Running index 1 - DESKTOP User')
        self.client.get("/")

    @task(2)
    def index_2(self):
        print('Running index 2 - DESKTOP User')
        self.client.get("/")


class MobileUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://api.todoist.com/rest/v1/projects"
    weight = 1
    
    @task
    def index_3(self):
        print('Running index 3 - MOBILE User')
        self.client.get("/")
    

