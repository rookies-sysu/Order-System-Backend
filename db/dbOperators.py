import pymysql
from getpass import getpass

# input the secrect of db
# secrect = getpass("Connecting db..\n--> password: ")
# connect to dataset
db = pymysql.connect("localhost", "root", "...", "TINYHIPPO" )
print('success!')
# create a cursor
cursor = db.cursor()

def executeSQL(sql):
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
def signIn(resturantName, password):
    sql = """SELECT resturantID FROM Resturant
               WHERE resturantName='%s' AND password='%s' ;""" % (resturantName, password)
    cursor.execute(sql)
    results = cursor.fetchall()
    resturantID = ''
    for row in results:
        resturantID = row[0]
    return resturantID != ''

def getNow():
    cursor.execute("SELECT DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%S');")
    results = cursor.fetchall()
    now = ''
    for row in results:
        now = row[0]
    return now

def getUniqueResult(sql):
    cursor.execute(sql)
    results = cursor.fetchall()
    result = ''
    for row in results:
        result = row[0]
    return result

def getResultSet(sql):
    cursor.execute(sql)
    results = cursor.fetchall()
    resultSet = []
    for row in results:
        resultSet.append(row[0])
    return resultSet


## -----------------------------------------------------
## Table `TINYHIPPO`.`Resturant`
## -----------------------------------------------------
class resturantOperator():
    def __init__(self, resturantName=None, password=None):
        self.resturantID = None
        self.hasSignedIn = False
        if resturantName != None and password != None:
            self.manageResturantTable(resturantName=resturantName, password=password)

    # Sign in to manage 'Resturant' table
    def manageResturantTable(self, resturantName, password):
        if signIn(resturantName, password):
            self.resturantName = resturantName
            self.password = password
            self.resturantID = self.selectResturantIDWithName(resturantName)
            self.hasSignedIn = True
            print("[SUCCESS] '%s' Sign In!" % resturantName)
        else:
            print('[ERROR] Username is not existed or password is wrong.')
            
    # Insert operator
    def insertResturantItem(self, resturantName, password):
        if not self.identifyResturantName(resturantName):
            sql = """INSERT INTO Resturant(resturantName, password)
                       VALUES ('%s', '%s');""" % (resturantName, password)
            executeSQL(sql)
            print("[SUCCESS] Username '%s' registed." % resturantName)
            self.manageResturantTable(resturantName, password)
        else:
            print("[FAILED] Username '%s' has been registed." % resturantName)

    # Delete operator
    def deleteResturantByID(self, resturantID):
        if self.hasSignedIn:
            if self.identifyResturantID(resturantID):
                self.deleteResturantForeignKey(resturantID)
                ResturantName = self.selectResturantNameWithID(resturantID)
                sql = """DELETE FROM Resturant
                           WHERE resturantID=%d;""" % resturantID
                executeSQL(sql)
                print("[SUCCESS] Username '%s' has been deleted." % ResturantName)
            else:
                print("[FAILED] resturantID '%d' is not existed." % resturantID)
        else:
            print('[FAILED] Please sign in first.')
    def deleteResturantByName(self, resturantName):
        if self.hasSignedIn:
            if self.identifyResturantName(resturantName):
                resturantID = self.selectResturantIDWithName(resturantName)
                self.deleteResturantForeignKey(resturantID)
                self.deleteResturantByID(resturantID)
            else:
                print("[FAILED] Username '%s' is not existed." % resturantName)
        else:
            print('[FAILED] Please sign in first.')
    def deleteResturantForeignKey(self, resturantID):
        # Menu
        mOpt = menuOperator(resturantName=self.resturantName, password=self.password)
        mOpt.deleteMenuByResturantID(resturantID=self.resturantID)
        # DishType
        dtOpt = dishTypeOperator(resturantName=self.resturantName, password=self.password)
        dtOpt.deleteDishTypeByResturantID(resturantID=self.resturantID)
        # Table
        tOpt = tableOperator(resturantName=self.resturantName, password=self.password)
        tOpt.deleteTableByResturantID(resturantID=self.resturantID)

    # Update operator
    def updateResturantName(self, newName):
        if self.hasSignedIn:
            if not self.identifyResturantName(newName):
                sql = """UPDATE Resturant
                           SET resturantName='%s'
                           WHERE resturantName='%s' AND password='%s';""" % (newName, self.resturantName, self.password)
                executeSQL(sql)
                self.resturantName = newName
                print("[SUCCESS] Username has been updated to '%s'." % newName)
            else:
                print("[FAILED] Username '%s' has been registed." % newName)
        else:
            print('[FAILED] Please sign in first.')
    def updateResturantPassword(self, newPassword):
        if self.hasSignedIn:
            sql = """UPDATE Resturant
                       SET password='%s';
                       WHERE resturantName='%s' AND password='%s';""" % (newPassword, self.resturantName, self.password)
            executeSQL(sql)
            self.password = newPassword
            print("[SUCCESS] Password has been updated.")
        else:
            print('[FAILED] Please sign in first.')

    # Select operator
    def selectResturantIDWithName(self, resturantName):
        sql = """SELECT resturantID FROM Resturant
                   WHERE resturantName='%s'""" % (resturantName)
        return getUniqueResult(sql)
    def selectResturantNameWithID(self, resturantID):
        sql = """SELECT resturantName FROM Resturant
                   WHERE resturantID=%d""" % (resturantID)
        return getUniqueResult(sql)

    def identifyResturantName(self, resturantName):
        return self.selectResturantIDWithName(resturantName) != ''
    def identifyResturantID(self, resturantID):
        return self.selectResturantNameWithID(resturantID) != ''

