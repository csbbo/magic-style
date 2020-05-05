#! /bin/bash

echo "--------------check the time----------------"
date -R
echo "----------please check the time-------------"

#echo "--------unzip style migrate date------------"
#unzip migrate.zip
#echo "---------------unzip finish-----------------"

echo "--------------load docker images------------"
docker load -i ms_server.tar.gz
echo "--------------load docker finish------------"

echo "-------------docker-compose up--------------"
docker-compose up -d
echo "------------docker-compose done-------------"

# figlet
cat <<-'EOF'

 __  __             _        ____  _         _      
|  \/  | __ _  __ _(_) ___  / ___|| |_ _   _| | ___ 
| |\/| |/ _` |/ _` | |/ __| \___ \| __| | | | |/ _ \
| |  | | (_| | (_| | | (__   ___) | |_| |_| | |  __/
|_|  |_|\__,_|\__, |_|\___| |____/ \__|\__, |_|\___|
              |___/                    |___/        

Server running successfully!
EOF
