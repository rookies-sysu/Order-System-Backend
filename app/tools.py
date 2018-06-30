import pymysql
import json
from dbPool import DBPool as dbPool

class Tools:
    def selectOpt(self, sql):  # 查询
        # 申请资源
        dbpOpt = dbPool()
        results = dbpOpt.op_select(sql)
        # 释放资源
        dbpOpt.dispose()
        return results
    def modifyOpt(self, sql):  # 插入 \ 更新 \ 删除
        # 申请资源
        dbpOpt = dbPool()
        results = dbpOpt.op_modify(sql)
        # 释放资源
        dbpOpt.dispose()
        return results

    def signIn(self, restaurantName, password):
        sql = """SELECT restaurantID FROM Restaurant
                    WHERE restaurantName='%s' AND password='%s' ;""" % (restaurantName, password)
        results = self.selectOpt(sql)
        restaurantID = ''
        for r in results:
            restaurantID = r['restaurantID']
        return restaurantID != ''

    def checkKeysCorrection(self, input, valid_keys):
        for key in input.keys():
            if key not in valid_keys:
                print("[ERROR] Key '%s' does not exist." % key)
                return False
            if key == "result" and not self.checkResultsCorrection(result=input["result"], valid_keys=valid_keys):
                return False
        return True

    def checkResultsCorrection(self, result, valid_keys):
        for key in result:
            if key not in valid_keys:
                print("[ERROR] Key '%s' does not exist." % key)
                return False
        return True

    def getNow(self):
        sql = "SELECT DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%S');"
        results = self.selectOpt(sql)
        now = ''
        for r in results:
            now = r["DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%S')"]
        return now

    def getTableKeys(self, tableName):
        sql = "SHOW COLUMNS FROM %s" % tableName
        resultSet = []
        try:
            results = self.selectOpt(sql)
            for r in results:
                resultSet.append(r['Field'])
        except:
            print("[ERROR] Table '%s' does not exist." % tableName)
        return resultSet
    
    def get_config(self, file_name="config"):
        """Get Configuration"""
        with open(file_name, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
    
    def byte2str(self, results):
        for r in results:
            for key in r.keys():
                if type(r[key]) == type(b'1'):
                    r[key] = r[key].decode('utf8')
        return results