## -----------------------------------------------------
## Table `TINYHIPPO`.`Menu`
## -----------------------------------------------------
class menuOperator:
    def __init__(self, resturantName=None, password=None):
        self.resturantID = None
        self.hasSignedIn = False
        if resturantName != None and password != None:
            self.manageMenuTable(resturantName, password)
    
    # Sign in to manage 'Menu' table
    def manageMenuTable(self, resturantName=None, password=None):
        if signIn(resturantName, password):
            rOpt = resturantOperator()
            self.resturantName = resturantName
            self.password = password
            self.resturantID = rOpt.selectResturantIDWithName(resturantName)
            self.hasSignedIn = True
            print("[SUCCESS] '%s' Sign In!" % resturantName)
        else:
            print('[ERROR] Username is not existed or password is wrong.')

    # Insert operator
    def insertMenuItem(self, menuTitle):
        if self.hasSignedIn:
            if not self.identifyMenuTitle(menuTitle):
                sql = """INSERT INTO Menu(menuTitle, resturantID)
                           VALUES ('%s', %d);""" % (menuTitle, self.resturantID)
                executeSQL(sql)
                print("[SUCCESS] MenuTitle '%s' has been inserted to menu." % menuTitle)
            else:
                print("[FAILED] MenuTitle '%s' has been created." % menuTitle)
        else:
            print('[FAILED] Please sign in first.')

    # Delete operator
    def deleteMenuByID(self, menuID):
        if self.hasSignedIn:
            if self.identifyMenuID(menuID):
                menuTitle = self.selectMenuTitleWithID(menuID)
                sql = """DELETE FROM Menu
                           WHERE menuID=%d;""" % menuID
                executeSQL(sql)
                print("[SUCCESS] MenuTitle '%s' has been deleted." % menuTitle)
            else:
                print("[FAILED] MenuID '%d' is not existed." % menuID)
        else:
            print('[FAILED] Please sign in first.')
    def deleteMenuByTitle(self, menuTitle):
        if self.hasSignedIn:
            if self.identifyMenuTitle(menuTitle):
                sql = """DELETE FROM Menu
                           WHERE resturantID=%d AND menuTitle='%s';""" % (self.resturantID, menuTitle)
                executeSQL(sql)
                print("[SUCCESS] MenuTitle '%s' has been deleted." % menuTitle)
            else:
                print("[FAILED] MenuTitle '%s' is not existed." % menuTitle)
        else:
            print('[FAILED] Please sign in first.')
    def deleteMenuByResturantID(self, resturantID):
        if self.hasSignedIn:
            menuIDs = self.selectMenuIDsWithResturantID(resturantID)
            for menuID in menuIDs:
                self.deleteMenuByID(menuID)
            print("[SUCCESS] Delete all resturantID '%d'." % resturantID)
        else:
            print('[FAILED] Please sign in first.')
    def deleteMenuForeignKey(self, menuID):
        # todo: Dish
        dOpt = dishOperator(self.resturantName, self.password)
        dOpt.deleteDishItemsWithMenuID(menuID)

    # Update operator
    def updateMenuTitle(self, oldTitle, newTitle):
        if self.hasSignedIn:
            if self.identifyMenuTitle(oldTitle):
                if not self.identifyMenuTitle(newTitle):
                    sql = """UPDATE Menu
                               SET menuTitle='%s'
                               WHERE resturantID=%d AND menuTitle='%s';""" % (newTitle, self.resturantID, oldTitle)
                    executeSQL(sql)
                    print("[SUCCESS] MenuTitle has been updated to '%s'." % newTitle)
                else:
                    print("[FAILED] MenuTitle '%s' has been created." % newTitle)
            else:
                print("[ERROR] MenuTitle '%s' is not existed." % oldTitle)
        else:
            print('[FAILED] Please sign in first.')

    # Select operator
    def selectMenuIDWithTitle(self, menuTitle, resturantID):
        sql = """SELECT menuID FROM Menu
                   WHERE resturantID=%d AND menuTitle='%s'""" % (resturantID, menuTitle)
        return getUniqueResult(sql)
    def selectMenuTitleWithID(self, menuID):
        sql = """SELECT menuTitle FROM Menu
                   WHERE menuID=%d""" % (menuID)
        return getUniqueResult(sql)
    def selectResturantIDWithMenuID(self, menuID):
        sql = """SELECT resturantID FROM Menu
                WHERE menuID=%d""" % (menuID)
        return getUniqueResult(sql)
    def selectMenuIDsWithResturantID(self, resturantID):
        sql = """SELECT menuID FROM Menu
                   WHERE resturantID=%d""" % (resturantID)
        return getUniqueResult(sql)

    def identifyMenuTitle(self, menuTitle):
        if self.hasSignedIn:
            return self.selectMenuIDWithTitle(menuTitle, self.resturantID) != ''
        else:
            print('[FAILED] Please sign in first.')
            return False
    def identifyMenuID(self, menuID):
        return self.selectMenuTitleWithID(menuID) != ''

## -----------------------------------------------------
## Table `TINYHIPPO`.`DishType`
## -----------------------------------------------------
class dishTypeOperator:
    def __init__(self, resturantName=None, password=None):
        self.resturantID = None
        self.hasSignedIn = False
        if resturantName != None and password != None:
            self.manageDishTypeTable(resturantName, password)
    
    # Sign in to manage 'DishType' table
    def manageDishTypeTable(self, resturantName=None, password=None):
        if signIn(resturantName, password):
            rOpt = resturantOperator()
            self.resturantName = resturantName
            self.password = password
            self.resturantID = rOpt.selectResturantIDWithName(resturantName)
            self.hasSignedIn = True
            print("[SUCCESS] '%s' Sign In!" % resturantName)
        else:
            print('[ERROR] Username is not existed or password is wrong.')

    # Insert operator
    def insertDishTypeItem(self, dishTypeName):
        if self.hasSignedIn:
            if not self.identifyDishTypeName(dishTypeName, self.resturantID):
                sql = """INSERT INTO DishType(dishTypeName, resturantID)
                           VALUES ('%s', %d);""" % (dishTypeName, self.resturantID)
                executeSQL(sql)
                print("[SUCCESS] DishTypeName '%s' has been inserted to DishType." % dishTypeName)
            else:
                print("[FAILED] DishTypeName '%s' has been created." % dishTypeName)
        else:
            print('[FAILED] Please sign in first.')

    # Delete operator
    def deleteDishTypeByID(self, dishTypeID):
        if self.hasSignedIn:
            if self.identifyDishTypeID(dishTypeID):
                dishTypeName = self.selectDishTypeNameWithID(dishTypeID)
                sql = """DELETE FROM DishType
                        WHERE dishTypeID=%d;""" % dishTypeID
                executeSQL(sql)
                print("[SUCCESS] DishTypeName '%s' has been deleted." % dishTypeName)
            else:
                print("[FAILED] DishTypeID '%d' is not existed." % dishTypeID)
        else:
            print('[FAILED] Please sign in first.')
    def deleteDishTypeByName(self, dishTypeName):
        if self.hasSignedIn:
            if self.identifyDishTypeName(dishTypeName, self.resturantID):
                sql = """DELETE FROM DishType
                        WHERE resturantID=%d AND dishTypeName='%s';""" % (self.resturantID, dishTypeName)
                executeSQL(sql)
                print("[SUCCESS] DishTypeName '%s' has been deleted." % dishTypeName)
            else:
                print("[FAILED] DishTypeName '%s' is not existed." % dishTypeName)
        else:
            print("[ERROR] Username is not existed or password is wrong.")
    def deleteDishTypeByResturantID(self, resturantID):
        if self.hasSignedIn:
            dishTypeIDs = self.selectDishTypeIDsWithResturantID(resturantID)
            for dishTypeID in dishTypeIDs:
                self.deleteDishTypeByID(dishTypeID)
            print("[SUCCESS] Delete all resturantID '%d'." % resturantID)
        else:
            print('[FAILED] Please sign in first.')
    def deleteDishTypeForeignKey(self, dishTypeID):
        # todo: Dish
        dOpt = dishOperator(self.resturantName, self.password)
        dOpt.deleteDishItemsWithDishTypeID(dishTypeID)

    # Update operator
    def updateDishTypeName(self, oldName, newName):
        if self.hasSignedIn:
            if self.identifyDishTypeName(oldName, self.resturantID):
                if not self.identifyDishTypeName(newName, self.resturantID):
                    sql = """UPDATE DishType
                               SET dishTypeName='%s'
                               WHERE resturantID=%d AND dishTypeName='%s';""" % (newName, self.resturantID, oldName)
                    executeSQL(sql)
                    print("[SUCCESS] DishTypeName has been updated to '%s'." % newName)
                else:
                    print("[FAILED] DishTypeName '%s' has been created." % newName)
            else:
                print("[ERROR] DishTypeName '%s' is not existed." % oldName)
        else:
            print('[FAILED] Please sign in first.')

    # select
    def selectDishTypeIDWithName(self, name, resturantID):
        sql = """SELECT dishTypeID FROM DishType
                   WHERE resturantID=%d AND dishTypeName='%s'""" % (resturantID, name)
        return getUniqueResult(sql)
    def selectDishTypeNameWithID(self, ID):
        sql = """SELECT dishTypeName FROM DishType
                   WHERE dishTypeID=%d""" % (ID)
        return getUniqueResult(sql)
    def selectDishTypeIDsWithResturantID(self, resturantID):
        sql = """SELECT dishTypeID FROM DishType
                   WHERE resturantID=%d""" % (resturantID)
        return getUniqueResult(sql)
    def identifyDishTypeName(self, name, resturantID):
        return self.selectDishTypeIDWithName(name, resturantID) != ''
    def identifyDishTypeID(self, ID):
        return self.selectDishTypeNameWithID(ID) != ''

