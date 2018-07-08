import pymysql
import json
from .dbPool import DBPool as dbPool

class Tools:
    def selectOpt(self, sql):  # select
        """ Select operator for db connection pool.
        Args:
            sql: sql sentence
            
        Returns:
            the set of results selected by sql
            example:
            [ {restaurantID: 1, restaurantName: 'rName1'},
              {restaurantID: 2, restaurantName: 'rName2'} ]
        """
        # apply connection rescource
        dbp_opt = dbPool()
        results = dbp_opt.opSelect(sql)
        # release connection rescource
        dbp_opt.dispose()
        return results
    def modifyOpt(self, sql):  # insert \ update \ delete
        """ Modify operator for db connection pool.
        Args:
            sql: sql sentence
            
        Returns:
            the result of modifying db
        """
        # apply connection rescource
        dbp_opt = dbPool()
        results = dbp_opt.opModify(sql)
        # release connection rescource
        dbp_opt.dispose()
        return results

    def signIn(self, restaurantName, password):
        """ Sign in with restaurantName & password.
        Args:
            restaurantName: the name of restaurant
            password: the password of restaurant
            
        Returns:
            Whether success to sign in with restaurantName & password.
            example:
                True / False
        """
        sql = """SELECT restaurantID FROM Restaurant
                    WHERE restaurantName='%s' AND password='%s' ;""" % (restaurantName, password)
        results = self.selectOpt(sql)
        restaurantID = ''
        for r in results:
            restaurantID = r['restaurantID']
        return restaurantID != ''

    def checkKeysCorrection(self, input, valid_keys):
        """ Check whether all input keys are included in valid keys.
        Args:
            input: keys of input
            valid_keys: valid keys
            
        Returns:
            Whether all keys of input are included in valid keys.
            example:
                True / False
        """
        for key in input.keys():
            if key not in valid_keys:
                print("[ERROR] Key '%s' does not exist." % key)
                return False
            # check whether all result keys are included in valid keys
            if key == "result" and not self.checkResultsCorrection(result=input["result"], valid_keys=valid_keys):
                return False
        return True

    def checkResultsCorrection(self, result, valid_keys):
        """ Check whether all result keys are included in valid keys.
        Args:
            result: keys of result for selecting
            valid_keys: valid keys
            
        Returns:
            Whether all result keys are included in valid keys.
            example:
                True / False
        """
        for key in result:
            if key not in valid_keys:
                print("[ERROR] Key '%s' does not exist." % key)
                return False
        return True

    def getNow(self):
        """ Get the present time.
        Returns:
            now: the present time in the form of string type
            example:
                2014-04-22 15:47:06
        """
        sql = "SELECT DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%S');"
        results = self.selectOpt(sql)
        now = ''
        for r in results:
            now = r["DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%S')"]
        return now

    def getTableKeys(self, tableName):
        """ Get keys of table with name of table.
        Args:
            tableName: name of table
            
        Returns:
            resultSet: the list of names of all keys of table whose name is the value of 'tableName'
            example:
                ['restaurantID', 'restaurantName', 'password', 'phone', 'email']
        """
        sql = "SHOW COLUMNS FROM %s" % tableName
        resultSet = []
        try:
            results = self.selectOpt(sql)
            for r in results:
                resultSet.append(r['Field'])
        except:
            print("[ERROR] Table '%s' does not exist." % tableName)
        return resultSet
    
    def getConfig(self, file_name="config"):
        """ Get configuration.
        Args:
            file_name: the path of the configuration
            
        Returns:
            config: the json of configuration of database and database connection pool
        """
        with open(file_name, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
