#/bin/bash
gunicorn -b 0.0.0.0:8001 --daemon --pid /tmp/pid_ci 'ci_server:app'