## -----------------------------------------------------
## Table `TINYHIPPO`.`Table`
## -----------------------------------------------------
class tableOperator:
    def __init__(self, resturantName=None, password=None):
        self.resturantID = None
        self.hasSignedIn = False
        if resturantName != None and password != None:
            self.manageTableTable(resturantName, password)
    
    # Sign in to manage 'Table' table
    def manageTableTable(self, resturantName=None, password=None):
        if signIn(resturantName, password):
            rOpt = resturantOperator()
            self.resturantID = rOpt.selectResturantIDWithName(resturantName)
            self.hasSignedIn = True
            print("[SUCCESS] '%s' Sign In!" % resturantName)
        else:
            print('[ERROR] Username is not existed or password is wrong.')
    # Insert operator
    def insertTableItem(self, tableNumber):
        if self.hasSignedIn:
            if not self.identifyTableNumber(tableNumber, self.resturantID):
                sql = """INSERT INTO Table(tableNumber, resturantID)
                           VALUES ('%s', %d);""" % (tableNumber, self.resturantID)
                executeSQL(sql)
                print("[SUCCESS] TableNumber '%d' has been inserted to Table." % tableNumber)
            else:
                print("[FAILED] TableNumber '%d' has been created." % tableNumber)
        else:
            print('[FAILED] Please sign in first.')

    # Delete operator
    def deleteTableByID(self, tableID):
        if self.hasSignedIn:
            if self.identifyTableID(tableID):
                tableNumber = self.selectTableNumberWithID(tableID)
                self.deleteTableForeignKey(tableID)
                sql = """DELETE FROM Table
                        WHERE tableID=%d;""" % tableID
                executeSQL(sql)
                print("[SUCCESS] Table '%d' has been deleted." % tableNumber)
            else:
                print("[FAILED] Table '%d' is not existed." % tableID)
        else:
            print('[FAILED] Please sign in first.')
    def deleteTableByNumber(self, tableNumber):
        if self.hasSignedIn:
            if self.identifyTableNumber(tableNumber, self.resturantID):
                tableID = self.selectTableIDWithNumber(tableNumber, self.resturantID)
                self.deleteTableForeignKey(tableID)
                self.deleteTableByID(tableID)
            else:
                print("[FAILED] TableNumber '%d' is not existed." % tableNumber)
        else:
            print('[FAILED] Please sign in first.')
    def deleteTableByResturantID(self, resturantID):
        if self.hasSignedIn:
            tableIDs = self.selectTableIDsWithResturantID(resturantID)
            for tableID in tableIDs:
                self.deleteTableByID(tableID)
            print("[SUCCESS] Delete all resturantID '%d'." % resturantID)
        else:
            print('[FAILED] Please sign in first.')
    def deleteTableForeignKey(self, tableID):
        # Delete QRlink Items By TableID
        qOpt = QRlinkOperator()
        qOpt.deleteLinkByTableID(tableID)
        # Delete Customer Items By TableID
        cOpt = customerOperator()
        cOpt.deleteCustomerItemsByTableID(tableID)

    # Update operator
    def updateTableByNumber(self, oldNumber, newNumber):
        if self.hasSignedIn:
            if self.identifyTableNumber(oldNumber, self.resturantID):
                if not self.identifyTableNumber(newNumber, self.resturantID):
                    sql = """UPDATE Table
                            SET tableNumber=%d
                            WHERE resturantID=%d AND tableNumber=%d;""" % (newNumber, self.resturantID, oldNumber)
                    executeSQL(sql)
                    print("[SUCCESS] TableNumber has been updated to '%s'." % newNumber)
                else:
                    print("[FAILED] TableNumber '%d' has been created." % newNumber)
            else:
                print("[ERROR] TableNumber '%d' is not existed." % oldNumber)
        else:
            print('[FAILED] Please sign in first.')

    # Select operator
    def selectTableIDWithNumber(self, tableNumber, resturantID):
        sql = """SELECT tableID FROM Table
                   WHERE resturantID=%d AND tableNumber=%d""" % (resturantID, tableNumber)
        return getUniqueResult(sql)
    def selectTableNumberWithID(self, tableID):
        sql = """SELECT tableNumber FROM Table
                   WHERE tableID=%d""" % (tableID)
        return getUniqueResult(sql)
    def selectTableIDsWithResturantID(self, resturantID):
        sql = """SELECT tableID FROM Table
                   WHERE resturantID=%d""" % (resturantID)
        return getResultSet(sql)
    def identifyTableNumber(self, number, resturantID):
        return self.selectTableIDWithNumber(number, resturantID) != ''
    def identifyTableID(self, tableID):
        return self.selectTableNumberWithID(tableID) != ''

