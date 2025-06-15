# Isabak

Backup your docker services.

## Dependencies

Install all the dependencies by running `pip install -r requirements.txt`.

## Configuration

Run `cp .env.example .env` and `cp config.yaml.example config.yaml` to create the base config files and edit them as needed.

The `.env` variable will override the `config.yaml` variables.
e.g. if you set both the `global.destination` in the `config.yaml` and the `DESTINATION` in the `.env`, the `.env` value will be used.

`.env` supports environment variables, e.g. `DESTINATION="${BACKUP_BASE_PATH}backups"` 

All services paths can use ${} to add an environment variable in the path itself. e.g. `folder: "${YOUR_SERVICE_BASE_PATH}/your_service_files"` where the env variable `YOUR_SERVICE_BASE_PATH` is `/home/user/` will become `/home/user/your_service_files`. In this specific situations, env variables can only be named with letter numbers and underscores (`_`). 

### Env to Yaml mapping
DOMAIN => global.domain
DESTINATION => global.destination

### List
- `global.domain`: used to generate backups for the ARR stack.
- `global.destination`: place where backups will be created

## Notes

MariaDB dump tool changed from mysqldump to mariadb-dump since mariadb 10.5, prior version would not dump the database correctly.

Do a run and **check all the backups are working**. Also check the content of gzipped files.

A folder `isabak` will be created at the `global.destination` and backups will be added inside, the folder will be deleted and recreated each usage.

## TODO
- Change logs level using config.yaml `global.log_level`
- move logger config to another file instead of main.py
- automated tests
- log files in debug mode that keeps 1 week of logs
  - it will show borgbackup disk usage and upload times
- allow arrays in yaml config services, to have multiple fs or multiple DBs
