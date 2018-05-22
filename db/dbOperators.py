import pymysql
from getpass import getpass

# input the secrect of db
# secrect = getpass("Connecting db..\n--> password: ")
# connect to dataset
db = pymysql.connect("localhost", "root", "yungljy96", "TINYHIPPO")
print('success!')
# create a cursor
cursor = db.cursor()

def executeSQL(sql):
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

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
            print("[SUCCESS] '%s' Sign In Resturant!" % resturantName)
        else:
            print('[FAILED] Username is not existed or password is wrong.')
            
    # Insert operator
    def insertResturantItem(self, resturantName, password, phone, email):
        if not self.identifyResturantName(resturantName):
            if not self.identifyResturantPhone(phone):
                if not self.identifyResturantEmail(email):
                    sql = """INSERT INTO Resturant(resturantName, password, phone, email)
                            VALUES ('%s', '%s', '%s', '%s');""" % (resturantName, password, phone, email)
                    executeSQL(sql)
                    print("[SUCCESS] Username '%s' registed." % resturantName)
                    self.manageResturantTable(resturantName, password)
                else:
                    print("[FAILED] Email '%s' has been registed." % email)
            else:
                print("[FAILED] Phone '%s' has been registed." % phone)
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
        # Edit
        eOpt = editOperator(resturantName=self.resturantName, password=self.password)
        eOpt.deleteEditByResturantID(resturantID=self.resturantID)
        # Order
        oOpt = orderListOperator(resturantName=self.resturantName, password=self.password)
        oOpt.deleteOrderByResturantID(resturantID=self.resturantID)

    # Update operator
    def updateResturantName(self, newName):
        if self.hasSignedIn:
            if not self.identifyResturantName(newName):
                sql = """UPDATE Resturant
                           SET resturantName='%s'
                           WHERE resturantID=%d;""" % (newName, self.resturantID)
                executeSQL(sql)
                self.resturantName = newName
                print("[SUCCESS] Username has been updated to '%s'." % newName)
            else:
                print("[FAILED] Username '%s' has been registed." % newName)
        else:
            print('[FAILED] Please sign in first.')
    def updateResturantPhone(self, newPhone):
        if self.hasSignedIn:
            if not self.identifyResturantPhone(newPhone):
                sql = """UPDATE Resturant
                           SET phone='%s'
                           WHERE resturantID=%d;""" % (newPhone, self.resturantID)
                executeSQL(sql)
                print("[SUCCESS] Phone has been updated to '%s'." % newPhone)
            else:
                print("[FAILED] Phone '%s' has been registed." % newPhone)
        else:
            print('[FAILED] Please sign in first.')
    def updateResturantEmail(self, newEmail):
        if self.hasSignedIn:
            if not self.identifyResturantEmail(newEmail):
                sql = """UPDATE Resturant
                           SET email='%s'
                           WHERE resturantID=%d;""" % (newEmail, self.resturantID)
                executeSQL(sql)
                print("[SUCCESS] Email has been updated to '%s'." % newEmail)
            else:
                print("[FAILED] Email '%s' has been registed." % newEmail)
        else:
            print('[FAILED] Please sign in first.')
    def updateResturantPassword(self, newPassword, oldPassword):
        if self.hasSignedIn:
            sql = """UPDATE Resturant
                       SET password='%s'
                       WHERE resturantID=%d AND password='%s';""" % (newPassword, self.resturantID, oldPassword)
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
    def selectResturantIDWithPhone(self, phone):
        sql = """SELECT resturantID FROM Resturant
                   WHERE phone='%s'""" % (phone)
        return getUniqueResult(sql)
    def selectResturantIDWithEmail(self, email):
        sql = """SELECT resturantID FROM Resturant
                   WHERE email='%s'""" % (email)
        return getUniqueResult(sql)
    def selectResturantNameWithID(self, resturantID):
        sql = """SELECT resturantName FROM Resturant
                   WHERE resturantID=%d""" % (resturantID)
        return getUniqueResult(sql)

    def identifyResturantName(self, resturantName):
        return resturantName != '' and self.selectResturantIDWithName(resturantName) != ''
    def identifyResturantPhone(self, phone):
        return phone != '' and self.selectResturantIDWithPhone(phone) != ''
    def identifyResturantEmail(self, email):
        return email != '' and self.selectResturantIDWithEmail(email) != ''
    def identifyResturantID(self, resturantID):
        return resturantID != '' and self.selectResturantNameWithID(resturantID) != ''

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
            print("[SUCCESS] '%s' Sign In Menu!" % resturantName)
        else:
            print('[FAILED] Username is not existed or password is wrong.')

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
                self.deleteMenuForeignKey(menuID)
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
            menuID = self.selectMenuIDWithTitle(menuTitle, self.resturantID)
            self.deleteMenuByID(menuID)
        else:
            print('[FAILED] Please sign in first.')
    def deleteMenuByResturantID(self, resturantID):
        if self.hasSignedIn:
            menuIDs = self.selectMenuIDsWithResturantID(resturantID)
            for menuID in menuIDs:
                self.deleteMenuByID(menuID)
            print("[SUCCESS] Delete all resturantID '%d' in Menu." % resturantID)
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
                print("[FAILED] MenuTitle '%s' is not existed." % oldTitle)
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
        return getResultSet(sql)

    def identifyMenuTitle(self, menuTitle):
        if self.hasSignedIn:
            return menuTitle != '' and self.selectMenuIDWithTitle(menuTitle, self.resturantID) != ''
        else:
            print('[FAILED] Please sign in first.')
            return False
    def identifyMenuID(self, menuID):
        return menuID != '' and self.selectMenuTitleWithID(menuID) != ''

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
            print("[SUCCESS] '%s' Sign In DishType!" % resturantName)
        else:
            print('[FAILED] Username is not existed or password is wrong.')

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
                self.deleteDishTypeForeignKey(dishTypeID)
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
            dishTypeID = self.selectDishTypeIDWithName(dishTypeName, self.resturantID)
            self.deleteDishTypeByID(dishTypeID)
        else:
            print("[FAILED] Username is not existed or password is wrong.")
    def deleteDishTypeByResturantID(self, resturantID):
        if self.hasSignedIn:
            dishTypeIDs = self.selectDishTypeIDsWithResturantID(resturantID)
            for dishTypeID in dishTypeIDs:
                self.deleteDishTypeByID(dishTypeID)
            print("[SUCCESS] Delete all resturantID '%d' in DishType." % resturantID)
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
                print("[FAILED] DishTypeName '%s' is not existed." % oldName)
        else:
            print('[FAILED] Please sign in first.')

    # select
    def selectDishTypeIDWithName(self, name, resturantID):
        sql = """SELECT dishTypeID FROM DishType
                   WHERE resturantID=%d AND dishTypeName='%s'""" % (resturantID, name)
        return getUniqueResult(sql)
    def selectDishTypeNameWithID(self, dishTypeID):
        sql = """SELECT dishTypeName FROM DishType
                   WHERE dishTypeID=%d""" % (dishTypeID)
        return getUniqueResult(sql)
    def selectDishTypeIDsWithResturantID(self, resturantID):
        sql = """SELECT dishTypeID FROM DishType
                   WHERE resturantID=%d""" % (resturantID)
        return getResultSet(sql)
    def identifyDishTypeName(self, name, resturantID):
        return name != '' and self.selectDishTypeIDWithName(name, resturantID) != ''
    def identifyDishTypeID(self, dishTypeID):
        return dishTypeID != '' and self.selectDishTypeNameWithID(dishTypeID) != ''

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
            self.resturantName = resturantName
            self.password = password
            print("[SUCCESS] '%s' Sign In ResturantTable!" % resturantName)
        else:
            print('[FAILED] Username is not existed or password is wrong.')
    # Insert operator
    def insertTableItem(self, tableNumber):
        if self.hasSignedIn:
            if not self.identifyTableNumber(tableNumber):
                sql = """INSERT INTO ResturantTable(tableNumber, resturantID)
                           VALUES (%d, %d);""" % (tableNumber, self.resturantID)
                executeSQL(sql)
                print("[SUCCESS] TableNumber '%d' has been inserted to ResturantTable." % tableNumber)
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
                sql = """DELETE FROM ResturantTable
                        WHERE tableID=%d;""" % tableID
                executeSQL(sql)
                print("[SUCCESS] ResturantTable '%d' has been deleted." % tableNumber)
            else:
                print("[FAILED] ResturantTable '%d' is not existed." % tableID)
        else:
            print('[FAILED] Please sign in first.')
    def deleteTableByNumber(self, tableNumber):
        if self.hasSignedIn:
            if self.identifyTableNumber(tableNumber):
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
            print("[SUCCESS] Delete all resturantID '%d' in ResturantTable." % resturantID)
        else:
            print('[FAILED] Please sign in first.')
    def deleteTableForeignKey(self, tableID):
        # Delete QRlink Items By TableID
        qOpt = QRlinkOperator(resturantName=self.resturantName, password=self.password)
        qOpt.deleteLinkByTableID(tableID)
        # Delete Customer Items By TableID
        cOpt = customerOperator()
        cOpt.deleteCustomerItemsByTableID(tableID)

    # Update operator
    def updateTableByNumber(self, oldNumber, newNumber):
        if self.hasSignedIn:
            if self.identifyTableNumber(oldNumber):
                if not self.identifyTableNumber(newNumber):
                    sql = """UPDATE ResturantTable
                            SET tableNumber=%d
                            WHERE resturantID=%d AND tableNumber=%d;""" % (newNumber, self.resturantID, oldNumber)
                    executeSQL(sql)
                    print("[SUCCESS] TableNumber has been updated to '%s'." % newNumber)
                else:
                    print("[FAILED] TableNumber '%d' has been created." % newNumber)
            else:
                print("[FAILED] TableNumber '%d' is not existed." % oldNumber)
        else:
            print('[FAILED] Please sign in first.')

    # Select operator
    def selectTableIDWithNumber(self, tableNumber, resturantID):
        sql = """SELECT tableID FROM ResturantTable
                   WHERE resturantID=%d AND tableNumber=%d""" % (resturantID, tableNumber)
        return getUniqueResult(sql)
    def selectTableNumberWithID(self, tableID):
        sql = """SELECT tableNumber FROM ResturantTable
                   WHERE tableID=%d""" % (tableID)
        return getUniqueResult(sql)
    def selectTableIDsWithResturantID(self, resturantID):
        sql = """SELECT tableID FROM ResturantTable
                   WHERE resturantID=%d""" % (resturantID)
        return getResultSet(sql)
    def identifyTableNumber(self, number):
        return number != '' and self.selectTableIDWithNumber(number, self.resturantID) != ''
    def identifyTableID(self, tableID):
        return tableID != '' and self.selectTableNumberWithID(tableID) != ''

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
            print("[SUCCESS] '%s' Sign In QRlink!" % resturantName)
        else:
            print('[FAILED] Username is not existed or password is wrong.')
    # Insert operator
    def insertQRlinkItem(self, linkImageURL, tableNumber):
        if self.hasSignedIn:
            tOpt = tableOperator()
            tableID = tOpt.selectTableIDWithNumber(tableNumber, self.resturantID)
            if not self.identifyLinkImageURL(linkImageURL):
                sql = """INSERT INTO QRlink(linkImageURL, tableID)
                           VALUES ('%s', %d);""" % (linkImageURL, tableID)
                executeSQL(sql)
                print("[SUCCESS] linkImageURL '%s' has been inserted to QRlink." % linkImageURL)
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
                linkID = self.selectLinkIDWithURL(linkImageURL)
                self.deleteLinkByID(linkID)
            else:
                print("[FAILED] linkImageURL '%s' is not existed." % linkImageURL)
        else:
            print('[FAILED] Please sign in first.')
    def deleteLinkByTableID(self, tableID):
        if self.hasSignedIn:
            linkID = self.selectLinkIDWithTableID(tableID)
            if self.identifyLinkID(linkID):
                sql = """DELETE FROM QRlink
                        WHERE tableID=%d;""" % tableID
                executeSQL(sql)
                print("[SUCCESS] Delete tableID '%d'." % tableID)
            else:
                print("[FAILED] TableID '%d' is not existed." % tableID)
        else:
            print('[FAILED] Please sign in first.')

    # Update operator
    def updateLinkImageURL(self, oldURL, newURL):
        if self.hasSignedIn:
            if self.identifyLinkImageURL(oldURL):
                if not self.identifyLinkImageURL(newURL):
                    sql = """UPDATE QRlink
                               SET linkImageURL='%s'
                               WHERE linkImageURL='%s';""" % (newURL, oldURL)
                    executeSQL(sql)
                    print("[SUCCESS] LinkImageURL has been updated to '%s'." % newURL)
                else:
                    print("[FAILED] LinkImageURL '%s' has been created." % newURL)
            else:
                print("[FAILED] LinkImageURL '%s' is not existed." % oldURL)
        else:
            print('[FAILED] Please sign in first.')
    def updateTableID(self, oldTableID, newTableID):
        if self.hasSignedIn:
            linkID = self.selectLinkIDWithTableID(oldTableID)
            if self.identifyLinkID(linkID):
                linkID = self.selectLinkIDWithTableID(newTableID)
                if self.identifyLinkID(linkID):
                    self.deleteLinkByTableID(tableID=newTableID)
                sql = """UPDATE QRlink
                           SET tableID=%d
                           WHERE tableID=%d;""" % (newTableID, oldTableID)
                executeSQL(sql)
                print("[SUCCESS] Table ID has been updated to '%d'." % newTableID)
            else:
                print("[FAILED] LinkImageURL '%d' is not existed." % oldTableID)
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
        return linkImageURL != '' and linkImageURL != '' and self.selectLinkIDWithURL(linkImageURL) != ''
    def identifyLinkID(self, linkID):
        return linkID != '' and linkID != '' and self.selectURLWithID(linkID) != ''