## -----------------------------------------------------
## Table `TINYHIPPO`.`QRlink`
## -----------------------------------------------------
class QRlinkOperator:
    def __init__(self, resturantName=None, password=None):
        self.resturantID = None
        self.hasSignedIn = False
        if resturantName != None and password != None:
            self.manageQRlinkTable(resturantName, password)
    
    # Sign in to manage 'QRlink' table
    def manageQRlinkTable(self, resturantName=None, password=None):
        if signIn(resturantName, password):
            rOpt = resturantOperator()
            self.resturantID = rOpt.selectResturantIDWithName(resturantName)
            self.hasSignedIn = True
            print("[SUCCESS] '%s' Sign In!" % resturantName)
        else:
            print('[ERROR] Username is not existed or password is wrong.')
    # Insert operator
    def insertQRlinkItem(self, linkImageURL, tableNumber):
        if self.hasSignedIn:
            tOpt = tableOperator()
            tableID = tOpt.selectTableIDWithNumber(tableNumber, self.resturantID)
            if not self.identifyLinkImageURL(linkImageURL):
                sql = """INSERT INTO QRlink(linkImageURL, tableID)
                           VALUES ('%s', %d);""" % (linkImageURL, tableID)
                executeSQL(sql)
                print("[SUCCESS] linkImageURL '%s' has been inserted to DishType." % linkImageURL)
            else:
                print("[FAILED] linkImageURL '%s' has been created." % linkImageURL)
        else:
            print('[FAILED] Please sign in first.')

    # Delete operator
    def deleteLinkByID(self, linkID):
        if self.hasSignedIn:
            if self.identifyLinkID(linkID):
                tableID = self.selectTableIDWithLinkID(linkID)
                tOpt = tableOperator()
                tableNumber = tOpt.selectTableNumberWithID(tableID)
                sql = """DELETE FROM QRlink
                           WHERE linkID=%d AND tableID=%d;""" % (linkID, tableID)
                executeSQL(sql)
                print("[SUCCESS] The QRlink of Table '%d' has been deleted." % tableNumber)
            else:
                print("[FAILED] LinkID '%d' is not existed." % linkID)
        else:
            print('[FAILED] Please sign in first.')
    def deleteLinkByURL(self, linkImageURL):
        if self.hasSignedIn:
            if self.identifyLinkImageURL(linkImageURL):
                linkID = self.selectURLWithID(linkImageURL)
                self.deleteLinkByID(linkID)
            else:
                print("[FAILED] linkImageURL '%s' is not existed." % linkImageURL)
        else:
            print('[FAILED] Please sign in first.')
    def deleteLinkByTableID(self, tableID):
        if self.hasSignedIn:
            sql = """DELETE FROM QRlink
                       WHERE tableID=%d;""" % tableID
            executeSQL(sql)
            print("[SUCCESS] Delete tableID '%d'." % tableID)
        else:
            print('[FAILED] Please sign in first.')

    # Update operator
    def updateLinkImageURL(self, oldURL, newURL):
        if self.hasSignedIn:
            if self.identifyLinkImageURL(oldURL):
                if not self.identifyLinkImageURL(newURL):
                    sql = """UPDATE DishType
                               SET linkImageURL='%s'
                               WHERE linkImageURL='%s';""" % (newURL, oldURL)
                    executeSQL(sql)
                    print("[SUCCESS] LinkImageURL has been updated to '%s'." % newURL)
                else:
                    print("[FAILED] LinkImageURL '%s' has been created." % newURL)
            else:
                print("[ERROR] LinkImageURL '%s' is not existed." % oldURL)
        else:
            print('[FAILED] Please sign in first.')
    def updateTableID(self, oldTableID, newTableID):
        if self.hasSignedIn:
            linkID = self.selectLinkIDWithTableID(oldTableID)
            if self.identifyLinkID(linkID):
                linkID = self.selectLinkIDWithTableID(newTableID)
                if not self.identifyLinkID(linkID):
                    sql = """UPDATE QRlink
                               SET tableID='%s'
                               WHERE tableID='%s';""" % (newTableID, oldTableID)
                    executeSQL(sql)
                    print("[SUCCESS] Table ID has been updated to '%d'." % newTableID)
                else:
                    print("[FAILED] Table ID '%d' has been created." % newTableID)
            else:
                print("[ERROR] LinkImageURL '%d' is not existed." % oldTableID)
        else:
            print('[FAILED] Please sign in first.')

    # Select operator
    def selectLinkIDWithURL(self, linkImageURL):
        sql = """SELECT linkID FROM QRlink
                   WHERE linkImageURL='%s'""" % (linkImageURL)
        return getUniqueResult(sql)
    def selectURLWithID(self, linkID):
        sql = """SELECT linkImageURL FROM QRlink
                   WHERE linkID=%d""" % (linkID)
        return getUniqueResult(sql)
    def selectLinkIDWithTableID(self, tableID):
        sql = """SELECT linkID FROM QRlink
                   WHERE tableID=%d""" % (tableID)
        return getUniqueResult(sql)
    def selectTableIDWithLinkID(self, linkID):
        sql = """SELECT tableID FROM QRlink
                   WHERE linkID=%d""" % (linkID)
        return getUniqueResult(sql)
    def identifyLinkImageURL(self, linkImageURL):
        return self.selectLinkIDWithURL(linkImageURL) != ''
    def identifyLinkID(self, linkID):
        return self.selectURLWithID(linkID) != ''

