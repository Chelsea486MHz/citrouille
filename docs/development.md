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
$ python -m build
```

Run tests:
```bash
$ pytest -v
```