from locust import User, HttpUser, between, task, events, TaskSet, tag
import locust.event

# locust -f src/test/events/trigger.py -u 1 -r 1 --headless --tags first
# locust -f src/test/events/trigger.py -u 1 -r 1 --headless --tags second


trigger_event1 = locust.event.EventHook()
trigger_event2 = locust.event.EventHook()

def handler1(a, b, **kwargs):
    print('add', a+b)

def handler2(a, b, **kwargs):
    print('diff', b-a)

def handler3(a, b, **kwargs):
    print('multiply', a*b)

trigger_event1.add_listener(handler1)
trigger_event1.add_listener(handler2)
trigger_event2.add_listener(handler3)


class TriggerTask(TaskSet):

    @tag('first')
    @task
    def index_1(self):
        trigger_event1.fire(a=2, b=2, message='first')
    
    @tag('second')
    @task
    def index_2(self):
        trigger_event2.fire(a=2, b=2, message='second')


class LoadUser(User):
    tasks = [TriggerTask]
    wait_time = between(1, 3)

    
