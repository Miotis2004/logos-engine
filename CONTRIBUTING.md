# Contributing

Thanks for helping improve Logos Engine.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Checks

```bash
ruff check src tests
mypy src
pytest
```
