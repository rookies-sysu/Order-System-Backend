import pymysql
from DBUtils.PooledDB import PooledDB
from .dbConfig import *
class DBPool(object):
    __pool = None
    def __init__(self):
        """ Constructed function
        Create database connection and cursor.
        """
        self.coon = DBPool.getMysqlConn()
        self.cur = self.coon.cursor(cursor=pymysql.cursors.DictCursor)

    @staticmethod
    def getMysqlConn():
        """ Get database connection pool.
        Returns:
            __pool.connection(): the database connection pool
        """
        if DBPool.__pool is None:
            __pool = PooledDB(creator=pymysql, mincached=DB_MIN_CACHED , maxcached=DB_MAX_CACHED, 
                              maxshared=DB_MAX_SHARED, maxconnections=DB_MAX_CONNECYIONS, 
                              blocking=DB_BLOCKING, maxusage=DB_MAX_USAGE, 
                              setsession=DB_SET_SESSION,
                              host=DB_HOST , port=DB_PORT , 
                              user=DB_USER , passwd=DB_PASSWORD ,
                              db=DB_DATABASE , charset=DB_CHARSET)
        return __pool.connection()

    def opModify(self, sql):
        """ Insert / Update / Delete Operator
        Args:
            sql: the sql sentence
        Returns:
            insert_num: the number of insert
        """
        insert_num = self.cur.execute(sql)  # execute sql
        self.coon.commit()
        return insert_num

    def opSelect(self, sql):
        """ Select Operator
        Args:
            sql: the sql sentence
        Returns:
            select_res: result in the form of dict
        """
        self.cur.execute(sql)  # 执行sql
        select_res = self.cur.fetchall()  # 返回结果为字典
        return select_res

    def dispose(self):
        """ dispose the connection and close the cursor. """
        self.coon.close()
        self.cur.close()