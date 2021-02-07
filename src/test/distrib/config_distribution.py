from locust import HttpUser, between, task, events

# locust --config=config/master.yml
# locust --config=config/slave.yml


@events.test_start.add_listener
def script_start(**kwargs):
    print('DB connected')


@events.test_stop.add_listener
def script_stop(**kwargs):
    print('DB disconnected')


class LoadUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        print('Start Hook')

    @task
    def index_1(self):
        print('Running index 1')
        self.client.get("/")

    @task
    def index_2(self):
        print('Running index 2')
        self.client.get("/")

    def on_stop(self):
        print('Stop Hook')