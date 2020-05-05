#! /bin/bash

# set package version
set -e
if [ $# -lt 1 ]
then
    now_date=$(date +"%Y%m%d")
    VERSION=${now_date}
else
    VERSION=${1}
fi

if [ -d magic_style ]; then
  echo "magic_style is exsit"
else
  mkdir magic_style
fi

echo "------------yarn install and build frontend------------"
cd ./frontend
yarn
yarn versions
yarn build
echo "------------finished------------"

echo "------------copy frontend to openresty------------"
cd ..
cp -rf ./frontend/dist ./openresty
echo "------------finished------------"

echo "------------build the openresty docker images------------"
docker build -t ms_openresty ./openresty
echo "------------finished------------"

echo "------------build the server docker images------------"
docker build -t ms_server ./server
echo "------------finished------------"

echo "------------build the style_migrate docker images------------"
docker build -t ms_style_migrate ./style_migrate
echo "------------finished------------"

echo "------------build the style_migrate docker images------------"
docker build -t ms_anime_style ./anime_style
echo "------------finished------------"

echo "------------pull the postgres image------------"
docker pull postgres:12.0
echo "------------finished------------"


echo "------------export and zip the images to deploy------------"
docker save -o ./ms_server.tar postgres:12.0 ms_openresty:latest ms_server:latest ms_style_migrate:latest ms_anime_style:latest
gzip ms_server.tar
cp ms_server.tar.gz ./magic_style
rm ms_server.tar.gz
echo "------------finished------------"

echo "------------copy deploy resource file to deploy------------"
cp ./deploy/deploy.sh ./magic_style
cp ./deploy/docker-compose.yml ./magic_style
echo "------------finished------------"


echo "------------create the final package------------"
PASSWRD=$(openssl rand -base64 10)
echo $PASSWRD > password.txt
zip -j ./magic_style.zip ./magic_style/* -P $PASSWRD
mv ./magic_style.zip "magic_style_${VERSION}.zip"
rm -rf ./magic_style

packagedir="magic_style_${VERSION}"
mkdir $packagedir
mv password.txt $packagedir
mv "magic_style_${VERSION}.zip" $packagedir
zip -r "${packagedir}.zip" $packagedir
rm -rf $packagedir
echo "------------finished------------"

echo "------------clean up package env------------"
rm -rf ./openresty/dist
rm -rf ./frontend/dist
docker image rm ms_openresty:latest ms_server:latest ms_style_migrate:latest
echo "------------finished------------"
