# My chess Style

[![codecov](https://codecov.io/github/calvom/my-chess-style/branch/main/graph/badge.svg?token=KTFUJR875Z)](https://codecov.io/github/calvom/my-chess-style)

## References

Reference Document: [Read more](https://docs.google.com/document/d/1tZYcn5qNHjpreDugcLztrE3W7mYAtdBTe6WdIZlW5GY/edit?usp=sharing)

Daily progress details: [Daily progress](https://splendid-bean-849.notion.site/My-chess-style-progress-style-1cbc2a6e3b5e804dbcf8f4ea76cbb865)

## Getting started

Please install `uv` tool to manage the application following instructions from [link](https://docs.astral.sh/uv/getting-started/installation/)

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install the dependencies using the following command:

```sh
uv add -r requirements.txt
```

Install the pre-commit hooks using the following command:

```sh
uv run pre-commit install
```

To run the django server, run and replace `address`:

```sh
uv run python manage.py runserver <address>
```

## Run Tests

Please run the following command:

```sh
uv run pytest

```

## Celery tasks

Run celery worker.

```sh
uv run celery -A my_chess_style worker --loglevel=info
```

Run the celery flower to inspect the tasks on a web interface.

```sh
uv run celery -A my_chess_style flower --port=5555
```

## LLM Configuration

1. Install [Ollama](https://ollama.com/download)

2. Pull/Install the various LLMs e.g. deepseek.

3. Run the ollama server.

```sh
ollama serve
```
