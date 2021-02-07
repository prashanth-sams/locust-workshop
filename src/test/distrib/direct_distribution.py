from locust import HttpUser, between, task, events

# locust -f src/test/distrib/direct_distribution.py --master --headless -u 4 -r 2
# locust -f src/test/distrib/direct_distribution.py --worker

# locust -f src/test/distrib/direct_distribution.py --master --headless -u 4 -r 2 --expect-workers=2

@events.test_start.add_listener
def script_start(**kwargs):
    print('DB connected')


@events.test_stop.add_listener
def script_stop(**kwargs):
    print('DB disconnected')


class LoadUser(HttpUser):
    wait_time = between(1, 3)

    host = "https://moodle.uni-due.de"

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