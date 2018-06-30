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

#### 2.2 Docker-compose 一键部署

```bash 
cd Order-System-Backend
docker-compose up -d
```

#### 2.3 测试服务器运行状况

```bash
curl localhost:8080/testRedis
Hello Tiny-Hippo Backend!! I have been seen 1 times.
```

有获得以上响应则说明部署成功。

---

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
