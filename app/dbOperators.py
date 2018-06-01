import pymysql
from tools import *

path_to_config = "./config"

# load config of database
config = get_config(path_to_config)

# connect to dataset
db = pymysql.connect(host='db',
                     user='root',
                     password='p@ssw0rd123',
                     database='TINYHIPPO',
                     charset='utf8')
# create a cursor
cursor = db.cursor()

# -----------------------------------------------------
# Table `TINYHIPPO`.`Resturant`
# -----------------------------------------------------


class resturantOperator():
    def __init__(self, resturantName=None, password=None):
        self.resturantID = None
        self.hasSignedIn = False
        if resturantName != None and password != None:
            self.manageResturantTable(
                resturantName=resturantName, password=password)

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
                print("[SUCCESS] Username '%s' has been deleted." %
                      ResturantName)
            else:
                print("[FAILED] resturantID '%d' is not existed." %
                      resturantID)
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
        # DishType
        dtOpt = dishTypeOperator(
            resturantName=self.resturantName, password=self.password)
        dtOpt.deleteDishTypeByResturantID(resturantID=self.resturantID)
        # todo: Dish
        dOpt = dishOperator(resturantName=self.resturantName,
                            password=self.password)
        # dOpt.deleteDishItemsWithResturantID(resturantID=self.resturantID)
        # Table
        tOpt = tableOperator(
            resturantName=self.resturantName, password=self.password)
        tOpt.deleteTableByResturantID(resturantID=self.resturantID)

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

# -----------------------------------------------------
# Table `TINYHIPPO`.`DishType`
# -----------------------------------------------------


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
                print(
                    "[SUCCESS] DishTypeName '%s' has been inserted to DishType." % dishTypeName)
            else:
                print("[FAILED] DishTypeName '%s' has been created." %
                      dishTypeName)
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
                print("[SUCCESS] DishTypeName '%s' has been deleted." %
                      dishTypeName)
            else:
                print("[FAILED] DishTypeID '%d' is not existed." % dishTypeID)
        else:
            print('[FAILED] Please sign in first.')

    def deleteDishTypeByName(self, dishTypeName):
        if self.hasSignedIn:
            dishTypeID = self.selectDishTypeIDWithName(
                dishTypeName, self.resturantID)
            self.deleteDishTypeByID(dishTypeID)
        else:
            print("[FAILED] Username is not existed or password is wrong.")

    def deleteDishTypeByResturantID(self, resturantID):
        if self.hasSignedIn:
            dishTypeIDs = self.selectDishTypeIDsWithResturantID(resturantID)
            for dishTypeID in dishTypeIDs:
                self.deleteDishTypeByID(dishTypeID)
            print("[SUCCESS] Delete all resturantID '%d' in DishType." %
                  resturantID)
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
                    print(
                        "[SUCCESS] DishTypeName has been updated to '%s'." % newName)
                else:
                    print("[FAILED] DishTypeName '%s' has been created." % newName)
            else:
                print("[FAILED] DishTypeName '%s' is not existed." % oldName)
        else:
            print('[FAILED] Please sign in first.')

    # select
    def selectDishTypeIDWithName(self, dishTypeName, resturantID):
        sql = """SELECT dishTypeID FROM DishType
                   WHERE resturantID=%d AND dishTypeName='%s'""" % (resturantID, dishTypeName)
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
    # new

    def selectAllDishType(self):
        sql = """SELECT * FROM DishType"""
        return getAllSet(sql)

