Godeyes
===

作为班长的你，曾经是否经历过给班级集体照标注人名的琐碎烦人的事情？不要慌，现在有一个小程序可以解决你的烦恼。这个项目是faceplus微信小程序后台的代码，它基于开源人脸识别框架[face_recognition](https://github.com/ageitgey/face_recognition)和自研的定位算法，从合照中精确定位用户所在行列，并支持导出人名表单，从此班主任再也不用担心给你的活过多了😉。

### 支持功能

1. 上传集体照
2. 查看集体照
3. 上传自拍照
4. 在合照中框出自己
5. 获取在合照中自己的行列位置
6. 导出合照中人名表


### 安装

1. 安装[docker](https://docs.docker.com/v17.12/docker-for-mac/install/)
2. 安装[anaconda](https://www.anaconda.com/distribution/#download-section)
3. 从github拉下代码到本地
```
git clone https://github.com/xiaolao/godeyes.git ~/
```
4. 创建虚拟环境并激活
```
cd ~/godeyes
conda create --name godeyes --file requirements.txt
conda activate godeyes
```
5. 安装[face_regconition](https://github.com/ageitgey/face_recognition)和依赖
```
pip install face_recognition
```
6. 安装其他依赖包
```
conda activate godeyes
pip install sanic
pip install aiomysql
pip install aioredis
pip install aiofiles
pip install uvloop
pip install sanic-openapi
```

### 运行
1. 启动mysql服务和redis服务
```
cd ~/godeyes/conf
sudo docker-compose -f mysql.yml up -d
sudo docker-compose -f redis.yml up -d
```
2. 启动人脸解析程序
```
cd ~/godeyes
conda activate godeyes
python worker.py
```
3. 启动web服务
```
cd ~/godeyes
conda activate godeyes
python run.py
```
