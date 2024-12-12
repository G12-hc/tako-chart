# tako-chart
[Read our Wiki for Repository Information](../../wiki)
Dependencies:
- python3.12
- python3.12-venv
- libpq-dev
- postgresql-16 (or later)
- [cloc](https://github.com/AlDanial/cloc)
- Optional: a make implementation, such as GNU Make

## Setup

Before running the server, you will need to [obtain a GitHub personal token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token) (ideally a fine-grained token). After you get one, create `cfg.ini` in the root of this repository with these contents:
```ini
[tokens]
github = <put your github token here>
```

After that's done, and Postgres is up and running, you should set up a virtual environment and start the server:

```
$ make venv # Setup up the virtual environment, also installs the pip deps
$ make dev-server # Run development server (also supports reload)
$ make deps # To reinstall dependencies
$ make clean # Clean the virtual environment
```