# -----------------------------------------------------
# Table `TINYHIPPO`.`ResturantTable`
# -----------------------------------------------------


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
                sql = """INSERT INTO ResturantTable(tableNumber, currentOrderNumber, resturantID)
                           VALUES (%d, %d, %d);""" % (tableNumber, -1, self.resturantID)
                executeSQL(sql)
                print(
                    "[SUCCESS] TableNumber '%d' has been inserted to ResturantTable." % tableNumber)
            else:
                print("[FAILED] TableNumber '%d' has been created." %
                      tableNumber)
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
                print("[SUCCESS] ResturantTable '%d' has been deleted." %
                      tableNumber)
            else:
                print("[FAILED] ResturantTable '%d' is not existed." % tableID)
        else:
            print('[FAILED] Please sign in first.')

    def deleteTableByNumber(self, tableNumber):
        if self.hasSignedIn:
            if self.identifyTableNumber(tableNumber):
                tableID = self.selectTableIDWithNumber(
                    tableNumber, self.resturantID)
                self.deleteTableForeignKey(tableID)
                self.deleteTableByID(tableID)
            else:
                print("[FAILED] TableNumber '%d' is not existed." %
                      tableNumber)
        else:
            print('[FAILED] Please sign in first.')

    def deleteTableByResturantID(self, resturantID):
        if self.hasSignedIn:
            tableIDs = self.selectTableIDsWithResturantID(resturantID)
            for tableID in tableIDs:
                self.deleteTableByID(tableID)
            print(
                "[SUCCESS] Delete all resturantID '%d' in ResturantTable." % resturantID)
        else:
            print('[FAILED] Please sign in first.')

    def deleteTableForeignKey(self, tableID):
        # Delete QRlink Items By TableID
        qOpt = QRlinkOperator(
            resturantName=self.resturantName, password=self.password)
        qOpt.deleteLinkByTableID(tableID)

    # Update operator
    def updateTableByNumber(self, oldNumber, newNumber):
        if self.hasSignedIn:
            if self.identifyTableNumber(oldNumber):
                if not self.identifyTableNumber(newNumber):
                    sql = """UPDATE ResturantTable
                            SET tableNumber=%d
                            WHERE resturantID=%d AND tableNumber=%d;""" % (newNumber, self.resturantID, oldNumber)
                    executeSQL(sql)
                    print(
                        "[SUCCESS] TableNumber has been updated to '%s'." % newNumber)
                else:
                    print("[FAILED] TableNumber '%d' has been created." %
                          newNumber)
            else:
                print("[FAILED] TableNumber '%d' is not existed." % oldNumber)
        else:
            print('[FAILED] Please sign in first.')

    def updateCurrentOrderNumberByTableID(self, currentOrderNumber, tableID):
        if self.hasSignedIn:
            if self.identifyAvailableTableID(tableID):
                sql = """UPDATE ResturantTable
                           SET currentOrderNumber=%d
                           WHERE resturantID=%d AND tableID=%d;""" % (currentOrderNumber, self.resturantID, tableID)
                executeSQL(sql)
                print("[SUCCESS] currentOrderNumber has been updated to '%s'." %
                      currentOrderNumber)
            else:
                print("[FAILED] Table ID '%d' is not available." % tableID)
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

    def selectAvailableTableIDsWithResturantID(self, resturantID):
        sql = """SELECT tableID FROM ResturantTable
                   WHERE resturantID=%d and currentOrderNumber=%d""" % (resturantID, -1)
        return getResultSet(sql)

    def selectCurrentOrderNumberWithTableID(self, tableID):
        sql = """SELECT currentOrderNumber FROM ResturantTable
                   WHERE tableID=%d""" % tableID
        return getUniqueResult(sql)

    def identifyTableNumber(self, number):
        return number != '' and self.selectTableIDWithNumber(number, self.resturantID) != ''

    def identifyTableID(self, tableID):
        return tableID != '' and self.selectTableNumberWithID(tableID) != ''

    def identifyAvailableTableID(self, tableID):
        return tableID != '' and self.selectCurrentOrderNumberWithTableID(tableID) != ''


