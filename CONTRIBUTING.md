# Contributing

Thank you for helping improve ASCII 3D Cube.

## Development setup

Fork and clone the repository, then create a virtual environment:

~~~bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
~~~

On Windows, activate the environment with:

~~~powershell
.venv\Scripts\activate
~~~

## Quality checks

Run these commands before opening a pull request:

~~~bash
ruff check .
pytest
~~~

Keep pull requests focused, include tests for behavior changes, and update the
README when a change affects users.

## Reporting bugs

Open a GitHub issue with your operating system, Python version, terminal
application, reproduction steps, and the expected and actual behavior.