## -----------------------------------------------------
## Table `TINYHIPPO`.`EditRelation`
## -----------------------------------------------------
class editOperator:
    def __init__(self, resturantName=None, password=None):
        self.resturantID = None
        self.hasSignedIn = False
        if resturantName != None and password != None:
            self.manageEditTable(resturantName, password)
    
    # Sign in to manage 'Edit' table
    def manageEditTable(self, resturantName=None, password=None):
        if signIn(resturantName, password):
            rOpt = resturantOperator()
            self.resturantID = rOpt.selectResturantIDWithName(resturantName)
            self.hasSignedIn = True
            self.resturantName = resturantName
            self.password = password
            print("[SUCCESS] '%s' Sign In Edit!" % resturantName)
        else:
            print('[FAILED] Username is not existed or password is wrong.')

    # Insert operator
    def insertEditItem(self, customerName, orderNumber):
        if self.hasSignedIn:
            # get customerID
            cOpt = customerOperator()
            customerID = cOpt.selectCustomerIDWithName(customerName)
            if cOpt.identifyCustomerID(customerID):
                if not self.identifyEditItemWithCustomerID(customerID):
                    # create OrderList Item and get orderID
                    oOpt = orderListOperator(resturantName=self.resturantName, password=self.password)
                    if not oOpt.identifyOrderNumber(orderNumber=orderNumber):
                        orderDishes = ''
                        total = 0.0
                        orderNumber = oOpt.insertOrderItem(orderDishes=orderDishes, total=total)
                    orderID = oOpt.selectOrderIDWithOrderNumber(orderNumber=orderNumber)

                    now = getNow()
                    sql = """INSERT INTO EditRelation(customerID, orderID, editedTime, resturantID)
                                VALUES (%d, %d, '%s', %d);""" % (customerID, orderID, now, self.resturantID)
                    executeSQL(sql)
                    print("[SUCCESS] CustomerName '%s' begins to edit orderNumber '%d' at '%s'." % (customerName, orderNumber, now))
                else:
                    print("[FAILED] CustomerName '%s' has order unpaid." % (customerName))
            else:
                print("[FAILED] CustomerName '%s' is not existed." % customerName)
        else:
            print('[FAILED] Please sign in first.')
    
    # Delete operator
    def deleteEditItemByCustomerIDAndOrderID(self, customerID, orderID):
        if self.hasSignedIn:
            if self.identifyEditItem(customerID, orderID):
                sql = """DELETE FROM EditRelation
                            WHERE customerID=%d AND orderID=%d;""" % (customerID, orderID)
                executeSQL(sql)
                print("[SUCCESS] Delete Edit item which stored customerID '%d' and orderID '%d'." % (customerID, orderID))
            else:
                print("[FAILED] There is no Edit item which stored customerID '%d' and orderID '%d'." % (customerID, orderID))
        else:
            print('[FAILED] Please sign in first.')
    def deleteEditItemByCustomerID(self, customerID):
        if self.hasSignedIn:
            orderIDs = self.selectOrderIDsWithCustomerID(customerID)
            if self.identifyEditItemWithCustomerID(customerID):
                for orderID in orderIDs:
                    self.deleteEditItemByCustomerIDAndOrderID(customerID, orderID)
                print("[SUCCESS] Delete all Edit items which stored customerID '%d'." % customerID)
            else:
                print("[FAILED] There is no Edit item which stored customerID '%d'." % customerID)
        else:
            print('[FAILED] Please sign in first.')
    def deleteEditItemByOrderID(self, orderID):
        if self.hasSignedIn:
            customerIDs = self.selectCustomerIDsWithOrderID(orderID)
            if self.identifyEditItemWithOrderID(orderID):
                for customerID in customerIDs:
                    self.deleteEditItemByCustomerIDAndOrderID(customerID, orderID)
                print("[SUCCESS] Delete all Edit items which stored orderID '%d'." % orderID)
            else:
                print("[FAILED] There is no Edit item which stored orderID '%d'." % orderID)
        else:
            print('[FAILED] Please sign in first.')
    def deleteEditByResturantID(self, resturantID):
        if self.hasSignedIn:
            sql = """DELETE FROM EditRelation
                        WHERE resturantID=%d;""" % (self.resturantID)
            executeSQL(sql)
            print("[SUCCESS] Delete Edit item which stored resturantID '%d'." % (self.resturantID))
        else:
            print('[FAILED] Please sign in first.')

    # Update operator
    def updateOrderDishes(self, customerName, orderNumber, newOrderDishes, total):
        if self.hasSignedIn:
            # get customerID
            cOpt = customerOperator()
            customerID = cOpt.selectCustomerIDWithName(customerName)
            if cOpt.identifyCustomerID(customerID):
                if self.identifyEditItemWithCustomerID(customerID):
                    # create OrderList Item and get orderID
                    oOpt = orderListOperator(resturantName=self.resturantName, password=self.password)
                    if oOpt.identifyOrderNumber(orderNumber=orderNumber):
                        now = getNow()
                        # todo: collision
                        orderID = oOpt.selectOrderIDWithOrderNumber(orderNumber=orderNumber)
                        oOpt.updateOrderDishes(newOrderDishes=newOrderDishes, total=total, orderID=orderID)
                        oOpt.updateIsPaid(isPaid='False', orderID=orderID)
                        # update the time
                        self.updateEditTime(editedTime=now, customerID=customerID, orderID=orderID)
                        print("[SUCCESS] CustomerName '%s' updated OrderDishes of OrderNumber '%d' at '%s'." % (customerName, orderNumber, now))
                    else:
                        print("[FAILED] orderNumber '%d' is not existed." % (orderNumber))
                else:
                    print("[FAILED] CustomerName '%s' is not existed." % (customerName))
            else:
                print("[FAILED] CustomerName '%s' is not existed." % customerName)
        else:
            print('[FAILED] Please sign in first.')

    def updateIsPaid(self, isPaid, customerName, orderNumber):
        if self.hasSignedIn:
            # get customerID
            cOpt = customerOperator()
            customerID = cOpt.selectCustomerIDWithName(customerName)
            if cOpt.identifyCustomerID(customerID):
                if self.identifyEditItemWithCustomerID(customerID):
                    # create OrderList Item and get orderID
                    oOpt = orderListOperator(resturantName=self.resturantName, password=self.password)
                    if oOpt.identifyOrderNumber(orderNumber=orderNumber):
                        now = getNow()
                        # todo: collision
                        orderID = oOpt.selectOrderIDWithOrderNumber(orderNumber=orderNumber)
                        oOpt.updateIsPaid(isPaid=isPaid, orderID=orderID)
                        # update the time
                        self.updateEditTime(editedTime=now, customerID=customerID, orderID=orderID)
                        print("[SUCCESS] CustomerName '%s' updated IsPaid of OrderNumber '%d' to '%s' at '%s' ." % (customerName, orderNumber, isPaid, now))
                    else:
                        print("[FAILED] orderNumber '%d' is not existed." % (orderNumber))
                else:
                    print("[FAILED] CustomerName '%s' is not existed." % (customerName))
            else:
                print("[FAILED] CustomerName '%s' is not existed." % customerName)
        else:
            print('[FAILED] Please sign in first.')

    def updateStatusToDone(self, customerName, orderNumber):
        if self.hasSignedIn:
            # get customerID
            cOpt = customerOperator()
            customerID = cOpt.selectCustomerIDWithName(customerName)
            if cOpt.identifyCustomerID(customerID):
                if self.identifyEditItemWithCustomerID(customerID):
                    # create OrderList Item and get orderID
                    oOpt = orderListOperator(resturantName=self.resturantName, password=self.password)
                    if oOpt.identifyOrderNumber(orderNumber=orderNumber):
                        now = getNow()
                        # todo: collision
                        orderID = oOpt.selectOrderIDWithOrderNumber(orderNumber=orderNumber)
                        oOpt.updateStatusToDone(orderID=orderID)
                        print("[SUCCESS] orderNumber '%d' has Done at '%s'." % (orderNumber, now))
                        self.deleteEditItemByOrderID(orderID=orderID)
                    else:
                        print("[FAILED] orderNumber '%d' is not existed." % (orderNumber))
                else:
                    print("[FAILED] CustomerName '%s' is not existed." % (customerName))
            else:
                print("[FAILED] CustomerName '%s' is not existed." % customerName)
        else:
            print('[FAILED] Please sign in first.')

    def updateEditTime(self, editedTime, customerID, orderID):
        if self.hasSignedIn:
            if self.identifyEditItem(customerID, orderID):
                now = getNow()
                sql = """UPDATE EditRelation
                            SET editedTime='%s'
                            WHERE customerID=%d AND orderID=%d;""" % (now, customerID, orderID)
                executeSQL(sql)
                print("[SUCCESS] The Edit item has updated at '%s'. [customerID '%d' and orderID '%d']" % (now, customerID, orderID))
            else:
                print("[FAILED] There is no Edit item which stored customerID '%d' and orderID '%d'." % (customerID, orderID))
        else:
            print('[FAILED] Please sign in first.')

    # Select operator
    def selectCustomerIDsWithOrderID(self, orderID):
        sql = """SELECT customerID FROM EditRelation
                   WHERE orderID=%d""" % (orderID)
        return getResultSet(sql)
    def selectOrderIDsWithCustomerID(self, customerID):
        sql = """SELECT orderID FROM EditRelation
                   WHERE customerID=%d""" % (customerID)
        return getResultSet(sql)
    def selectEditedTimeWithCustomerIDAndOrderID(self, customerID, orderID):
        sql = """SELECT editedTime FROM EditRelation
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
    # Insert operator
    def insertCustomerItem(self, customerName, linkID):
        if not self.identifyCustomerName(customerName):
            lOpt = QRlinkOperator()
            tableID = lOpt.selectTableIDWithLinkID(linkID)
            sql = """INSERT INTO Customer(customerName, tableID)
                       VALUES ('%s', %d);""" % (customerName, tableID)
            executeSQL(sql)
            print("[SUCCESS] customerName '%s' has been inserted." % customerName)
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
            print("[FAILED] There is no TableID '%d'." % tableID)

    # Update operator
    def updateCustomerName(self, oldCustomerName, newCustomerName):
        if self.identifyCustomerName(oldCustomerName):
            if not self.identifyCustomerName(newCustomerName):
                sql = """UPDATE Customer
                            SET customerName='%s'
                            WHERE customerName='%s';""" % (newCustomerName, oldCustomerName)
                executeSQL(sql)
                print("[SUCCESS] The CustomerName has updated to '%s'." % newCustomerName)
            else:
                print("[FAILED] CustomerName '%s' has been created." % newCustomerName)
        else:
            print("[FAILED] CustomerName '%s' is not existed." % oldCustomerName)
    def updateTableIDWithCustomerName(self, customerName, oldTableID, newTableID):
        if self.identifyCustomerName(customerName):
            if self.identifyTableID(oldTableID):
                sql = """UPDATE Customer
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

    def identifyCustomerName(self, customerName):
        return customerName != '' and self.selectCustomerIDWithName(customerName) != ''
    def identifyCustomerID(self, customerID):
        return customerID != '' and self.selectCustomerNameWithID(customerID) != ''
    def identifyTableID(self, tableID):
        return tableID != '' and self.selectCustomerIDsWithTableID(tableID) != []