# -----------------------------------------------------
# Table `TINYHIPPO`.`QRlink`
# -----------------------------------------------------
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
            self.resturantName = resturantName
            self.password = password
            print("[SUCCESS] '%s' Sign In QRlink!" % resturantName)
        else:
            print('[FAILED] Username is not existed or password is wrong.')
    # Insert operator

    def insertQRlinkItem(self, linkImageURL, tableNumber):
        if self.hasSignedIn:
            tOpt = tableOperator(
                resturantName=self.resturantName, password=self.password)
            if tOpt.identifyTableNumber(tableNumber):
                tableID = tOpt.selectTableIDWithNumber(
                    tableNumber, self.resturantID)
                if not self.identifyLinkImageURL(linkImageURL):
                    sql = """INSERT INTO QRlink(linkImageURL, tableID)
                            VALUES ('%s', %d);""" % (linkImageURL, tableID)
                    executeSQL(sql)
                    print(
                        "[SUCCESS] linkImageURL '%s' has been inserted to QRlink." % linkImageURL)
                else:
                    print("[FAILED] linkImageURL '%s' has been created." %
                          linkImageURL)
            else:
                print("[FAILED] tableNumber '%d' is not existed." %
                      tableNumber)
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
                print(
                    "[SUCCESS] The QRlink of Table '%d' has been deleted." % tableNumber)
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
                print("[FAILED] linkImageURL '%s' is not existed." %
                      linkImageURL)
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
                    print(
                        "[SUCCESS] LinkImageURL has been updated to '%s'." % newURL)
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
                print("[SUCCESS] Table ID has been updated to '%d'." %
                      newTableID)
            else:
                print("[FAILED] LinkImageURL '%d' is not existed." %
                      oldTableID)
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

# -----------------------------------------------------
# Table `TINYHIPPO`.`Customer`
# -----------------------------------------------------


class customerOperator:
    # Insert operator
    def insertCustomerItem(self, customerName, linkID):
        if not self.identifyCustomerName(customerName):
            lOpt = QRlinkOperator()
            if lOpt.identifyLinkID(linkID):
                tableID = lOpt.selectTableIDWithLinkID(linkID)
                sql = """INSERT INTO Customer(customerName, tableID)
                        VALUES ('%s', %d);""" % (customerName, tableID)
                executeSQL(sql)
                print("[SUCCESS] customerName '%s' has been inserted." %
                      customerName)
            else:
                print("[FAILED] linkID '%d' is not existed." % linkID)
        else:
            print("[FAILED] customerName '%s' has been created." %
                  customerName)

    # Delete operator
    def deleteCustomerItemByCustomerID(self, customerID):
        if self.identifyCustomerID(customerID):
            customerName = self.selectCustomerNameWithID(customerID)
            sql = """DELETE FROM Customer
                       WHERE customerID=%d;""" % customerID
            executeSQL(sql)
            print("[SUCCESS] The Customer '%s' has been deleted." %
                  customerName)
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
            print(
                "[SUCCESS] All Customers eat on TableID '%d' has been deleted." % tableID)
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
                print("[SUCCESS] The CustomerName has updated to '%s'." %
                      newCustomerName)
            else:
                print("[FAILED] CustomerName '%s' has been created." %
                      newCustomerName)
        else:
            print("[FAILED] CustomerName '%s' is not existed." %
                  oldCustomerName)

    def updateTableIDWithCustomerName(self, customerName, oldTableID, newTableID):
        if self.identifyCustomerName(customerName):
            if self.identifyTableID(oldTableID):
                sql = """UPDATE Customer
                            SET tableID=%d
                            WHERE customerName='%s' AND tableID=%d;""" % (newTableID, customerName, oldTableID)
                executeSQL(sql)
                print("[SUCCESS] The TableID of Customer '%s' has updated to '%d'." % (
                    customerName, newTableID))
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

# -----------------------------------------------------
# Table `TINYHIPPO`.`OrderList`
# -----------------------------------------------------


