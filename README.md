# Isabak
Backup your docker services

## Environment Variables
If any backups use the api feature, a `SRV_DOMAIN` environment variable is needed.

Eg. `export SERV_DOMAIN="https://yourdomain.com"`

## TODO
- Use dotenv library
- Change logs level using config.yaml `global.log_level`
- use env vars in config.yaml (for base paths or domain)
- move logger config to another file instead of main.py
