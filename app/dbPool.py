import pymysql
from DBUtils.PooledDB import PooledDB
import dbConfig as config

class DBPool(object):
    __pool = None
    def __init__(self):
        # 构造函数，创建数据库连接、游标
        self.coon = DBPool.getmysqlconn()
        self.cur = self.coon.cursor(cursor=pymysql.cursors.DictCursor)


    # 数据库连接池连接
    @staticmethod
    def getmysqlconn():
        if DBPool.__pool is None:
            __pool = PooledDB(creator=pymysql, mincached=config.DB_MIN_CACHED , maxcached=config.DB_MAX_CACHED, 
                              maxshared=config.DB_MAX_SHARED, maxconnections=config.DB_MAX_CONNECYIONS, 
                              blocking=config.DB_BLOCKING, maxusage=config.DB_MAX_USAGE, 
                              setsession=config.DB_SET_SESSION,
                              host=config.DB_HOST , port=config.DB_PORT , 
                              user=config.DB_USER , passwd=config.DB_PASSWORD ,
                              db=config.DB_DATABASE , charset=config.DB_CHARSET)
        return __pool.connection()

    # 插入\更新\删除 sql
    def op_modify(self, sql):
        insert_num = self.cur.execute(sql)  # 执行sql
        self.coon.commit()
        return insert_num

    # 查询
    def op_select(self, sql):
        self.cur.execute(sql)  # 执行sql
        select_res = self.cur.fetchall()  # 返回结果为字典
        return select_res

    # 释放资源
    def dispose(self):
        self.coon.close()
        self.cur.close()