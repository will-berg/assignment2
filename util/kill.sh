#!/bin/bash
cd $(dirname $0)

[ -f /tmp/pid_updater ] && kill -TERM $(cat /tmp/pid_updater)