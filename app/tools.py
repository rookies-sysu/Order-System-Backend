import pymysql
import json

class Tools:
    def __init__(self, db=None, cursor=None):
        self.db = db
        self.cursor = cursor
    
    def executeSQL(self, sql):
        self.cursor.execute(sql)
        self.db.commit()

    def signIn(self, restaurantName, password):
        sql = """SELECT restaurantID FROM Restaurant
                WHERE restaurantName='%s' AND password='%s' ;""" % (restaurantName, password)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        restaurantID = ''
        for row in results:
            restaurantID = row[0]
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
        self.cursor.execute("SELECT DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%S');")
        results = self.cursor.fetchall()
        now = ''
        for row in results:
            now = row[0]
        return now

    def getTableKeys(self, tableName):
        sql = "SHOW COLUMNS FROM %s" % tableName
        resultSet = []
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                resultSet.append(row[0])
        except:
            print("[ERROR] Table '%s' does not exist." % tableName)
        return resultSet

    def getResults(self, sql, keys):
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        resultSet = []
        for row in results:
            dict_row = {}
            for idx, key in enumerate(keys):
                dict_row[key] = row[idx]
            resultSet.append(dict_row)
        return resultSet
    
    def get_config(self, file_name="config"):
        """Get Configuration"""
        with open(file_name, "r", encoding="utf-8") as f:
            config = json.load(f)
        return 
        
    def getUniqueResult(self, status, result):
        _, result = selectOperator(tableName="Restaurant", restaurantName=restaurantName, result=["restaurantID"])
        self.restaurantID = result[0]["restaurantID"]
        return config