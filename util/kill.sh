#!/bin/bash
cd $(dirname $0)

[ -f /tmp/pid_updater ] && kill -TERM $(cat /tmp/pid_updater)
[ -f /tmp/pid_web ] && kill -TERM $(cat /tmp/pid_web)
[ -f /tmp/pid_ci ] && kill -TERM $(cat /tmp/pid_ci)