## -----------------------------------------------------
## Table `TINYHIPPO`.`Edit`
## -----------------------------------------------------
class editOperator:
    # Insert operator
    def insertEditItem(self, customerID=0, orderID=0):
        if customerID != 0 or orderID != 0:
            if not self.identifyEditItem(customerID, orderID):
                now = getNow()
                sql = """INSERT INTO Edit(customerID, orderID, editedTime)
                            VALUES (%d, %d, '%s');""" % (customerID, orderID, now)
                executeSQL(sql)
                print("[SUCCESS] customerID '%d' and orderID '%d' has been inserted to Edit at '%s'." % (customerID, orderID, now))
            else:
                print("[FAILED] customerID '%d' and orderID '%d' has been created." % (customerID, orderID))
        else:
            print("[ERROR] Input information is not enough.")
    
    # Delete operator
    def deleteEditItemByCustomerIDAndOrderID(self, customerID, orderID):
        if self.identifyEditItem(customerID, orderID):
            self.deleteCustomerForeignKey(customerID)
            self.deleteOrderForeignKey(orderID)
            sql = """"DELETE FROM Edit
                        WHERE customerID=%d AND orderID=%d;""" % (customerID, orderID)
            executeSQL(sql)
            print("[SUCCESS] Delete Edit item which stored customerID '%d' and orderID '%d'." % (customerID, orderID))
        else:
            print("[FAILED] There is no Edit item which stored customerID '%d' and orderID '%d'." % (customerID, orderID))
    def deleteEditItemByCustomerID(self, customerID):
        orderIDs = self.selectOrderIDsWithCustomerID(customerID)
        if not orderIDs:
            for orderID in orderIDs:
                self.deleteEditItemByCustomerIDAndOrderID(customerID, orderID)
            print("[SUCCESS] Delete all Edit items which stored customerID '%d'." % customerID)
        else:
            print("[FAILEpassD] There is no Edit item which stored customerID '%d'." % customerID)
    def deleteEditItemByOrderID(self, orderID):
        customerIDs = self.selectCustomerIDsWithOrderID(orderID)
        if not customerIDs:
            for customerID in customerIDs:
                self.deleteEditItemByCustomerIDAndOrderID(customerID, orderID)
            print("[SUCCESS] Delete all Edit items which stored orderID '%d'." % orderID)
        else:
            print("[FAILED] There is no Edit item which stored orderID '%d'." % orderID)
    
    def deleteCustomerForeignKey(self, customerID):
        # todo: order operator
        # delete Order By customerID
        oOpt = orderOperator()
        oOpt.deleteOrderItemsWithCustomerID(customerID)

    def deleteOrderForeignKey(self, orderID):
        # delete Customer By orderID
        cOpt = customerOperator()
        cOpt.deleteCustomerItemsByOrderID(orderID)

    # Update operator
    def updateEditedTime(self, customerID, orderID):
        if self.identifyEditItem(customerID, orderID):
            now = getNow()
            sql = """"UPDATE Edit
                        SET editedTime='%s'
                        WHERE customerID=%d AND orderID=%d;""" % (now, customerID, orderID)
            executeSQL(sql)
            print("[SUCCESS] The Edit item has updated at '%s'. [customerID '%d' and orderID '%d']" % (now, customerID, orderID))
        else:
            print("[FAILED] There is no Edit item which stored customerID '%d' and orderID '%d'." % (customerID, orderID))
    def updateCustomerID(self, newCustomerID, oldCustomerID, orderID):
        if self.identifyEditItem(oldCustomerID, orderID):
            sql = """"UPDATE Edit
                        SET customerID=%d
                        WHERE customerID=%d AND orderID=%d;""" % (newCustomerID, oldCustomerID, orderID)
            executeSQL(sql)
            print("[SUCCESS] The Edit item has updated. [customerID '%d' and orderID '%d']" % (newCustomerID, orderID))
        else:
            print("[FAILED] There is no Edit item which stored customerID '%d' and orderID '%d'." % (oldCustomerID, orderID))
    def updateOrderID(self, customerID, newOrderID, OldOrderID):
        if self.identifyEditItem(customerID, OldOrderID):
            sql = """"UPDATE Edit
                        SET orderID=%d
                        WHERE customerID=%d AND orderID=%d;""" % (newOrderID, customerID, OldOrderID)
            executeSQL(sql)
            print("[SUCCESS] The Edit item has updated. [customerID '%d' and orderID '%d']" % (customerID, newOrderID))
        else:
            print("[FAILED] There is no Edit item which stored customerID '%d' and orderID '%d'." % (customerID, OldOrderID))

    # Select operator
    def selectCustomerIDsWithOrderID(self, orderID):
        sql = """SELECT customerID FROM Edit
                   WHERE orderID=%d""" % (orderID)
        return getResultSet(sql)
    def selectOrderIDsWithCustomerID(self, customerID):
        sql = """SELECT orderID FROM Edit
                   WHERE customerID=%d""" % (customerID)
        return getResultSet(sql)
    def selectEditedTimeWithCustomerIDAndOrderID(self, customerID, orderID):
        sql = """SELECT editedTime FROM Edit
                   WHERE customerID=%d AND orderID=%d""" % (customerID, orderID)
        return getUniqueResult(sql)

    def identifyEditItem(self, customerID, orderID):
        return self.selectEditedTimeWithCustomerIDAndOrderID(customerID, orderID) != ''
    def identifyEditItemWithCustomerID(self, customerID):
        return self.selectOrderIDsWithCustomerID(customerID) != []
    def identifyEditItemWithOrderID(self, orderID):
        return self.selectCustomerIDsWithOrderID(orderID) != []

## -----------------------------------------------------
## Table `TINYHIPPO`.`Customer`
## -----------------------------------------------------
class customerOperator:
    def __init__(self, customerID=0, orderID=0, tableID=0):
        self.customerID = customerID
        self.orderID = orderID
        self.tableID = tableID
    # Insert operator
    def insertCustomerItem(self, customerName, orderID, tableID):
        if not self.identifyCustomerName(customerName):
            sql = """INSERT INTO Customer(customerName, orderID, tableID)
                       VALUES ('%s', %d, %d);""" % (customerName, orderID, tableID)
            executeSQL(sql)
            print("[SUCCESS] customerName '%s' has been inserted to Table ''." % customerName)
        else:
            print("[FAILED] customerName '%s' has been created." % customerName)
    
    # Delete operator
    def deleteCustomerItemByCustomerID(self, customerID):
        if self.identifyCustomerID(customerID):
            customerName = self.selectCustomerNameWithID(customerID)
            sql = """DELETE FROM Customer
                       WHERE customerID=%d;""" % customerID
            executeSQL(sql)
            print("[SUCCESS] The Customer '%s' has been deleted." % customerName)
        else:
            print("[FAILED] CustomerID '%d' is not existed." % customerID)
    def deleteCustomerItemByCustomerName(self, customerName):
        if self.identifyCustomerName(customerName):
            customerID = self.selectCustomerIDWithName(customerName)
            self.deleteCustomerItemByCustomerID(customerID)
        else:
            print("[FAILED] customerName '%s' is not existed." % customerName)
    def deleteCustomerItemsByTableID(self, tableID):
        if self.identifyTableID(tableID):
            customerIDs = self.selectCustomerIDsWithTableID(tableID)
            for customerID in customerIDs:
                self.deleteCustomerItemByCustomerID(customerID)
            print("[SUCCESS] All Customers eat on TableID '%d' has been deleted." % tableID)
        else:
            print("[ERROR] There is no TableID '%d'." % tableID)
    def deleteCustomerItemsByOrderID(self, orderID):
        if self.identifyOrderID(orderID):
            customerIDs = self.selectCustomerIDsWithOrderID(orderID)
            for customerID in customerIDs:
                self.deleteCustomerItemByCustomerID(customerID)
            print("[SUCCESS] All Customers edit OrderID '%d' has been deleted." % orderID)
        else:
            print("[ERROR] There is no OrderID '%d'." % orderID)

    # Update operator
    def updateCustomerName(self, oldCustomerName, newCustomerName):
        if self.identifyCustomerName(oldCustomerName):
            sql = """"UPDATE Customer
                        SET customerName='%s'
                        WHERE customerName='%s';""" % (newCustomerName, oldCustomerName)
            executeSQL(sql)
            print("[SUCCESS] The CustomerName has updated to '%s'." % newCustomerName)
        else:
            print("[FAILED] CustomerName '%s' is not existed." % oldCustomerName)
    def updateOrderIDWithCustomerName(self, customerName, oldOrderID, newOrderID):
        if self.identifyCustomerName(customerName):
            if self.identifyOrderID(oldOrderID):
                sql = """"UPDATE Customer
                            SET orderID=%d
                            WHERE customerName='%s' AND orderID=%d;""" % (newOrderID, customerName, oldOrderID)
                executeSQL(sql)
                print("[SUCCESS] The OrderID of Customer '%s' has updated to '%d'." % (customerName, newOrderID))
            else:
                print("[FAILED] OrderID '%d' is not existed." % oldOrderID)
        else:
            print("[FAILED] CustomerName '%s' is not existed." % customerName)
    def updateTableIDWithCustomerName(self, customerName, oldTableID, newTableID):
        if self.identifyCustomerName(customerName):
            if self.identifyTableID(oldTableID):
                sql = """"UPDATE Customer
                            SET tableID=%d
                            WHERE customerName='%s' AND tableID=%d;""" % (newTableID, customerName, oldTableID)
                executeSQL(sql)
                print("[SUCCESS] The TableID of Customer '%s' has updated to '%d'." % (customerName, newTableID))
            else:
                print("[FAILED] TableID '%d' is not existed." % oldTableID)
        else:
            print("[FAILED] CustomerName '%s' is not existed." % customerName)

    # Select operator
    def selectCustomerIDWithName(self, customerName):
        sql = """SELECT customerID FROM Customer
                   WHERE customerName='%s'""" % customerName
        return getUniqueResult(sql)
    def selectCustomerNameWithID(self, customerID):
        sql = """SELECT customerName FROM Customer
                   WHERE customerID=%d""" % customerID
        return getUniqueResult(sql)
    def selectCustomerIDsWithTableID(self, tableID):
        sql = """SELECT customerID FROM Customer
                   WHERE tableID=%d""" % tableID
        return getResultSet(sql)
    def selectCustomerIDsWithOrderID(self, orderID):
        sql = """SELECT customerID FROM Customer
                   WHERE orderID=%d""" % orderID
        return getResultSet(sql)

    def identifyCustomerName(self, customerName):
        return self.selectCustomerIDWithName(customerName) != ''
    def identifyCustomerID(self, customerID):
        return self.selectCustomerNameWithID(customerID) != ''
    def identifyTableID(self, tableID):
        return self.selectCustomerIDsWithTableID(tableID) != []
    def identifyOrderID(self, orderID):
        return self.selectCustomerIDsWithOrderID(orderID) != []