class orderListOperator:
    # Insert operator
    def insertOrderItem(self, orderDetail, total, tableID, customerID):
        '''
        Input:
            orderDishes: the json of dishes in the order
            total: the total of the order
        '''
        # determine orderNumber
        now = getNow()
        # todo: collision
        orderNumber = self.getMaxNumber() + 1
        sql = """INSERT INTO OrderList(orderNumber, orderDetail, total, isPaid, status, editedTime, tableID, customerID)
                    VALUES (%d, '%s', %f, %d, '%s', '%s', %d, %d);""" % (orderNumber, orderDetail, total, False, 'todo', now, tableID, customerID)
        executeSQL(sql)
        print("[SUCCESS] A new Order '%d' has been inserted to Table." %
              orderNumber)
        return orderNumber

    # Delete operator
    def deleteOrderItemWithOrderID(self, orderID):
        if self.identifyOrderID(orderID):
            sql = """DELETE FROM OrderList
                        WHERE orderID=%d;""" % orderID
            executeSQL(sql)
            print("[SUCCESS] The OrderID '%d' has been deleted." % orderID)
        else:
            print("[FAILED] OrderID '%d' is not existed." % orderID)

    def deleteOrderItemsWithTableID(self, tableID, resturantName, password):
        if signIn(resturantName=resturantName, password=password):
            tOpt = tableOperator(
                resturantName=resturantName, password=password)
            if tOpt.identifyTableID(tableID=tableID):
                sql = """DELETE FROM OrderList
                        WHERE tableID=%d;""" % tableID
                executeSQL(sql)
                print(
                    "[SUCCESS] Delete OrderList items which stored tableID '%d'." % tableID)
            else:
                print("[FAILED] TableID '%d' is not existed." % tableID)
        else:
            print('[FAILED] Please sign in first.')

    def deleteOrderItemsWithCustomerID(self, customerID, resturantName, password):
        if signIn(resturantName=resturantName, password=password):
            cOpt = customerOperator()
            if cOpt.identifyCustomerID(customerID=customerID):
                sql = """DELETE FROM OrderList
                        WHERE customerID=%d;""" % customerID
                executeSQL(sql)
                print(
                    "[SUCCESS] Delete OrderList items which stored customerID '%d'." % customerID)
            else:
                print("[FAILED] CustomerID '%d' is not existed." % customerID)
        else:
            print('[FAILED] Please sign in first.')

    # Update operator
    def updateOrderDetail(self, newOrderDetail, total, orderID):
        if self.identifyOrderID(orderID):
            now = getNow()
            sql = """UPDATE OrderList
                       SET orderDetail='%s', total=%f, editedTime='%s'
                       WHERE orderID=%d;""" % (newOrderDetail, total, now, orderID)
            executeSQL(sql)
            print(
                "[SUCCESS] The orderDishes of OrderID '%d' has been updated." % (orderID))
        else:
            print("[FAILED] OrderID '%d' is not existed." % orderID)

    def updateTotal(self, total, orderID):
        if self.identifyOrderID(orderID):
            now = getNow()
            sql = """UPDATE OrderList
                       SET total=%f, editedTime='%s'
                       WHERE orderID=%d;""" % (total, now, orderID)
            executeSQL(sql)
            print("[SUCCESS] The total of OrderID '%d' has been updated to '%.2f'." % (
                orderID, total))
        else:
            print("[FAILED] OrderID '%d' is not existed." % orderID)

    def updateStatus(self, status, orderID):
        if status not in ['todo', 'doing', 'done']:
            print("[FAILED] The status '%s' is invalid." % status)
        if self.identifyOrderID(orderID):
            if self.identifyIsPaid(orderID):
                sql = """UPDATE OrderList
                           SET status='%s'
                           WHERE orderID=%d;""" % (status, orderID)
                executeSQL(sql)
                print("[SUCCESS] The Status of OrderID '%d' has been updated to '%s'." % (
                    orderID, status))
            else:
                print("[FAILED] OrderID '%d' has not been paid." % orderID)
        else:
            print("[FAILED] OrderID '%d' is not existed." % orderID)

    def updateIsPaid(self, isPaid, orderID):
        if self.identifyOrderID(orderID):
            sql = """UPDATE OrderList
                        SET isPaid=%d
                        WHERE orderID=%d;""" % (isPaid, orderID)
            executeSQL(sql)
            print("[SUCCESS] IsPaid of OrderID '%d' has been updated to '%s'." % (
                orderID, isPaid))
        else:
            print("[FAILED] OrderID '%d' is not existed." % orderID)

    # Select operator
    def selectOrderIDWithOrderNumber(self, orderNumber):
        sql = """SELECT orderID FROM OrderList
                   WHERE orderNumber=%d;""" % orderNumber
        return getUniqueResult(sql)

    def selectOrderIDsWithTableID(self, tableID):
        sql = """SELECT orderID FROM OrderList
                    WHERE tableID=%d;""" % tableID
        return getResultSet(sql)

    def selectOrderIDsWithCustomerID(self, customerID):
        sql = """SELECT orderID FROM OrderList
                   WHERE customerID=%d;""" % customerID
        return getResultSet(sql)

    def selectOrderDetailWithOrderID(self, orderID):
        sql = """SELECT orderDetail FROM OrderList
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
        sql = """SELECT MAX(orderNumber) FROM OrderList"""
        number = getUniqueResult(sql)
        return 0 if number == None else int(number)
    # new

    def selectAllOrder(self):
        sql = """SELECT * FROM OrderList"""
        return getAllSet(sql)


# -----------------------------------------------------
# Table `TINYHIPPO`.`Dish`
# -----------------------------------------------------
class dishOperator:
    def __init__(self, resturantName=None, password=None):
        self.resturantID = None
        self.hasSignedIn = False
        if resturantName != None and password != None:
            self.manageDishTable(resturantName, password)

    # Sign in to manage 'Dish' table
    def manageDishTable(self, resturantName=None, password=None):
        if signIn(resturantName, password):
            rOpt = resturantOperator(resturantName, password)
            self.resturantID = rOpt.selectResturantIDWithName(resturantName)
            self.hasSignedIn = True
            self.resturantName = resturantName
            self.password = password
            print("[SUCCESS] '%s' Sign In Dish!" % resturantName)
        else:
            print('[FAILED] Username is not existed or password is wrong.')

    # Insert operator
    def insertDishItem(self, dishName, dishDescription, price, dishImageURL, dishTypeID):
        if self.hasSignedIn:
            dtOpt = dishTypeOperator(
                resturantName=self.resturantName, password=self.password)
            if dtOpt.identifyDishTypeID(dishTypeID=dishTypeID):
                # get dishTypeName
                dishtypeName = dtOpt.selectDishTypeNameWithID(
                    dishTypeID=dishTypeID)
                if not self.identifyDishName(dishName, self.resturantID):
                    sql = """INSERT INTO Dish(dishName, dishDescription, onSale, price, dishImageURL, dishComment, dishHot, monthlySales, resturantID, dishTypeID)
                            VALUES ('%s', '%s', %d, %f, '%s', '%s', %d, %d, %d, %d);""" % (dishName, dishDescription, False, float(price), dishImageURL, '', 0, 0, self.resturantID, dishTypeID)
                    executeSQL(sql)
                    print("[SUCCESS] A new Dish '%s' has been inserted into Dishtype '%s'." % (
                        dishName, dishtypeName))
                else:
                    print("[FAILED] Dish '%s' has been created in resturant '%s'" % (
                        dishName, self.resturantName))
            else:
                print("[FAILED] DishTypeID '%d' is not existed" % dishTypeID)
        else:
            print('[FAILED] Please sign in first.')

    # Delete operator
    def deleteDishItemWithDishID(self, dishID):
        if self.hasSignedIn:
            if self.identifyDishID(dishID):
                dishName = self.selectDishNameWithDishID(dishID)
                sql = """DELETE FROM Dish
                           WHERE dishID=%d;""" % dishID
                executeSQL(sql)
                print("[SUCCESS] The Dish '%s' has been deleted." % dishName)
            else:
                print("[FAILED] DishID '%d' is not existed." % dishID)
        else:
            print('[FAILED] Please sign in first.')

    def deleteDishItemsWithDishTypeID(self, dishTypeID):
        if self.hasSignedIn:
            dishIDs = self.selectDishIDsWithDishTypeID(dishTypeID)
            if dishIDs != []:
                # get dishTypeName
                dtOpt = dishTypeOperator()
                dishTypeName = dtOpt.selectDishTypeNameWithID(dishTypeID)
                for dishID in dishIDs:
                    self.deleteDishItemWithDishID(dishID)
                print(
                    "[SUCCESS] All Dishes in DishType '%s' have been deleted." % dishTypeName)
            else:
                print("[FAILED] There is no dish in DishType '%d'." %
                      dishTypeID)
        else:
            print('[FAILED] Please sign in first.')

    def deleteDishItemsWithResturantID(self, resturantID):
        if self.hasSignedIn:
            dishIDs = self.selectDishIDsWithResturantID(resturantID)
            if dishIDs != []:
                for dishID in dishIDs:
                    self.deleteDishItemWithDishID(dishID)
                print(
                    "[SUCCESS] All Dishes in Resturant '%s' have been deleted." % self.resturantName)
            else:
                print("[FAILED] There is no dish in ResturantID '%d'." %
                      resturantID)
        else:
            print('[FAILED] Please sign in first.')

    # Update operator
    def updateDishName(self, newDishName, dishID):
        if self.hasSignedIn:
            if self.identifyDishID(dishID):
                dishName = self.selectDishNameWithDishID(dishID)
                if not self.identifyDishName(dishName, self.resturantID):
                    sql = """UPDATE Dish
                                SET dishName='%s'
                                WHERE dishID=%d;""" % (newDishName, dishID)
                    executeSQL(sql)
                    print("[SUCCESS] The name of Dish '%s' has updated to '%s'." % (
                        dishName, newDishName))
                else:
                    print("[FAILED] DishName '%s' has been created." %
                          newDishName)
            else:
                print("[FAILED] DishID '%d' is not existed." % dishID)
        else:
            print('[FAILED] Please sign in first.')

    def updateDishTypeIDWithDishID(self, newDishTypeID, dishID):
        if self.hasSignedIn:
            if self.identifyDishID(dishID):
                dtOpt = dishTypeOperator(
                    resturantName=self.resturantName, password=self.password)
                if dtOpt.identifyDishTypeID(dishTypeID=newDishTypeID):
                    dishName = self.selectDishNameWithDishID(dishID)
                    sql = """UPDATE Dish
                                SET dishTypeID=%d
                                WHERE dishID=%d;""" % (newDishTypeID, dishID)
                    executeSQL(sql)
                    print("[SUCCESS] The DishTypeID of Dish '%s' has updated to '%d'." % (
                        dishName, newDishTypeID))
                else:
                    print("[FAILED] DishTypeID '%d' is not existed." %
                          newDishTypeID)
            else:
                print("[FAILED] DishID '%d' is not existed." % dishID)
        else:
            print('[FAILED] Please sign in first.')

    def updateOnSaleWithDishID(self, onSale, dishID):
        if self.hasSignedIn:
            if self.identifyDishID(dishID):
                sql = """UPDATE Dish
                            SET onSale=%d
                            WHERE dishID=%d;""" % (onSale, dishID)
                executeSQL(sql)
                dishName = self.selectDishNameWithDishID(dishID)
                onSale_str = 'True' if onSale == True else 'False'
                print("[SUCCESS] The onSale of Dish '%s' has updated to '%s'." % (
                    dishName, onSale_str))
            else:
                print("[FAILED] DishID '%d' is not existed." % dishID)
        else:
            print('[FAILED] Please sign in first.')

    def updatePriceWithDishID(self, newPrice, dishID):
        if self.hasSignedIn:
            if self.identifyDishID(dishID):
                sql = """UPDATE Dish
                            SET price=%f
                            WHERE dishID=%d;""" % (newPrice, dishID)
                executeSQL(sql)
                dishName = self.selectDishNameWithDishID(dishID)
                print("[SUCCESS] The price of Dish '%s' has updated to %.2f." % (
                    dishName, newPrice))
            else:
                print("[FAILED] DishID '%d' is not existed." % dishID)
        else:
            print('[FAILED] Please sign in first.')

    def updateDishImageURLWithDishID(self, newDishImageURL, dishID):
        if self.hasSignedIn:
            if self.identifyDishID(dishID):
                sql = """UPDATE Dish
                            SET dishImageURL='%s'
                            WHERE dishID=%d;""" % (newDishImageURL, dishID)
                executeSQL(sql)
                dishName = self.selectDishNameWithDishID(dishID)
                print("[SUCCESS] The ImageURL of Dish '%s' has updated." % dishName)
            else:
                print("[FAILED] DishID '%d' is not existed." % dishID)
        else:
            print('[FAILED] Please sign in first.')

    def updateDishCommentWithDishID(self, newDishComment, dishID):
        if self.hasSignedIn:
            if self.identifyDishID(dishID):
                # todo: comments += newComment
                sql = """UPDATE Dish
                            SET dishComment='%s'
                            WHERE dishID=%d;""" % (newDishComment, dishID)
                executeSQL(sql)
                dishName = self.selectDishNameWithDishID(dishID)
                print("[SUCCESS] The Comment of Dish '%s' has updated." % dishName)
            else:
                print("[FAILED] DishID '%d' is not existed." % dishID)
        else:
            print('[FAILED] Please sign in first.')

    def updateDishHotWithDishID(self, newDishHot, dishID):
        if self.hasSignedIn:
            if self.identifyDishID(dishID):
                sql = """UPDATE Dish
                            SET dishHot=%d
                            WHERE dishID=%d;""" % (newDishHot, dishID)
                executeSQL(sql)
                dishName = self.selectDishNameWithDishID(dishID)
                dishHot_str = 'True' if newDishHot == True else 'False'
                print("[SUCCESS] The Hot of Dish '%s' has updated to '%s'." %
                      (dishName, dishHot_str))
            else:
                print("[FAILED] DishID '%d' is not existed." % dishID)
        else:
            print('[FAILED] Please sign in first.')

    def updateMonthlySalesWithDishID(self, newMonthlySales, dishID):
        if self.hasSignedIn:
            if self.identifyDishID(dishID):
                sql = """UPDATE Dish
                            SET monthlySales=%d
                            WHERE dishID=%d;""" % (newMonthlySales, dishID)
                executeSQL(sql)
                dishName = self.selectDishNameWithDishID(dishID)
                print("[SUCCESS] The Monthly Sales of Dish '%s' has updated to '%d'." % (
                    dishName, newMonthlySales))
            else:
                print("[FAILED] DishID '%d' is not existed." % dishID)
        else:
            print('[FAILED] Please sign in first.')

    # Select operator
    def selectOnSaleWithDishID(self, dishID):
        sql = """SELECT onSale FROM Dish
                   WHERE dishID=%d""" % dishID
        return getUniqueResult(sql)

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

    def selectDishIDWithDishName(self, dishName, resturantID):
        sql = """SELECT dishID FROM Dish
                   WHERE resturantID=%d AND dishName='%s'""" % (resturantID, dishName)
        return getUniqueResult(sql)

    def selectDishNameWithDishID(self, dishID):
        sql = """SELECT dishName FROM Dish
                   WHERE dishID=%d""" % dishID
        return getUniqueResult(sql)

    def selectDishTypeIDWithDishID(self, dishID):
        sql = """SELECT dishTypeID FROM Dish
                   WHERE dishID=%d""" % dishID
        return getUniqueResult(sql)

    def selectDishIDsWithResturantID(self, resturantID):
        sql = """SELECT dishID FROM Dish
                   WHERE resturantID=%d""" % resturantID
        return getResultSet(sql)

    def selectDishIDsWithDishTypeID(self, dishTypeID):
        sql = """SELECT dishID FROM Dish
                   WHERE dishTypeID=%d""" % dishTypeID
        return getResultSet(sql)

    def identifyDishID(self, dishID):
        return dishID != '' and self.selectDishNameWithDishID(dishID) != ''

    def identifyDishName(self, dishName, resturantID):
        return dishName != '' and resturantID != '' and self.selectDishIDWithDishName(dishName, resturantID) != ''

    def selectAllDishWithDishTypeID(self, dishTypeID):
        sql = """SELECT * FROM Dish
                   WHERE dishTypeID=%d""" % (dishTypeID)
        return getResultSet(sql)
    # new

    def selectDishIDsWithDishName(self, dishName):
        sql = """SELECT dishID FROM Dish
                   WHERE dishName ='%s'""" % dishName
        return getResultSet(sql)


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

# new


def getAllSet(sql):
    cursor.execute(sql)
    results = cursor.fetchall()
    resultSet = []
    for row in results:
        resultSet.append(row)
    return resultSet
