# Locust Boilerplate
> Excercise locust with programs

### Prerequisites

    python3 -m venv venv/
    source venv/bin/activate
    pip3 install -r requirements.txt

### Execution

- Web Interface
```
locust -f src/locust.py
```
- Headless Mode
```
locust -f src/locust.py -u 5 -r 5 -t 10s --headless --logfile logs/output.log --loglevel DEBUG
```
> with hooks, multiple class, weightage with class and task, logs, headless mode, runtime, task reusability, task reusability with weightage, task set, sequential task set, nested task set, interrupt
```
locust -f src/locust.py MobileUser -u 1 -r 1 --headless --logfile logs/output.log --loglevel DEBUG --only-summary
```