## -----------------------------------------------------
## Table `TINYHIPPO`.`OrderList`
## -----------------------------------------------------
class orderListOperator:
    def __init__(self, resturantName=None, password=None):
        self.resturantID = None
        self.hasSignedIn = False
        if resturantName != None and password != None:
            self.manageOrderListTable(resturantName, password)
    
    # Sign in to manage 'OrderList' table
    def manageOrderListTable(self, resturantName=None, password=None):
        if signIn(resturantName, password):
            rOpt = resturantOperator()
            self.resturantID = rOpt.selectResturantIDWithName(resturantName)
            self.hasSignedIn = True
            self.resturantName=resturantName
            self.password = password
            print("[SUCCESS] '%s' Sign In OrderList!" % resturantName)
        else:
            print('[FAILED] Username is not existed or password is wrong.')

    # Insert operator
    def insertOrderItem(self, orderDishes, total):
        '''
        Input:
            orderDishes: the json of dishes in the order
            total: the total of the order
        '''
        if self.hasSignedIn:
            # initialize param
            status = 'todo'
            isPaid = 'False'
            # determine orderNumber
            orderNumber = self.getMaxNumber() + 1
            sql = """INSERT INTO OrderList(orderNumber, orderDishes, status, total, isPaid, resturantID)
                    VALUES (%d, '%s', '%s', %f, '%s', %d);""" % (orderNumber, orderDishes, status, total, isPaid, self.resturantID)
            executeSQL(sql)
            print("[SUCCESS] A new Order '%d' has been inserted to Table." % orderNumber)
            return orderNumber
        else:
            print('[FAILED] Please sign in first.')
            return 0
    # Delete operator
    def deleteOrderItemWithOrderID(self, orderID):
        if self.hasSignedIn:
            if self.identifyOrderID(orderID):
                sql = """DELETE FROM OrderList
                        WHERE orderID=%d AND resturantID=%d;""" % (orderID, self.resturantID)
                executeSQL(sql)
                print("[SUCCESS] The OrderID '%d' has been deleted." % orderID)
            else:
                print("[FAILED] OrderID '%d' is not existed." % orderID)
        else:
            print('[FAILED] Please sign in first.')
    def deleteOrderByResturantID(self, resturantID):
        if self.hasSignedIn:
            sql = """DELETE FROM OrderList
                        WHERE resturantID=%d;""" % (self.resturantID)
            executeSQL(sql)
            print("[SUCCESS] Delete OrderList item which stored resturantID '%d'." % (self.resturantID))
        else:
            print('[FAILED] Please sign in first.')

    # Update operator
    def updateOrderDishes(self, newOrderDishes, total, orderID):
        if self.hasSignedIn:
            if self.identifyOrderID(orderID):
                sql = """UPDATE OrderList
                        SET orderDishes='%s', total=%f
                        WHERE orderID=%d AND resturantID=%d;""" % (newOrderDishes, total, orderID, self.resturantID)
                executeSQL(sql)
                print("[SUCCESS] The orderDishes of OrderID '%d' has been updated." % (orderID))
            else:
                print("[FAILED] OrderID '%d' is not existed." % orderID)
        else:
            print('[FAILED] Please sign in first.')

    def updateTotal(self, total, orderID):
        if self.hasSignedIn:
            if self.identifyOrderID(orderID):
                sql = """UPDATE OrderList
                        SET total=%f
                        WHERE orderID=%d AND resturantID=%d;""" % (total, orderID, self.resturantID)
                executeSQL(sql)
                print("[SUCCESS] The total of OrderID '%d' has been updated to '%.2f'." % (orderID, total))
            else:
                print("[FAILED] OrderID '%d' is not existed." % orderID)
        else:
            print('[FAILED] Please sign in first.')
    
    def updateStatusToDone(self, orderID):
        if self.hasSignedIn:
            if self.identifyOrderID(orderID):
                if self.identifyIsPaid(orderID):
                    status = 'done'
                    sql = """UPDATE OrderList
                            SET status='%s'
                            WHERE orderID=%d AND resturantID=%d;""" % (status, orderID, self.resturantID)
                    executeSQL(sql)
                    print("[SUCCESS] The Status of OrderID '%d' has been updated to '%s'." % (orderID, status))
                else:
                    print("[FAILED] OrderID '%d' has not been paid." % orderID)
            else:
                print("[FAILED] OrderID '%d' is not existed." % orderID)
        else:
            print('[FAILED] Please sign in first.')

    def updateIsPaid(self, isPaid, orderID):
        if self.hasSignedIn:
            if self.identifyOrderID(orderID):
                status = 'doing' if isPaid == 'True' else 'todo'
                sql = """UPDATE OrderList
                        SET status='%s', isPaid='%s'
                        WHERE orderID=%d;""" % (status, isPaid, orderID)
                executeSQL(sql)
                print("[SUCCESS] IsPaid of OrderID '%d' has been updated to '%s'." % (orderID, isPaid))
            else:
                print("[FAILED] OrderID '%d' is not existed." % orderID)
        else:
            print('[FAILED] Please sign in first.')

    # Select operator
    def selectOrderIDWithOrderNumber(self, orderNumber):
        if self.hasSignedIn:
            sql = """SELECT orderID FROM OrderList
                       WHERE orderNumber=%d AND resturantID=%d;""" % (orderNumber, self.resturantID)
            return getUniqueResult(sql)
        else:
            print('[FAILED] Please sign in first.')
            return ''
    def selectOrderIDsWithResturantID(self):
        if self.hasSignedIn:
            sql = """SELECT orderID FROM OrderList
                    WHERE resturantID=%d;""" % self.resturantID
            return getResultSet(sql)
        else:
            print('[FAILED] Please sign in first.')
            return []
    def selectOrderDishesWithOrderID(self, orderID):
        sql = """SELECT orderDishes FROM OrderList
                   WHERE orderID=%d;""" % (orderID)
        return getUniqueResult(sql)
    def selectStatusWithOrderID(self, orderID):
        sql = """SELECT status FROM OrderList
                   WHERE orderID=%d;""" % (orderID)
        return getUniqueResult(sql)
    def selectTotalWithOrderID(self, orderID):
        sql = """SELECT total FROM OrderList
                   WHERE orderID=%d;""" % (orderID)
        return getUniqueResult(sql)
    def selectIsPaidWithOrderID(self, orderID):
        sql = """SELECT isPaid FROM OrderList
                   WHERE orderID=%d;""" % orderID
        return getUniqueResult(sql)
    
    def identifyIsPaid(self, orderID):
        return self.selectIsPaidWithOrderID(orderID) == 'True'
    def identifyOrderID(self, orderID):
        return self.selectTotalWithOrderID(orderID) != ''
    def identifyOrderNumber(self, orderNumber):
        return self.selectOrderIDWithOrderNumber(orderNumber) != ''
    def getMaxNumber(self):
        if self.hasSignedIn:
            sql = """SELECT MAX(orderNumber) FROM OrderList"""
            number = getUniqueResult(sql)
            return 0 if number == None else int(number)
        else:
            print('[FAILED] Please sign in first.')
            return 0
    

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
            print("[SUCCESS] '%s' Sign In Dish!" % resturantName)
        else:
            print('[FAILED] Username is not existed or password is wrong.')

    # Insert operator
    def insertDishItem(self, dishName='', price=0, dishImageURL='', dishTypeName='', menuTitle=''):
        if self.hasSignedIn:
            # get dishTypeID
            dtOpt = dishTypeOperator()
            dishTypeID = dtOpt.selectDishTypeIDWithName(dishTypeName, self.resturantID)
            # get menuID
            mOpt = menuOperator()
            menuID = mOpt.selectMenuIDWithTitle(menuTitle, self.resturantID)
            if not self.identifyDishName(dishName, menuID):
                dishComment=''
                dishHot=0
                monthlySales=0
                sql = """INSERT INTO Dish(dishName, price, dishImageURL, dishComment, dishHot, monthlySales, dishTypeID, menuID)
                           VALUES ('%s', %f, '%s', '%s', %d, %d, %d, %d);""" % (dishName, float(price), dishImageURL, dishComment, dishHot, monthlySales, dishTypeID, menuID)
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
                sql = """UPDATE Dish
                            SET dishName='%s'
                            WHERE dishName='%s' AND menuID=%d;""" % (newDishName, oldDishName, menuID)
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
                sql = """UPDATE Dish
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
                sql = """UPDATE Dish
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
                sql = """UPDATE Dish
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
                sql = """UPDATE Dish
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
                sql = """UPDATE Dish
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
        return dishID != '' and menuID != '' and self.selectDishNameWithDishID(dishID, menuID) != ''
    def identifyDishName(self, dishName, menuID):
        return dishName != '' and menuID != '' and self.selectDishIDWithDishName(dishName, menuID) != ''
