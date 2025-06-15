# Isabak

Backup your docker services

## Environment Variables

If any backups use the api feature, a `SRV_DOMAIN` environment variable is needed.

Eg. `export SERV_DOMAIN="https://yourdomain.com"`

## Notes

MariaDB dump tool changed from mysqldump to mariadb-dump since mariadb 10.5, prior version would not dump the database correctly.

Do a run and **check all the backups are working**. Also check the content of gzipped files.

## TODO
- Use dotenv library
- Change logs level using config.yaml `global.log_level`
- use env vars in config.yaml (for base paths or domain)
- move logger config to another file instead of main.py
- automated tests
- log files in debug mode that keeps 1 week of logs
  - it will show borgbackup disk usage and upload times
