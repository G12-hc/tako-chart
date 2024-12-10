# tako-chart
[Read our Wiki for Repository Information](../../wiki)
Dependencies:
- python3.12
- python3.12-venv
- libpq-dev
- postgresql-16
- Optional: a make implementation, such as GNU Make

## Setup

```
$ make venv # Setup up the virtual environment, also installs the pip deps
$ make dev-server # Run development server (also supports reload)
$ make deps # To reinstall dependencies
$ make clean # Clean the virtual environment
```
