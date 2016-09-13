# ClassCloud
A minimal cloud storage service written in Flask

ClassCloud accepts HTTP requests to list, get, and put files.

## Deployment

These are instructions for a deployment on debian/ubuntu using nginx and uwsgi to host the app.

We will also use systemd to run the uwsgi service

```bash
git clone https://github.com/KillianDavitt/ClassCloud.git

cd ClassCloud

virtualenv --python=python3 flask

flask/bin/pip3 install -r requirements.txt

#Quick check of the tests
flask/bin/python3 tests.py
```
Ensure nginx is installed before this next step

Then edit deploy/classcloud-nginx to suit your needs, your domain name etc etc
```bash
cp ./deploy/classcloud-nginx /etc/nginx/site-enabled/classcloud
cp ./deploy/classcloud.service /etc/systemd/system/classcloud.service

sudo systemctl enable classcloud
sudo systemctl start classcloud

sudo systemctl status classcloud

sudo systemctl restart nginx

```

Try using curl against the hostname you provided in the nginx config to check if it's working


