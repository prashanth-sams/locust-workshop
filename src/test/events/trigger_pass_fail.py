from locust import User, HttpUser, between, task, events, TaskSet, tag
import locust.event
import json, socket

hostname = socket.gethostname()

# locust -f src/test/events/trigger_pass_fail.py -u 1 -r 1 --headless


@events.request_success.add_listener
def success(request_type, name, response_time, response_length, **kw):
    data = ' "hostname": {}, "request_type":{}, "name": {}, "result": "OK", "response_time": {}, "response_length":{} '\
        .format(hostname,request_type,name,response_time,response_length)
    print('success event triggered')
    print(data)

@events.request_failure.add_listener
def failure(request_type, name, response_time, response_length, exception, **kw):
    data = ' "hostname": {}, "request_type": {}, "name": {}, "result": "Not OK", "response_time": {}, "response_length": {}'\
        .format(hostname, request_type, name, response_time, response_length,exception)
    print('failure event triggered')
    print(data)


class TriggerTask(TaskSet):
    
    @task
    def index_1(self):
        with self.client.post(
            "/login/index.php",
            data=json.dumps({ "username":"prashanthsams", "password":"covid@2020", "anchor":"" }),
            headers={"Content-Type": "application/json", "Origin": "https://moodle.uni-due.de", "Referer": "https://moodle.uni-due.de/login/index.php"},
            name="Login Moodle",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure('failure response')


class LoadUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://moodle.uni-due.de"

    tasks = [TriggerTask]
