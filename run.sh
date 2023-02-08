#/bin/bash
[ ! -d /srv/ci/ ] && mkdir /srv/ci
gunicorn -b 0.0.0.0:8001 --daemon --pid /tmp/pid_ci --access-logfile /var/log/ci_access --error-logfile /var/log/ci_error 'ci_server:app'
gunicorn -b 0.0.0.0:80   --daemon --pid /tmp/pid_web --access-logfile /var/log/web_access --error-logfile /var/log/web_error 'web:app'
gunicorn -b 0.0.0.0:8002 --daemon --pid /tmp/pid_updater --access-logfile /var/log/updater_access --error-logfile /var/log/updater_error 'updater:app'
