# Lab Web

Small web interface for checking the status of several lab environments.

Currently this only supports Fuel-devops 2.9

This operates in 2 parts.

One part is the collector on each node. It runs via cron and places a json blob into a local web server.
Queries on the lab nodes were slow, and it seemed unnecissary to have a full webapp running on each node.

The other part is the web application its self. It is a simple flask app with a yaml configuration file.

Fuel-devops was installed in a virtualenv, so it is necissary for cron to call the virtualenv's python binary.

```shell
*   * *	* * sudo /home/sto/.virtualenvs/fuel-devops-venv-2.9/bin/python /home/sto/bin/json_env_info.py /var/www/html/env.json > /dev/null 2>&1
```