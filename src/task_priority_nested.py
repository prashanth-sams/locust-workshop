from locust import HttpUser, between, task, SequentialTaskSet

# locust -f src/task_priority_nested.py -u 1 -r 1 --headless --logfile logs/output.log --loglevel DEBUG --only-summary


class LoadUserNestedSequentialTaskSet(HttpUser):
    wait_time = between(1, 3)
    host = "https://api.todoist.com/rest/v1/projects"

    @task()
    class OuterTaskSet(SequentialTaskSet):
        @task()
        class StoreTaskSet1(SequentialTaskSet):
            @task()
            def task_3(self):
                print('Running index A - 1')
                self.client.get("/")
            
            @task()
            def task_4(self):
                print('Running index A - 2')
                self.client.get("/")
                self.interrupt()

        @task()
        class StoreTaskSet2(SequentialTaskSet):
            @task()
            def task_5(self):
                print('Running index B - 3')
                self.client.get("/")
            
            @task()
            def task_6(self):
                print('Running index B - 4')
                self.client.get("/")
                self.interrupt()
