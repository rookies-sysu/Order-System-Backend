[![Build Status](https://travis-ci.org/rookies-sysu/Order-System-Backend.svg?branch=docker)](https://travis-ci.org/rookies-sysu/Order-System-Backend)

# Order-System-Backend 后台部署文档
Order system backend; Nginx + python3 flask + mysql db

---

## 一、部署架构图

![](https://github.com/rookies-sysu/Dashboard/blob/master/imgs/deployment_img.png?raw=true)


---

## 二、部署流程

### 1. 服务器后台环境配置

#### 1.1 服务器系统环境

- 腾讯云 Ubuntu 16.04 LTS Server

#### 1.2 Docker 安装

- [官方参考链接](https://docs.docker.com/install/linux/docker-ce/ubuntu/#prerequisites)

- [中文参考链接](https://yeasy.gitbooks.io/docker_practice/content/install/ubuntu.html)

若通过上面链接中给出的安装测试 `sudo docker run hello-world` ，则证明安装成功。

#### 1.3 Docker-Compose 安装

- [官方参考链接](https://docs.docker.com/compose/install/)

截至于 2018/06/24 版本安装示例：

1. Run this command to download the latest version of Docker Compose:
```bash
sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
```

2. Apply executable permissions to the binary:
```bash
sudo chmod +x /usr/local/bin/docker-compose
```

3. Test the installation.
```bash
$ docker-compose --version
docker-compose version 1.21.2, build 1719ceb
```

#### 1.4 Mysql-Client 安装（验证测试用）

```
sudo apt install mysql-client
```

### 2. 服务器程序配置运行

#### 2.1 拉取后台源代码

```bash
git clone https://github.com/rookies-sysu/Order-System-Backend
```

#### 2.2 放置 Vue build 出来的静态页面

将 vue build 出来的静态页面文件夹 `dist` 复制放到 `client/` 文件夹下。

#### 2.3 Docker-compose 一键部署

```bash 
cd Order-System-Backend
docker-compose up -d
```

#### 2.4 测试服务器运行状况

```bash
curl localhost:8080/api/testRedis
Hello Tiny-Hippo Backend!! I have been seen 1 times.
```

有获得以上响应则说明 api 转发部署成功。

```bash
curl localhost:8080/
```

若成功 get 到页面文件，则说明使用 vue 写的 web 前端商品管理页面转发部署成功。

---

#### 2.5 插入服务器初始化内容

```bash
curl localhost:8080/api/insert_fake_data2
```

## 三、常见问题解决方法

### 1. Docker 安装失败

可能是因为天朝被墙的原因，强烈建议使用国内源而不是官方源，详情可以见前面 docker 安装的[中文参考链接](https://yeasy.gitbooks.io/docker_practice/content/install/ubuntu.html)。

### 2. Docker 镜像拉取缓慢

使用国内镜像源加速。

[参考链接](https://yeasy.gitbooks.io/docker_practice/content/install/mirror.html)

### 3. 需要查看数据库内部状态使用

```
mysql -h 127.0.0.1 -P 3306 -uroot -ptiny-hippo
```

即可以正常使用 mysql-client 访问数据库

### 4. 需要重建数据库

```
make redeploy
```

### 5. 需要重新 build 镜像

```
make rebuild
```

### 6. docker-compose up -d 后访问服务器 502 Bad Gateway

后台以及数据库第一次部署的时候需要一定时间进行初始化，请耐心等待十几秒后再发出请求

或者，也可以改用 `docker-compose up` 命令，让后台的输出重定向到终端上，当看到下图时说明服务器已经初始化完成并且正在正常监听，此时再发出请求。

![flask 正常工作的截图](http://or5jajfqs.bkt.clouddn.com/flask_working.png)

### 7. 数据库 TINYHIPPO 中无数据

请再次尝试使用 api 导入初始数据：

```bash
curl localhost:8080/api/insert_fake_data2
```

### 8. Vue 前端访问 localhost 出现跨域错误

因为该前端 build 出来的拿数据的 api 指向的是我们的服务器，所以直接在本地部署并且尝试访问 localhost:8080 后要拿数据的话会出现跨域错误。所以只需要去前端代码把拿数据的api改成你需要部署的 api 地址再重新 build 即可。

- [点餐系统 微信小程序前端](https://github.com/rookies-sysu/Order-System-Frontend)
- [管理系统 Vue 前端](https://github.com/rookies-sysu/Management-System-Frontend)

### 9. 其他不确定错误

1. 请检查系统环境配置是否和本仓库部署环境一致

- python3.5
- Docker version 18.03.1-ce, build 9ee9f40
- docker-compose version 1.21.2, build a133471

2. 简单查看[后台测试文档](https://github.com/rookies-sysu/Order-System-Backend/blob/dbpool/tests/README.md)

3. Email 联系仓库维护者 [Johnny Law](https://github.com/longjj).

