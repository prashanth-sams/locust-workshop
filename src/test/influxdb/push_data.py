from locust import HttpUser, between, task, TaskSet, events
from influxdb import InfluxDBClient
import datetime
import pytz
import locust.event
import json, socket

# locust -f src/test/influxdb/push_data.py -u 1 -r 1 --headless --run-time 10s

# curl -G http://localhost:8086/query --data-urlencode "q=SHOW DATABASES"

# influx

# CREATE DATABASE locustdb
# SHOW DATABASES
# SHOW USERS
# use locustdb
# select * from ResponseTable

# curl -G 'http://localhost:8086/query?db=locustdb' --data-urlencode "q=select * from ResponseTable"

# docker run -d -p 8086:8086 influxdb
# docker exec -it <container_id> bash

# docker run -d --name=grafana -p 3000:3000 grafana/grafana
# admin/admin
# SELECT responseTime FROM "ResponseTable" WHERE ("requestName" = 'Login CRM')

hostname = socket.gethostname()
clientdb=InfluxDBClient(host="localhost", port="8086")
clientdb.switch_database("locustdb")

@events.request_success.add_listener
def success(request_type, name, response_time, response_length, **kwargs):
    SUCCESS_TEMPLATE = '[{"measurement": "%s","tags": {"hostname":"%s","requestName": "%s","requestType": "%s","status":"%s"' \
                       '},"time":"%s","fields": {"responseTime": "%s","responseLength":"%s"}' \
                       '}]'
    json_string=SUCCESS_TEMPLATE%("ResponseTable",hostname,name,request_type,"OK",datetime.datetime.now(tz=pytz.UTC),response_time,response_length)
    print(json_string)
    clientdb.write_points(json.loads(json_string))

@events.request_failure.add_listener
def failure(request_type, name, response_time, response_length, exception, **kwargs):
    FAIL_TEMPLATE = '[{"measurement": "%s","tags": {"hostname":"%s","requestName": "%s","requestType": "%s","exception":"%s","status":"%s"' \
                    '},"time":"%s","fields": {"responseTime": "%s","responseLength":"%s"}' \
                    '}]'
    json_string=FAIL_TEMPLATE%("ResponseTable",hostname,name,request_type,exception,"FAIL",datetime.datetime.now(tz=pytz.UTC),response_time,response_length)
    print(json_string)
    clientdb.write_points(json.loads(json_string))


class TriggerTask(TaskSet):
    
    @task
    def index_1(self):
        with self.client.post(
            url="/login/index.php",
            data=json.dumps({ "username": "prashanthsams", "password": "covid@2020", "anchor": "" }),
            headers={"Content-Type": "application/json", "Origin": "https://moodle.uni-due.de", "Referer": "https://moodle.uni-due.de/login/index.php"},
            name="Login Moodle",
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure('failure response')


class LoadUser(HttpUser):
    tasks = [TriggerTask]
    wait_time = between(1, 3)
    host = "https://moodle.uni-due.de"
    
