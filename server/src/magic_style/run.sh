#! /bin/bash

echo -e "\e[1;31m 1. initializing databases \e[0m"
while :; do
    if python3 manage.py migrate; then
        break
    fi
    sleep 1
done

#python3 manage.py create_superuser
echo -e "\e[1;31m 2. server start \e[0m"
gunicorn magic_style.wsgi:application -c gunicorn_conf.py
echo -e "\e[1;31m 3. finished! \e[0m"
