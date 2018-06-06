[![Build Status](https://travis-ci.org/rookies-sysu/Order-System-Backend.svg?branch=docker)](https://travis-ci.org/rookies-sysu/Order-System-Backend)

# Order-System-Backend
Order system backend; python3 flask + mysql db

## 部署架构图

![](https://raw.githubusercontent.com/rookies-sysu/Dashboard/master/imgs/deployment_img.png)

目前 nginx 已经上线，并且已经全部部署至云服务器上。

## 目前发现的问题

docker mysql 数据库的初始化需要使用api来进行初始化，不太科学，目前可以work。

`data_import.py` 实际上不能用，景仰需要调试。`data_insert.py` 反而可以，所以应该不是docker部署的锅。

后台的同学们写完 py 代码后麻烦用 autopep8 格式化一下代码，求你们了！orz


** 业务逻辑层和持久化层的链接还是有不通的地方，需要进一步调试，具体部署调试方法看下面 **


## docker build 部署流程

1. 上官网，找资料，安装好 docker
2. 查找 `docker-compose` 的官方文档，安装 `docker-compose`
3. 进入到根目录，运行 `docker-compose up` 进行项目启动，初次运行需要 pull 镜像，耗时稍长
4. 看到如下输出，`db_1` 表示已经准备好接受连接，`web_1` 表示已经准备好接受 request ![](https://raw.githubusercontent.com/rookies-sysu/Dashboard/master/imgs/docker-compose-flask-mysql-res.png)
5. 在浏览器上访问 `localhost:8080/testRedis`， 可以看到 `Hello Tiny-Hippo Backend!! I have been seen 1 times. ` 的字样，表示服务器已经成功work。刷新可以发现 times 前面的数字不断递增，说明 redis 缓冲容器正常运行并连接上了。钟涛接下来要在业务逻辑层对 redis 进行操作实现点菜逻辑。
6. 在浏览器上访问 `http://localhost:8080/insert_fake_data1` ，如果收到 `Good createDB` 消息，说明数据库假数据已经插入。其中，目前只有 `data_insert.py` 这个可以用， `data_importer.py` 不能用，data_importer 调用的 api 为 `http://localhost:8080/insert_fake_data2`. 直接看浏览器返回的错误信息帮助就已经很大。
7. 连接数据库操作： 在终端输入 `mysql -h 172.19.0.1 -P 3306 -u root -p`， 密码是 `tiny-hippo` , 即可以正常连上数据库。注意，`172.19.0.1` 这个ip地址只在 longjj 的本机上适用，这是 docker-compose 给 db 这个容器随机分配的一个地址，如果上述命令连接不上，请上网查一下如何找到一个container的地址。
8. 对于 py 程序代码，直接在本地修改保存后就可以直接在浏览器上测试，因为已经在 docker-compose 中挂载了相关代码文件，可以实时更新容器中的代码，不需要停掉服务器程序。如果需要修改容器中的配置，或者重新 build 容器，需要先 `docker-compose down` 停掉当前正在跑的服务器，再 `docker-compose build {你想要build的容器名(在docker-compose.yml文件中可以看到)}`，再 `docker-compose up` 重启服务器。重新开始调试。
9. 除此之外如果还有其他问题，在群里提出疑问后，先尝试自己解决。
10. 由于持久化层和业务逻辑层都没有做test处理，所以在调试过程中可能需要看一下其他层的工作代码，都了解一下。我写docker帮你们debug已经弄了整整4天了，由衷的感觉到大家要互相看看。
11. 目前的数据库连接方式由于采用直接 sql， 维护成本巨大，而且目前还不能稳稳work，开发任务巨大。考虑一下转 ORM，潘老师也是建议 ORM。**不管用什么技术，保证数据库要work就行。**
12. 业务逻辑层处理客户点餐的逻辑得抓紧时间写了，包括对 redis 的操作，其中可以先忽略掉持久化层的调用，起码得给前端一些反馈。
13. 有什么玄学问题主要看一下各种包的版本。
