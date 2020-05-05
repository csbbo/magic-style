#! /bin/bash

echo -e "\033[1;32m initializing databases \033[0m"
while :; do
    if python3 manage.py migrate; then
        break
    fi
    sleep 1
done

echo -e "\033[1;32m server start \033[0m"

gunicorn magic_style.wsgi:application -c gunicorn_conf.py
echo -e "\033[1;32m finished! \033[0m"