## -----------------------------------------------------
## Table `TINYHIPPO`.`Order`
## -----------------------------------------------------
class orderOperator:
    # Insert operator
    def insertOrderItem(self, orderDishes='', total=0, customerName=''):
        '''
        Input:
            orderDishes: the json of dishes in the order
            total: the total of the order
            customerName: The name of customer who edit the order
        '''
        # initialize param
        status = 'todo'
        isPaid = 'False'
        # get customerID
        cOpt = customerOperator()
        customerID = cOpt.selectCustomerIDWithName(customerName)
        if self.selectUndoneOrderIDWithCustomerID(customerID) == '':
            sql = """INSERT INTO Order(orderDishes, status, total, isPaid, customerID)
                       VALUES ('%s', '%s', %f, '%s', %d);""" % (orderDishes, status, total, isPaid, customerID)
            executeSQL(sql)
            print("[SUCCESS] A new Order has been inserted to Table.")
            orderID = self.selectUndoneOrderIDWithCustomerID(customerID)
            eOpt = editOperator()
            eOpt.insertEditItem(customerID=customerID, orderID=orderID)
        else:
            print("[FAILED] CustomerID '%s' is not existed.")

    # Delete operator
    def deleteOrderItemWithOrderID(self, orderID):
        if self.identifyOrderID(orderID):
            sql = """DELETE FROM Order
                       WHERE orderID=%d;""" % orderID
            executeSQL(sql)
            print("[SUCCESS] The OrderID '%d' has been deleted." % orderID)
        else:
            print("[FAILED] OrderID '%d' is not existed." % orderID)
    def deleteOrderItemsWithCustomerID(self, customerID):
        if self.identifyCustomerID(customerID):
            sql = """DELETE FROM Order
                       WHERE customerID=%d;""" % customerID
            executeSQL(sql)
            print("[SUCCESS] All OrderItems of CustomerID '%d' has been deleted." % customerID)
        else:
            print("[FAILED] CustomerID '%d' is not existed." % customerID)

    # Update operator
    def updateOrderDishes(self, newOrderDishes, total, orderID, customerID):
        if self.identifyOrderID(orderID):
            if self.identifyCustomerID(customerID):
                self.updateTotal(total, orderID, customerID)
                sql = """"UPDATE Order
                            SET orderDishes='%s'
                            WHERE orderID=%d AND customerID=%d;""" % (newOrderDishes, orderID, customerID)
                executeSQL(sql)
                print("[SUCCESS] The orderDishes of OrderID '%d' has been updated." % (orderID))
            else:
                print("[ERROR] CustomerID '%d' is not existed." % customerID)
        else:
            print("[ERROR] OrderID '%d' is not existed." % orderID)

    def updateTotal(self, total, orderID, customerID):
        if self.identifyOrderID(orderID):
            if self.identifyCustomerID(customerID):
                sql = """"UPDATE Order
                            SET total=%f
                            WHERE orderID=%d AND customerID=%d;""" % (total, orderID, customerID)
                executeSQL(sql)
                print("[SUCCESS] The total of OrderID '%d' has been updated to '%.2f'." % (orderID, total))
            else:
                print("[ERROR] CustomerID '%d' is not existed." % customerID)
        else:
            print("[ERROR] OrderID '%d' is not existed." % orderID)
    
    def updateStatusToDone(self, orderID, customerID):
        if self.identifyOrderID(orderID):
            if self.identifyCustomerID(customerID):
                if self.selectIsPaid(orderID, customerID) == 'True':
                    status = 'done'
                    sql = """"UPDATE Order
                                SET status='%s'
                                WHERE orderID=%d AND customerID=%d;""" % (status, orderID, customerID)
                    executeSQL(sql)
                    print("[SUCCESS] The Status of OrderID '%d' has been updated to '%s'." % (orderID, status))
                else:
                    print("[FAILED] The order has not been paid.")
            else:
                print("[ERROR] CustomerID '%d' is not existed." % customerID)
        else:
            print("[ERROR] OrderID '%d' is not existed." % orderID)

    def updateIsPaid(self, orderID, customerID):
        if self.identifyOrderID(orderID):
            if self.identifyCustomerID(customerID):
                if self.selectIsPaid(orderID, customerID) == 'False':
                    status = 'doing'
                    isPaid = 'True'
                    sql = """"UPDATE Order
                                SET status='%s', isPaid='%s'
                                WHERE orderID=%d AND customerID=%d;""" % (status, isPaid, orderID, customerID)
                    executeSQL(sql)
                    print("[SUCCESS] The OrderID '%d' has been paid and dishes is '%s'." % (orderID, status))
                else:
                    print("[FAILED] The OrderID '%d' has been paid.")
            else:
                print("[ERROR] CustomerID '%d' is not existed." % customerID)
        else:
            print("[ERROR] OrderID '%d' is not existed." % orderID)

    # Select operator
    def selectStatus(self, orderID, customerID):
        sql = """SELECT status FROM Order
                   WHERE orderID=%d AND customerID=%d;""" % (orderID, customerID)
        return getUniqueResult(sql)
    def selectTotal(self, orderID, customerID):
        sql = """SELECT total FROM Order
                   WHERE orderID=%d AND customerID=%d;""" % (orderID, customerID)
        return getUniqueResult(sql)
    def selectIsPaid(self, orderID, customerID):
        sql = """SELECT isPaid FROM Order
                   WHERE orderID=%d AND customerID=%d;""" % (orderID, customerID)
        return getUniqueResult(sql)

    def selectOrderIDsWithCustomerID(self, customerID):
        sql = """SELECT orderID FROM Order
                   WHERE customerID=%d""" % customerID
        return getResultSet(sql)
    def selectCustomerIDsWithOrderID(self, orderID):
        sql = """SELECT customerID FROM Order
                   WHERE orderID=%d""" % orderID
        return getResultSet(sql)

    def selectUndoneOrderIDWithCustomerID(self, customerID):
        '''
        select Order whose status is 'todo' or 'doing' with CustomerID
        '''
        orderIDs = self.selectOrderIDsWithCustomerID(customerID)
        for orderID in orderIDs:
            sql = """SELECT orderID FROM Order
                       WHERE orderID=%d AND (status='%s' OR status='%s') ;""" % (orderID, 'todo', 'doing')
            result = getUniqueResult(sql)
            if result != '':
                return result
        return ''

    def identifyCustomerID(self, customerID):
        return self.selectOrderIDsWithCustomerID(customerID) != ''
    def identifyOrderID(self, orderID):
        return self.selectCustomerIDsWithOrderID(orderID) != []
    

