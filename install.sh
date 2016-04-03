set -e

pip3 install --upgrade flask flask-login flask-sqlalchemy requests

cat /dev/urandom | env LC_CTYPE=C tr -cd a-zA-Z0-9 |\
	head -c 32 > classcloud.token

mkdir files
