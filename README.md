# sib

Forward http request to several targets (smtp/http/db/log/...) through RabbitMQ queues.

Currently the only implemented targets are:
- email
- http

# Run

```bash
docker-compose up -d
```

# Example

```bash
curl -X POST -H "Some: Value" -d "{\"x\": 42}" http://localhost:5000/   
```

# Tests

```bash
docker build -t sib-test .
docker run --rm sib-test python -m pytest /sib/tests
docker image rm -f sib-test
```

# TODO

It's not really easy and reliable to use mocked rabbit, it's better to add integration tests as well.
