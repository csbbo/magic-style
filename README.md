# magic-style

## 安装环境

Docker  
docker-compose

## 打包
```.env
bash package.sh
```

## 部署
将项目下打包好的安装包复制到要部署的文件夹
```.env
cp magic_style_date.zip /path/to/deploy/
```

解压安装包
```.env
uzip magic_style_date.zip
```

下载vgg16模型到magic_style_date中
```.env
cd magic_style_date
unzip -P password magic_style_date.zip
unzip anime.zip
unzip migrate.zip
```

执行部署脚本
```.env
bash deploy.sh
```