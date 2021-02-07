# Locust Boilerplate
> Exercise locust with sample programs

### Prerequisites

    python3 -m venv venv/
    source venv/bin/activate
    pip3 install -r requirements.txt

### Execution

- Web Interface
```
locust -f src/test/task/hooks.py
```
- Headless Mode
```
locust -f src/test/task/weightage.py MobileUser -u 5 -r 1 -t 10s --headless --logfile logs/output.log --loglevel DEBUG --only-summary
```
> Docker Execution
```
docker run -p 8089:8089 -v $(pwd):/mnt/locust locustio/locust:master -f /mnt/locust/src/test/task/hooks -u 4 -r 1
```
> Scale up slaves
``` 
docker-compose up --scale worker=4
```