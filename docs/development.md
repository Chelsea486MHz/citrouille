# Development documentation

## Set up a development environment

Clone the repo:
```bash
$ git clone https://github.com/Chelsea486MHz/citrouille
$ cd citrouille
```

Install dependencies in a virtual environment:
```bash
$ python3.14 -m venv venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt -r requirements-dev.txt
```

Build the project:
```bash
$ pip install -e .
```

Run tests:
```bash
$ pytest -v
```

## Tests

The tool is not tested against a cluster due to CI/CD limitations. Kube requests are emulated.