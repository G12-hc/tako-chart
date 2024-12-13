# tako-chart
[Read our Wiki for Repository Information](../../wiki)
## Setup
### 0. System Requirements
This project is primarily built for deployment in a linux-based environment. Deployment on Windows is possible using WSL, or with additional manual steps.
- Linux-based OS
- MacOS
- Windows (Using WSL)
- Windows (Manual)
<br>
Before running the server, you will need to [obtain a GitHub personal token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)  ideally a fine-grained token. After you get one, create `cfg.ini` in the root of this repository with these contents:
```ini
[tokens]
github = <put your github token here>
```
### 1. Install System Dependencies
- python3.12
- python3.12-venv
- libpq-dev
- [cloc](https://github.com/AlDanial/cloc)
- postgresql-16 (minimum)
- make (optional)

### 2. Initialise Database
#### Note: If you are reading this Quick Start Guide, you should already have the SQL file to populate the database.
1. Initialise the database with `su -l postgres -c "initdb --locale=C.UTF-8 --encoding=UTF8 -D '/var/lib/postgres/data'"`
2. Start or enable the postgresql service. With systemd, `systemctl start postgresql`.
3. Create the table with `sudo -u postgres psql -c 'CREATE DATABASE hackcamp;'`
4. Populate the database with the SQL file `sudo -u postgres psql -U postgres -d hackcamp -a -f /path/to/.sql_file`

### 3. Clone Repository
Clone Directory: `git clone https://github.com/G12-hc/tako-chart.git`<br>
Navigate to repository directory: `cd tako-chart`

### 4. Install Python Dependencies and Run
To set up a virtual environment and start the server:
```
$ make venv # Setup up the virtual environment, also installs the pip deps
$ make dev-server # Run development server (also supports reload)
$ make deps # To reinstall dependencies
$ make clean # Clean the virtual environment
```
### 5. Done!
Open in browser at `http://HOST_IP:8000`
- If running on the same machine: `http://localhost:8000`
