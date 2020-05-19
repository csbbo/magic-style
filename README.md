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
cp magic_style_`date`.zip /path/to/deploy/
```

解压安装包
```.env
uzip magic_style_date.zip
```

下载含动漫风格迁移训练完成模型压缩包anime.zip,含风格迁移所需要的MSCOCO数据集和vgg16模型压缩包migrate.zip到magic_style_date文件夹中

[anime.zip](https://pan.baidu.com/s/1WbIGUX3IYi_FRDEiwdLnmw) 密码: gqh0
[migrate.zip](https://pan.baidu.com/s/1DEaPQ1ytdhBNL3weT3bczQ) 密码: pij7
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
