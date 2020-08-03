# Simple Web Poller

Simple Python app (microservice) to read a given web page from a provided URL and write output to stdio or Redis server. It is intended to be run from systemd as a service, but it should also work under whatever scheduler or service manager you use.

requires a running Redis server, Python 3.7+, Redis-py, e.g., pip install redis.

## installation as a systemd service

Assuming you are running this as `ubuntu` user, with a virtual environment setup under `~/.venvs/default/`, and your script is installed under `~/Projects/simple_web_poller`,
add the following to your `/etc/systemd/system` folder, name it something sensible like `simple_web_poller.service`:

```
[Unit]
Description=Simple Web Poller Service
After=redis-server.service

[Service]
Type=simple
User=ubuntu
ExecStart=/home/ubuntu/.venvs/default/bin/python /home/ubuntu/Projects/simple_web_poller/simple_web_poller.py -r -f 10 -k example http://example.com/
Restart=on-abort

[Install]
WantedBy=multi-user.target
```

After installation, run `sudo systemctl daemon-reload` to pick up the changes, then `sudo systemctl start simple_web_poller.service` (assuming that's the name you gave it).

You can be sure it's running by checking `sudo systemctl status temperature-monitor` and `sudo journalctl -u simple_web_poller` for details.

When satisfied that everything is working as intended, you can permanently install the temperature monitor by entering `sudo systemctl enable simple_web_poller`.

## Running More Than One Web Poller
Same as above, but give each poller service a unique description and filename. You will want to adjust the Key argument (-k) to be unique so you don't overwrite each poller's contents in redis.

## License

Do what you want with this.
