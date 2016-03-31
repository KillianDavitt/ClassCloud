set -e

cat /dev/urandom | env LC_CTYPE=C tr -cd a-zA-Z0-9 |\
	head -c 32 > classcloud.token
mkdir files