## -----------------------------------------------------
## Table `TINYHIPPO`.`Dish`
## -----------------------------------------------------
class dishOperator:
    def __init__(self, resturantName=None, password=None):
        self.resturantID = None
        self.hasSignedIn = False
        if resturantName != None and password != None:
            self.manageDishTable(resturantName, password)

    # Sign in to manage 'Resturant' table
    def manageDishTable(self, resturantName=None, password=None):
        if signIn(resturantName, password):
            rOpt = resturantOperator(resturantName, password)
            self.resturantID = rOpt.selectResturantIDWithName(resturantName)
            self.hasSignedIn = True
            print("[SUCCESS] '%s' Sign In!" % resturantName)
        else:
            print('[ERROR] Username is not existed or password is wrong.')

    # Insert operator
    def insertDishItem(self, dishName='', price=0, dishImageURL='', dishComment='', dishHot=0, monthlySales=0, dishTypeName='', menuTitle=''):
        if self.hasSignedIn:
            # get dishTypeID
            dtOpt = dishTypeOperator()
            dishTypeID = dtOpt.selectDishTypeIDWithName(dishTypeName, self.resturantID)
            # get menuID
            mOpt = menuOperator()
            menuID = mOpt.selectMenuIDWithTitle(menuTitle, self.resturantID)
            if self.identifyDishName(dishName, menuID):
                sql = """INSERT INTO Dish(dishName, price, dishImageURL, dishComment, dishHot, monthlySales, dishTypeID, menuID)
                           VALUES ('%s', %d, '%s', '%s', %d, %d, %d, %d, %d);""" % (dishName, price, dishImageURL, dishComment, dishHot, monthlySales, dishTypeID, menuID)
                executeSQL(sql)
                print("[SUCCESS] A new Dish '%s' has been inserted." % dishName)
            else:
                print("[FAILED] DishName '%s' has been created in Menu '%s'" % (dishName, menuTitle))
        else:
            print('[FAILED] Please sign in first.')
    
    # Delete operator
    def deleteDishItemWithDishID(self, dishID):
        if self.hasSignedIn:
            menuID = self.selectMenuIDWithDishID(dishID)
            if self.identifyDishID(dishID, menuID):
                dishName = self.selectDishNameWithDishID(dishID, menuID)
                sql = """DELETE FROM Dish
                           WHERE dishID=%d;""" % dishID
                executeSQL(sql)
                print("[SUCCESS] The Dish '%s' has been deleted." % dishName)
            else:
                print("[FAILED] DishID '%d' is not existed." % dishID)
        else:
            print('[FAILED] Please sign in first.')
    def deleteDishItemsWithMenuID(self, menuID):
        if self.hasSignedIn:
            dishIDs = self.selectDishIDsWithMenuID(menuID)
            if dishIDs != []:
                # get menuID
                mOpt = menuOperator()
                menuTitle = mOpt.selectMenuTitleWithID(menuID)
                for dishID in dishIDs:
                    self.deleteDishItemWithDishID(dishID)
                print("[SUCCESS] All Dishes in Menu '%s' have been deleted." % menuTitle)
            else:
                print("[FAILED] There is no dish in Menu '%d'." % menuID)
        else:
            print('[FAILED] Please sign in first.')
    def deleteDishItemsWithDishTypeID(self, dishTypeID):
        if self.hasSignedIn:
            dishIDs = self.selectDishIDsWithDishTypeID(dishTypeID)
            if dishIDs != []:
                # get menuID
                dtOpt = dishTypeOperator()
                dishTypeName = dtOpt.selectDishTypeNameWithID(dishTypeID)
                for dishID in dishIDs:
                    self.deleteDishItemWithDishID(dishID)
                print("[SUCCESS] All Dishes in DishType '%s' have been deleted." % dishTypeName)
            else:
                print("[FAILED] There is no dish in DishType '%d'." % dishTypeID)
        else:
            print('[FAILED] Please sign in first.')
    
    # Update operator
    def updateDishName(self, oldDishName, newDishName, menuTitle):
        if self.hasSignedIn:
            # get menuID
            mOpt = menuOperator()
            menuID = mOpt.selectMenuIDWithTitle(menuTitle, self.resturantID)
            if self.identifyDishName(oldDishName, menuID):
                sql = """"UPDATE Dish
                            SET dishName='%s'
                            WHERE dishName='%s' AND menuID=%d;""" % (menuTitle, oldDishName, menuID)
                executeSQL(sql)
                print("[SUCCESS] The DishName has updated to '%s'." % newDishName)
            else:
                print("[FAILED] DishName '%s' is not existed in Menu '%s'." % (oldDishName, menuTitle))
        else:
            print('[FAILED] Please sign in first.')
    def updatePrice(self, newPrice, dishName, menuTitle):
        if self.hasSignedIn:
            # get menuID
            mOpt = menuOperator()
            menuID = mOpt.selectMenuIDWithTitle(menuTitle, self.resturantID)
            # get dishID
            dishID = self.selectDishIDWithDishName(dishName, menuID)
            if self.identifyDishName(dishName, menuID):
                sql = """"UPDATE Dish
                            SET price=%f
                            WHERE dishID=%d AND menuID=%d;""" % (newPrice, dishID, menuID)
                executeSQL(sql)
                print("[SUCCESS] The price of Dish '%s' in Menu '%s' has updated to %.2f." % (dishName, menuTitle, newPrice))
            else:
                print("[FAILED] DishName '%s' is not existed in Menu '%s'." % (dishName, menuTitle))
        else:
            print('[FAILED] Please sign in first.')
    def updateDishImageURL(self, newDishImageURL, dishName, menuTitle):
        if self.hasSignedIn:
            # get menuID
            mOpt = menuOperator()
            menuID = mOpt.selectMenuIDWithTitle(menuTitle, self.resturantID)
            # get dishID
            dishID = self.selectDishIDWithDishName(dishName, menuID)
            if self.identifyDishName(dishName, menuID):
                sql = """"UPDATE Dish
                            SET dishImageURL='%s'
                            WHERE dishID=%d AND menuID=%d;""" % (newDishImageURL, dishID, menuID)
                executeSQL(sql)
                print("[SUCCESS] The ImageURL of Dish '%s' in Menu '%s' has updated to '%s'." % (dishName, menuTitle, newDishImageURL))
            else:
                print("[FAILED] DishName '%s' is not existed in Menu '%s'." % (dishName, menuTitle))
        else:
            print('[FAILED] Please sign in first.')
    def updateDishComment(self, newDishComment, dishName, menuTitle):
        if self.hasSignedIn:
            # get menuID
            mOpt = menuOperator()
            menuID = mOpt.selectMenuIDWithTitle(menuTitle, self.resturantID)
            # get dishID
            dishID = self.selectDishIDWithDishName(dishName, menuID)
            if self.identifyDishName(dishName, menuID):
                sql = """"UPDATE Dish
                            SET dishComment='%s'
                            WHERE dishID=%d AND menuID=%d;""" % (newDishComment, dishID, menuID)
                executeSQL(sql)
                print("[SUCCESS] The Comment of Dish '%s' in Menu '%s' has updated to '%s'." % (dishName, menuTitle, newDishComment))
            else:
                print("[FAILED] DishName '%s' is not existed in Menu '%s'." % (dishName, menuTitle))
        else:
            print('[FAILED] Please sign in first.')
    def updateDishHot(self, newDishHot, dishName, menuTitle):
        if self.hasSignedIn:
            # get menuID
            mOpt = menuOperator()
            menuID = mOpt.selectMenuIDWithTitle(menuTitle, self.resturantID)
            # get dishID
            dishID = self.selectDishIDWithDishName(dishName, menuID)
            if self.identifyDishName(dishName, menuID):
                sql = """"UPDATE Dish
                            SET dishHot=%d
                            WHERE dishID=%d AND menuID=%d;""" % (newDishHot, dishID, menuID)
                executeSQL(sql)
                print("[SUCCESS] The Hot of Dish '%s' in Menu '%s' has updated to '%d'." % (dishName, menuTitle, newDishHot))
            else:
                print("[FAILED] DishName '%s' is not existed in Menu '%s'." % (dishName, menuTitle))
        else:
            print('[FAILED] Please sign in first.')
    def updateMonthlySales(self, newMonthlySales, dishName, menuTitle):
        if self.hasSignedIn:
            # get menuID
            mOpt = menuOperator()
            menuID = mOpt.selectMenuIDWithTitle(menuTitle, self.resturantID)
            # get dishID
            dishID = self.selectDishIDWithDishName(dishName, menuID)
            if self.identifyDishName(dishName, menuID):
                sql = """"UPDATE Dish
                            SET monthlySales=%d
                            WHERE dishID=%d AND menuID=%d;""" % (newMonthlySales, dishID, menuID)
                executeSQL(sql)
                print("[SUCCESS] The Monthly Sales of Dish '%s' in Menu '%s' has updated to '%d'." % (dishName, menuTitle, newMonthlySales))
            else:
                print("[FAILED] DishName '%s' is not existed in Menu '%s'." % (dishName, menuTitle))
        else:
            print('[FAILED] Please sign in first.')
    
    # Select operator
    def selectPriceWithDishID(self, dishID):
        sql = """SELECT price FROM Dish
                   WHERE dishID=%d""" % dishID
        return getUniqueResult(sql)
    def selectDishImageURLWithDishID(self, dishID):
        sql = """SELECT dishImageURL FROM Dish
                   WHERE dishID=%d""" % dishID
        return getUniqueResult(sql)
    def selectDishCommentWithDishID(self, dishID):
        sql = """SELECT dishComment FROM Dish
                   WHERE dishID=%d""" % dishID
        return getUniqueResult(sql)
    def selectDishHotWithDishID(self, dishID):
        sql = """SELECT dishHot FROM Dish
                   WHERE dishID=%d""" % dishID
        return getUniqueResult(sql)
    def selectMonthlySalesWithDishID(self, dishID):
        sql = """SELECT monthlySales FROM Dish
                   WHERE dishID=%d""" % dishID
        return getUniqueResult(sql)

    def selectDishIDWithDishName(self, dishName, menuID):
        sql = """SELECT dishID FROM Dish
                   WHERE menuID=%d AND dishName='%s'""" % (menuID, dishName)
        return getUniqueResult(sql)
    def selectDishNameWithDishID(self, dishID, menuID):
        sql = """SELECT dishName FROM Dish
                   WHERE menuID=%d AND dishID=%d""" % (menuID, dishID)
        return getUniqueResult(sql)
    def selectMenuIDWithDishID(self, dishID):
        sql = """SELECT menuID FROM Dish
                   WHERE dishID=%d""" % dishID
        return getUniqueResult(sql)
    def selectDishIDsWithMenuID(self, menuID):
        sql = """SELECT dishID FROM Dish
                   WHERE menuID=%d""" % menuID
        return getResultSet(sql)
    def selectDishIDsWithDishTypeID(self, dishTypeID):
        sql = """SELECT dishID FROM Dish
                   WHERE dishTypeID=%d""" % dishTypeID
        return getResultSet(sql)
    def identifyDishID(self, dishID, menuID):
        return self.selectDishNameWithDishID(dishID, menuID) != ''
    def identifyDishName(self, dishName, menuID):
        return self.selectDishIDWithDishName(dishName, menuID) != ''
