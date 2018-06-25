import pymysql
from tools import *
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

# connect to dataset
db = pymysql.connect(host='db',
                     user='root',
                     password='tiny-hippo',
                     database='TINYHIPPO',
                     charset='utf8')
# create a cursor
cursor = db.cursor()

cursor.execute('SHOW TABLES')
tables=[] 
for row in cursor.fetchall(): tables.append(row)
for row in tables: cursor.execute('ALTER TABLE %s CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;' % (row[0]))

# create tools
tools = Tools(db=db, cursor=cursor)

## -----------------------------------------------------
## Table `TINYHIPPO`.`Restaurant`
## -----------------------------------------------------
class restaurantOperator():
    def __init__(self, restaurantName=None, password=None):
        self.restaurantID = None
        self.hasSignedIn = False
        if restaurantName != None and password != None:
            self.manageRestaurantTable(restaurantName=restaurantName, password=password)

    # Sign in to manage 'Restaurant' table
    def manageRestaurantTable(self, restaurantName, password):
        if tools.signIn(restaurantName, password):
            self.restaurantName = restaurantName
            self.password = password
            _, result = selectOperator(tableName="Restaurant", restaurantName=restaurantName, result=["restaurantID"])
            self.restaurantID = result[0]["restaurantID"]
            self.hasSignedIn = True
        else:
            print('[FAILED] Username is not existed or password is wrong.')
            
    # Insert operator
    def insertRestaurantItem(self, restaurantName, password, phone, email):
        if self.checkRestaurantItem(restaurantName=restaurantName, password=password, phone=phone, email=email):
            sql = """INSERT INTO Restaurant(restaurantName, password, phone, email)
                       VALUES ("%s", "%s", "%s", "%s");""" % (restaurantName, password, phone, email)
            tools.executeSQL(sql)
            print("[SUCCESS] Username '%s' registered." % restaurantName)
            self.manageRestaurantTable(restaurantName, password)
            return True
        return False
    
    # check restaurant item for Insert operation
    def checkRestaurantItem(self, restaurantName, password, phone, email):
        if identifyOperator(tableName="Restaurant", restaurantName=restaurantName):
            print("[FAILED] The restaurantName '%s' has been registered." % restaurantName)
            return False
        if len(password) < 6 or len(password) > 20:
            print("[FAILED] The format of password is wrong.")
            return False
        if identifyOperator(tableName="Restaurant", phone=phone):
            print("[FAILED] The phone '%s' has been registered." % phone)
            return False
        if identifyOperator(tableName="Restaurant", email=email):
            print("[FAILED] The email '%s' has been registered." % email)
            return False
        return True

    # Delete operator
    def deleteRestaurantByID(self, restaurantID):
        if self.hasSignedIn:
            if identifyOperator(tableName="Restaurant", restaurantID=restaurantID):
                # delete Restaurant Foreign Key
                # self.deleteRestaurantForeignKey(restaurantID)
                # delete Restaurant by ID
                _, result = selectOperator(tableName="Restaurant", restaurantID=restaurantID, result=["restaurantName"])
                RestaurantName = result[0]["restaurantName"]
                if RestaurantName != self.restaurantName:
                    print("[FAILED] No authority to Delete other's Restaurant items.")
                    return False
                sql = """DELETE FROM Restaurant
                           WHERE restaurantID=%d;""" % restaurantID
                tools.executeSQL(sql)
                print("[SUCCESS] Username '%s' has been deleted." % RestaurantName)
                return True
            else:
                print("[FAILED] restaurantID '%d' is not existed." % restaurantID)
        else:
            print('[FAILED] Please sign in first.')
        return False
    def deleteRestaurantByName(self, restaurantName):
        if self.hasSignedIn:
            if identifyOperator(tableName="Restaurant", restaurantName=restaurantName):
                _, result = selectOperator(tableName="Restaurant", restaurantName=restaurantName, result=["restaurantID"])
                return self.deleteRestaurantByID(result[0]["restaurantID"])
            else:
                print("[FAILED] Username '%s' is not existed." % restaurantName)
        else:
            print('[FAILED] Please sign in first.')
        return False
    def deleteRestaurantForeignKey(self, restaurantID):
        # DishType
        dtOpt = dishTypeOperator(restaurantName=self.restaurantName, password=self.password)
        dtOpt.deleteDishTypeByRestaurantID(restaurantID=self.restaurantID)
        # todo: Dish
        dOpt = dishOperator(restaurantName=self.restaurantName, password=self.password)
        # dOpt.deleteDishItemsWithRestaurantID(restaurantID=self.restaurantID)
        # Table
        tOpt = tableOperator(restaurantName=self.restaurantName, password=self.password)
        tOpt.deleteTableByRestaurantID(restaurantID=self.restaurantID)

## -----------------------------------------------------
## Table `TINYHIPPO`.`DishType`
## -----------------------------------------------------
class dishTypeOperator:
    def __init__(self, restaurantName=None, password=None):
        self.restaurantID = None
        self.hasSignedIn = False
        if restaurantName != None and password != None:
            self.manageDishTypeTable(restaurantName, password)
    
    # Sign in to manage 'DishType' table
    def manageDishTypeTable(self, restaurantName=None, password=None):
        if tools.signIn(restaurantName, password):
            self.restaurantName = restaurantName
            self.password = password
            _, result = selectOperator(tableName="Restaurant", restaurantName=restaurantName, result=["restaurantID"])
            self.restaurantID = result[0]["restaurantID"]
            self.hasSignedIn = True
            # print("[SUCCESS] '%s' Sign In DishType!" % restaurantName)
        else:
            print('[FAILED] Username is not existed or password is wrong.')

    # Insert operator
    def insertDishTypeItem(self, dishTypeName):
        if self.hasSignedIn:
            if not identifyOperator(tableName="DishType", dishTypeName=dishTypeName, restaurantID=self.restaurantID):
                sql = """INSERT INTO DishType(dishTypeName, restaurantID)
                           VALUES ("%s", %d);""" % (dishTypeName, self.restaurantID)
                tools.executeSQL(sql)
                print("[SUCCESS] DishTypeName '%s' inserted to DishType." % dishTypeName)
                return True
            else:
                print("[FAILED] DishTypeName '%s' has been created." % dishTypeName)
        else:
            print('[FAILED] Please sign in first.')
        return False

    # Delete operator
    def deleteDishTypeByID(self, dishTypeID):
        if self.hasSignedIn:
            if identifyOperator(tableName="DishType", dishTypeID=dishTypeID):
                # check authority of restaurant
                _, result = selectOperator(tableName="DishType", dishTypeID=dishTypeID, result=["restaurantID"])
                restaurantID = result[0]["restaurantID"]
                if restaurantID != self.restaurantID:
                    print("[FAILED] No authority to Delete other's DishType items.")
                    return False
                # delete DishType by ID
                _, result = selectOperator(tableName="DishType", dishTypeID=dishTypeID, result=["dishTypeName"])
                dishTypeName = result[0]["dishTypeName"]
                sql = """DELETE FROM DishType
                           WHERE dishTypeID=%d;""" % dishTypeID
                tools.executeSQL(sql)
                print("[SUCCESS] DishTypeName '%s' has been deleted." % dishTypeName)
                return True
            else:
                print("[FAILED] DishTypeID '%d' is not existed." % dishTypeID)
        else:
            print('[FAILED] Please sign in first.')
        return False
    def deleteDishTypeByName(self, dishTypeName):
        if self.hasSignedIn:
            if identifyOperator(tableName="DishType", dishTypeName=dishTypeName):
                _, result = selectOperator(tableName="DishType", dishTypeName=dishTypeName, result=["dishTypeID"])
                dishTypeID = result[0]["dishTypeID"]
                return self.deleteDishTypeByID(dishTypeID)
            else:
                print("[FAILED] dishTypeName '%s' is not existed." % dishTypeName)
        else:
            print("[FAILED] Username is not existed or password is wrong.")
        return False
    def deleteDishTypeByRestaurantID(self, restaurantID):
        if self.hasSignedIn:
            _, result = selectOperator(tableName="DishType", restaurantID=restaurantID, result=["dishTypeID"])
            for r in result:
                self.deleteDishTypeByID(r["dishTypeID"])
            print("[SUCCESS] Delete all restaurantID '%d' in DishType." % restaurantID)
        else:
            print('[FAILED] Please sign in first.')

## -----------------------------------------------------
## Table `TINYHIPPO`.`RestaurantTable`
## -----------------------------------------------------
class tableOperator:
    def __init__(self, restaurantName=None, password=None):
        self.restaurantID = None
        self.hasSignedIn = False
        if restaurantName != None and password != None:
            self.manageTableTable(restaurantName, password)
    
    # Sign in to manage 'RestaurantTable' table
    def manageTableTable(self, restaurantName=None, password=None):
        if tools.signIn(restaurantName, password):
            self.restaurantName = restaurantName
            self.password = password
            _, result = selectOperator(tableName="Restaurant", restaurantName=restaurantName, result=["restaurantID"])
            self.restaurantID = result[0]["restaurantID"]
            self.hasSignedIn = True
            # print("[SUCCESS] '%s' Sign In RestaurantTable!" % restaurantName)
        else:
            print('[FAILED] Username is not existed or password is wrong.')
    # Insert operator
    def insertTableItem(self, tableNumber):
        if self.hasSignedIn:
            if not identifyOperator(tableName="RestaurantTable", tableNumber=tableNumber, restaurantID=self.restaurantID):
                sql = """INSERT INTO RestaurantTable(tableNumber, currentOrderNumber, restaurantID)
                           VALUES (%d, %d, %d);""" % (tableNumber, -1, self.restaurantID)
                tools.executeSQL(sql)
                print("[SUCCESS] TableNumber '%d' inserted to RestaurantTable." % tableNumber)
                return True
            else:
                print("[FAILED] TableNumber '%d' has been created." % tableNumber)
        else:
            print('[FAILED] Please sign in first.')
        return False

    # Delete operator
    def deleteTableByID(self, tableID):
        if self.hasSignedIn:
            if identifyOperator(tableName="RestaurantTable", tableID=tableID):
                # check authority of restaurant
                _, result = selectOperator(tableName="RestaurantTable", tableID=tableID, result=["restaurantID"])
                restaurantID = result[0]["restaurantID"]
                if restaurantID != self.restaurantID:
                    print("[FAILED] No authority to Delete other's RestaurantTable items.")
                    return False
                # delete RestaurantTable item by ID
                _, result = selectOperator(tableName="RestaurantTable", tableID=tableID, result=["tableNumber"])
                tableNumber = result[0]["tableNumber"]
                sql = """DELETE FROM RestaurantTable
                           WHERE tableID=%d;""" % tableID
                tools.executeSQL(sql)
                print("[SUCCESS] RestaurantTable '%d' has been deleted." % tableNumber)
                return True
            else:
                print("[FAILED] RestaurantTable '%d' is not existed." % tableID)
        else:
            print('[FAILED] Please sign in first.')
        return False
    def deleteTableByNumber(self, tableNumber):
        if self.hasSignedIn:
            if identifyOperator(tableName="RestaurantTable", tableNumber=tableNumber, restaurantID=self.restaurantID):
                _, result = selectOperator(tableName="RestaurantTable", tableNumber=tableNumber, restaurantID=self.restaurantID, result=["tableID"])
                tableID = result[0]["tableID"]
                return self.deleteTableByID(tableID)
            else:
                print("[FAILED] TableNumber '%d' is not existed." % tableNumber)
        else:
            print('[FAILED] Please sign in first.')
        return False
    def deleteTableByRestaurantID(self, restaurantID):
        if self.hasSignedIn:
            _, result = selectOperator(tableName="RestaurantTable", restaurantID=restaurantID, result=["tableID"])
            for r in result:
                self.deleteTableByID(tableID=r["tableID"])
            print("[SUCCESS] Delete all restaurantID '%d' in RestaurantTable." % restaurantID)
            return True
        else:
            print('[FAILED] Please sign in first.')
        return False


## -----------------------------------------------------
## Table `TINYHIPPO`.`QRlink`
## -----------------------------------------------------
class QRlinkOperator:
    def __init__(self, restaurantName=None, password=None):
        self.restaurantID = None
        self.hasSignedIn = False
        if restaurantName != None and password != None:
            self.manageQRlinkTable(restaurantName, password)
    
    # Sign in to manage 'QRlink' table
    def manageQRlinkTable(self, restaurantName=None, password=None):
        if tools.signIn(restaurantName, password):
            self.restaurantName = restaurantName
            self.password = password
            _, result = selectOperator(tableName="Restaurant", restaurantName=restaurantName, result=["restaurantID"])
            self.restaurantID = result[0]["restaurantID"]
            self.hasSignedIn = True
            # print("[SUCCESS] '%s' Sign In QRlink!" % restaurantName)
        else:
            print('[FAILED] Username is not existed or password is wrong.')
    # Insert operator
    def insertQRlinkItem(self, linkImageURL, tableNumber):
        if self.hasSignedIn:
            if identifyOperator(tableName="RestaurantTable", tableNumber=tableNumber, restaurantID=self.restaurantID):
                _, result = selectOperator(tableName="RestaurantTable", tableNumber=tableNumber, restaurantID=self.restaurantID, result=["tableID"])
                tableID = result[0]["tableID"]
                if not identifyOperator(tableName="QRlink", tableID=tableID):
                    if not identifyOperator(tableName="QRlink", linkImageURL=linkImageURL):
                        sql = """INSERT INTO QRlink(linkImageURL, tableID)
                                VALUES ("%s", %d);""" % (linkImageURL, tableID)
                        tools.executeSQL(sql)
                        print("[SUCCESS] linkImageURL '%s' has been inserted to QRlink." % linkImageURL)
                        return True
                    else:
                        print("[FAILED] linkImageURL '%s' has been created." % linkImageURL)
                else:
                    print("[FAILED] tableID '%d' already has QR link." % tableID)
            else:
                print("[FAILED] tableNumber '%d' is not existed." % tableNumber)
        else:
            print('[FAILED] Please sign in first.')
        return False

    # Delete operator
    def deleteLinkByID(self, linkID):
        if self.hasSignedIn:
            if identifyOperator(tableName="QRlink", linkID=linkID):
                # get table ID
                _, result = selectOperator(tableName="QRlink", linkID=linkID, result=["tableID"])
                tableID = result[0]["tableID"]
                # check authority of restaurant
                _, result = selectOperator(tableName="RestaurantTable", tableID=tableID, result=["restaurantID"])
                restaurantID = result[0]["restaurantID"]
                if restaurantID != self.restaurantID:
                    print("[FAILED] No authority to Delete other's QRlink items.")
                    return False
                # delete QRlink item by ID
                sql = """DELETE FROM QRlink
                           WHERE linkID=%d;""" % linkID
                tools.executeSQL(sql)
                print("[SUCCESS] The QRlink of TableID '%d' has been deleted." % tableID)
                return True
            else:
                print("[FAILED] LinkID '%d' is not existed." % linkID)
        else:
            print('[FAILED] Please sign in first.')
        return False
    def deleteLinkByURL(self, linkImageURL):
        if self.hasSignedIn:
            if identifyOperator(tableName="QRlink", linkImageURL=linkImageURL):
                _, result = selectOperator(tableName="QRlink", linkImageURL=linkImageURL, result=["linkID"])
                linkID = result[0]["linkID"]
                return self.deleteLinkByID(linkID)
            else:
                print("[FAILED] linkImageURL '%s' is not existed." % linkImageURL)
        else:
            print('[FAILED] Please sign in first.')
        return False
    def deleteLinkByTableID(self, tableID):
        if self.hasSignedIn:
            _, result = selectOperator(tableName="QRlink", tableID=tableID, result=["linkID"])
            linkID = result[0]["linkID"]
            if identifyOperator(tableName="QRlink", linkID=linkID):
                sql = """DELETE FROM QRlink
                           WHERE tableID=%d;""" % tableID
                tools.executeSQL(sql)
                print("[SUCCESS] Delete tableID '%d'." % tableID)
                return True
            else:
                print("[FAILED] TableID '%d' is not existed." % tableID)
        else:
            print('[FAILED] Please sign in first.')
        return False

## -----------------------------------------------------
## Table `TINYHIPPO`.`Dish`
## -----------------------------------------------------
class dishOperator:
    def __init__(self, restaurantName=None, password=None):
        self.restaurantID = None
        self.hasSignedIn = False
        if restaurantName != None and password != None:
            self.manageDishTable(restaurantName, password)

    # Sign in to manage 'Dish' table
    def manageDishTable(self, restaurantName=None, password=None):
        if tools.signIn(restaurantName, password):
            self.restaurantName = restaurantName
            self.password = password
            _, result = selectOperator(tableName="Restaurant", restaurantName=restaurantName, result=["restaurantID"])
            self.restaurantID = result[0]["restaurantID"]
            self.hasSignedIn = True
            # print("[SUCCESS] '%s' Sign In Dish!" % restaurantName)
        else:
            print('[FAILED] Username is not existed or password is wrong.')

    # Insert operator
    def insertDishItem(self, dishName, dishDescription, price, dishImageURL, dishTypeID):
        if self.hasSignedIn:
            if identifyOperator(tableName="DishType", dishTypeID=dishTypeID):
                # get dishTypeName
                _, result = selectOperator(tableName="DishType", dishTypeID=dishTypeID, result=["dishTypeName"])
                dishTypeName = result[0]["dishTypeName"]
                if not identifyOperator(tableName="Dish", dishName=dishName, restaurantID=self.restaurantID):
                    sql = """INSERT INTO Dish(dishName, dishDescription, onSale, price, dishImageURL, dishHot, monthlySales, restaurantID, dishTypeID)
                               VALUES ("%s", "%s", %d, %f, "%s", %d, %d, %d, %d);""" % (dishName, dishDescription, False, float(price), dishImageURL, 0, 0, self.restaurantID, dishTypeID)
                    tools.executeSQL(sql)
                    print("[SUCCESS] A new Dish '%s' has been inserted into Dishtype '%s'." % (dishName, dishTypeName))
                    return True
                else:
                    print("[FAILED] Dish '%s' has been created in restaurant '%s'" % (dishName, self.restaurantName))
            else:
                print("[FAILED] DishTypeID '%d' is not existed" % dishTypeID)
        else:
            print('[FAILED] Please sign in first.')
        return False
    
    # Delete operator
    def deleteDishItemWithDishID(self, dishID):
        if self.hasSignedIn:
            if identifyOperator(tableName="Dish", dishID=dishID):
                # check authority of restaurant
                _, result = selectOperator(tableName="Dish", dishID=dishID, result=["restaurantID"])
                restaurantID = result[0]["restaurantID"]
                if restaurantID != self.restaurantID:
                    print("[FAILED] No authority to Delete other's Dish items.")
                    return False
                # get dish name
                _, result = selectOperator(tableName="Dish", dishID=dishID, result=["dishName"])
                dishName = result[0]["dishName"]
                # delete dish by id
                sql = """DELETE FROM Dish
                           WHERE dishID=%d;""" % dishID
                tools.executeSQL(sql)
                print("[SUCCESS] The Dish '%s' has been deleted." % dishName)
                return True
            else:
                print("[FAILED] DishID '%d' is not existed." % dishID)
        else:
            print('[FAILED] Please sign in first.')
        return False
    def deleteDishItemsWithDishTypeID(self, dishTypeID):
        if self.hasSignedIn:
            _, result = selectOperator(tableName="Dish", dishTypeID=dishTypeID, result=["dishID"])
            if len(result) != 0:
                # get dishTypeName
                _, dtN_result = selectOperator(tableName="DishType", dishTypeID=dishTypeID, result=["dishTypeName"])
                dishTypeName = dtN_result[0]["dishTypeName"]

                for r in result:
                    self.deleteDishItemWithDishID(dishID=r["dishID"])
                print("[SUCCESS] All Dishes in DishType '%s' have been deleted." % dishTypeName)
                return True
            else:
                print("[FAILED] There is no dish in DishType '%d'." % dishTypeID)
        else:
            print('[FAILED] Please sign in first.')
        return False
    def deleteDishItemsWithRestaurantID(self, restaurantID):
        if self.hasSignedIn:
            if restaurantID == self.restaurantID:
                _, result = selectOperator(tableName="Dish", restaurantID=restaurantID, result=["dishID"])
                if len(result) != 0:
                    for r in result:
                        self.deleteDishItemWithDishID(dishID=r["dishID"])
                    print("[SUCCESS] All Dishes in Restaurant '%s' have been deleted." % self.restaurantName)
                    return True
                else:
                    print("[FAILED] There is no dish in RestaurantID '%d'." % restaurantID)
            else:
                print("[FAILED] No authority to Delete other's Dish items.")
        else:
            print('[FAILED] Please sign in first.')
        return False

## -----------------------------------------------------
## Table `TINYHIPPO`.`DishComment`
## -----------------------------------------------------
class dishCommentOperator:
    # Insert operator
    def insertDishTypeItem(self, comment, dishID):
        if identifyOperator(tableName="Dish", dishID=dishID):
            _, result = selectOperator(tableName="Dish", dishID=dishID, result=["dishName"])
            dishName = result[0]["dishName"]
            sql = """INSERT INTO DishComment(comment, dishID)
                       VALUES ('%s', %d);""" % (comment, dishID)
            tools.executeSQL(sql)
            print("[SUCCESS] A new comment inserted to Dish '%s'." % dishName)
            return True
        print("[FAILED] dishID '%d' is not existed." % dishID)
        return False

    # Delete operator
    def deleteDishCommentByCommentID(self, dishCommentID):
        if identifyOperator(tableName="DishComment", dishCommentID=dishCommentID):
            # delete DishComment by dishCommentID
            _, result = selectOperator(tableName="DishComment", dishCommentID=dishCommentID, result=["dishID"])
            dishID = result[0]["dishID"]
            sql = """DELETE FROM DishComment
                           WHERE dishCommentID=%d;""" % dishCommentID
            tools.executeSQL(sql)
            print("[SUCCESS] A comment of DishID '%d' has been deleted." % dishID)
            return True
        print("[FAILED] DishCommentID '%d' is not existed." % dishCommentID)
        return False
    def deleteDishCommentsWithDishID(self, dishID):
        if identifyOperator(tableName="DishComment", dishID=dishID):
            _, result = selectOperator(tableName="DishComment", dishID=dishID, result=["dishCommentID"])
            if len(result) != 0:
                for r in result:
                    self.deleteDishCommentByCommentID(dishCommentID=r["dishCommentID"])
                print("[SUCCESS] All DishComments for DishID '%d' have been deleted." % dishID)
                return True
        print("[FAILED] DishID '%d' is not existed in Table 'DishComment'." % dishID)
        return False

## -----------------------------------------------------
## Table `TINYHIPPO`.`OrderList`
## -----------------------------------------------------
class orderListOperator:
    def __init__(self, restaurantName=None, password=None):
        self.restaurantID = None
        self.hasSignedIn = False
        if restaurantName != None and password != None:
            self.manageOrderListTable(restaurantName, password)

    # Sign in to manage 'OrderList' table
    def manageOrderListTable(self, restaurantName=None, password=None):
        if tools.signIn(restaurantName, password):
            self.restaurantName = restaurantName
            self.password = password
            _, result = selectOperator(tableName="Restaurant", restaurantName=restaurantName, result=["restaurantID"])
            self.restaurantID = result[0]["restaurantID"]
            self.hasSignedIn = True
            # print("[SUCCESS] '%s' Sign In DishComment!" % restaurantName)
        else:
            print('[FAILED] Username is not existed or password is wrong.')

    # Insert operator
    def insertOrderItem(self, orderDetail, total, customerID, tableID):
        '''
        Input:
            orderDishes: the json of dishes in the order
            total: the total of the order
        '''
        if self.hasSignedIn:
            now = tools.getNow()
            # determine orderNumber
            if identifyOperator(tableName="RestaurantTable", tableID=tableID):
                # get orderNumber
                _, result = selectOperator(tableName="RestaurantTable", tableID=tableID, result=["currentOrderNumber"])
                orderNumber = result[0]["currentOrderNumber"]
                if orderNumber == -1:
                    # todo: collision
                    orderNumber = self.getMaxNumber() + 1
                    updateOperator(rstName=self.restaurantName, pwd=self.password, tableName="RestaurantTable", tableID=tableID, new_currentOrderNumber=orderNumber)
                sql = """INSERT INTO OrderList(orderNumber, orderDetail, total, isPaid, status, editedTime, customerID, tableID, restaurantID)
                            VALUES (%d, "%s", %f, %d, "%s", "%s", "%s", %d, %d);""" % (orderNumber, orderDetail, total, False, 'todo', now, customerID, tableID, self.restaurantID)
                tools.executeSQL(sql)
                print("[SUCCESS] A new Order '%d' has been inserted to Table." % orderNumber)
                return orderNumber
            else:
                print("[FAILED] TableID '%d' is not existed." % tableID)
        else:
            print('[FAILED] Please sign in first.')
        return -1

    # Delete operator
    def deleteOrderItemWithOrderID(self, orderID):
        if self.hasSignedIn:
            if identifyOperator(tableName="OrderList", orderID=orderID):
                # check authority of restaurant
                _, result = selectOperator(tableName="OrderList", orderID=orderID, result=["restaurantID"])
                restaurantID = result[0]["restaurantID"]
                if restaurantID != self.restaurantID:
                    print("[FAILED] No authority to Delete other's Dish items.")
                    return False
                # delete OrderList by ID
                sql = """DELETE FROM OrderList
                            WHERE orderID=%d;""" % orderID
                tools.executeSQL(sql)
                print("[SUCCESS] The OrderID '%d' has been deleted." % orderID)
                return True
            else:
                print("[FAILED] OrderID '%d' is not existed." % orderID)
        else:
            print('[FAILED] Please sign in first.')
        return False
    def deleteOrderItemsWithTableID(self, tableID):
        if self.hasSignedIn:
            if identifyOperator(tableName="RestaurantTable", tableID=tableID):
                # check authority of restaurant
                _, result = selectOperator(tableName="RestaurantTable", tableID=tableID, result=["restaurantID"])
                restaurantID = result[0]["restaurantID"]
                if restaurantID != self.restaurantID:
                    print("[FAILED] No authority to Delete other's Dish items.")
                    return False
                # delete OrderItems by tableID
                sql = """DELETE FROM OrderList
                           WHERE tableID=%d;""" % tableID
                tools.executeSQL(sql)
                print("[SUCCESS] Delete OrderList items which stored tableID '%d'." % tableID)
                return False
            else:
                print("[FAILED] TableID '%d' is not existed." % tableID)
        else:
            print('[FAILED] Please sign in first.')
        return False
    def getMaxNumber(self):
        sql = """SELECT MAX(orderNumber) FROM OrderList"""
        cursor.execute(sql)
        results = cursor.fetchall()
        number = results[0][0]
        return 0 if number == None else int(number)

## -----------------------------------------------------
## Table `TINYHIPPO`.`Recommendation`
## -----------------------------------------------------
class RecommendationOperator:
    def __init__(self, restaurantName=None, password=None):
        self.restaurantID = None
        self.hasSignedIn = False
        if restaurantName != None and password != None:
            self.manageRecommendationTable(restaurantName, password)
    
    # Sign in to manage 'Recommendation' table
    def manageRecommendationTable(self, restaurantName=None, password=None):
        if tools.signIn(restaurantName, password):
            self.restaurantName = restaurantName
            self.password = password
            _, result = selectOperator(tableName="Restaurant", restaurantName=restaurantName, result=["restaurantID"])
            self.restaurantID = result[0]["restaurantID"]
            self.hasSignedIn = True
            # print("[SUCCESS] '%s' Sign In Recommendation!" % restaurantName)
        else:
            print('[FAILED] Username is not existed or password is wrong.')
    # Insert operator
    def insertRecommendationItem(self, title, tag, imageURL):
        if self.hasSignedIn:
            now = tools.getNow()
            sql = """INSERT INTO Recommendation(title, tag, imageURL, editedTime, restaurantID)
                    VALUES ("%s", "%s", "%s", "%s", %d);""" % (title, tag, imageURL, now, self.restaurantID)
            tools.executeSQL(sql)
            print("[SUCCESS] A new recommendation '%s' inserted to Recommendation." % title)
            return True
        else:
            print('[FAILED] Please sign in first.')
        return False
    # Delete operator
    def deleteDishCommentByCommentID(self, recommendationID):
        if self.hasSignedIn:
            if identifyOperator(tableName="Recommendation", recommendationID=recommendationID):
                # check authority of restaurant
                _, result = selectOperator(tableName="Recommendation", recommendationID=recommendationID, result=["restaurantID"])
                restaurantID = result[0]["restaurantID"]
                if restaurantID != self.restaurantID:
                    print("[FAILED] No authority to Delete other's Recommendation items.")
                    return False
                # delete Recommendation by recommendationID
                _, result = selectOperator(tableName="Recommendation", recommendationID=recommendationID, result=["title"])
                title = result[0]["title"]
                sql = """DELETE FROM Recommendation
                            WHERE recommendationID=%d;""" % recommendationID
                tools.executeSQL(sql)
                print("[SUCCESS] Recommendation '%s' has been deleted." % title)
                return True
            else:
                print("[FAILED] recommendationID '%d' is not existed." % recommendationID)
        else:
            print('[FAILED] Please sign in first.')
        return False

## -----------------------------------------------------
## Table `TINYHIPPO`.`RecommendationDetails`
## -----------------------------------------------------
class RecommendationDetailsOperator:
    # Insert operator
    def insertRecommendationDetailsItem(self, recommendationID, dishID, description):
        if identifyOperator(tableName="Recommendation", recommendationID=recommendationID):
            if identifyOperator(tableName="Dish", dishID=dishID):
                # check whether recommendationID and dishID are from same restaurant
                _, result = selectOperator(tableName="Recommendation", recommendationID=recommendationID, result=["restaurantID"])
                restaurantID1 = result[0]["restaurantID"]
                _, result = selectOperator(tableName="Dish", dishID=dishID, result=["restaurantID"])
                restaurantID2 = result[0]["restaurantID"]
                if restaurantID1 != restaurantID2:
                    print("[FAILED] The recommendationID '%d' and the dishID '%d' are not from same restaurant." % (recommendationID, dishID))
                    return False
                sql = """INSERT INTO RecommendationDetails(recommendationID, dishID, description)
                           VALUES (%d, %d, "%s");""" % (recommendationID, dishID, description)
                tools.executeSQL(sql)
                print("[SUCCESS] A new relationship between Table 'Dish' and Table 'Recommendation' created.")
                return True
            else:
                print("[FAILED] dishID '%d' is not existed." % dishID)
        else:
            print("[FAILED] recommendationID '%d' is not existed." % recommendationID)
        return False

    # Delete operator
    def deleteRecommendationDetailsByRecommendationID(self, recommendationID):
        if identifyOperator(tableName="RecommendationDetails", recommendationID=recommendationID):
            # delete RecommendationDetails item by recommendationID
            sql = """DELETE FROM RecommendationDetails
                       WHERE recommendationID=%d;""" % recommendationID
            tools.executeSQL(sql)
            print("[SUCCESS] All RecommendationDetails items whose recommendationID is '%d' has been delete." % recommendationID)
            return True
        print("[FAILED] recommendationID '%d' is not existed." % recommendationID)
        return False
    def deleteRecommendationDetailsByDishID(self, dishID):
        if identifyOperator(tableName="RecommendationDetails", dishID=dishID):
            # delete RecommendationDetails item by recommendationID
            sql = """DELETE FROM RecommendationDetails
                       WHERE dishID=%d;""" % dishID
            tools.executeSQL(sql)
            print("[SUCCESS] All RecommendationDetails items whose dishID is '%d' has been delete." % dishID)
            return True
        print("[FAILED] dishID '%d' is not existed." % dishID)
        return False

def identifyOperator(tableName, **kwargs):
    staus, result = selectOperator(tableName, **kwargs)
    return staus and len(result) != 0

def selectOperator(tableName, **kwargs):
    '''
    Input:
        tableName: the name of the table
        **kwargs: key-value of table
    Output:
        the status of selection
        the result for the selection
    '''
    # check the correction of keys
    keys = tools.getTableKeys(tableName=tableName)
    if not keys:
        return False, []
    if "result" not in kwargs:
        kwargs["result"] = [keys[0]]
    keys.append("result")
    if not tools.checkKeysCorrection(input=kwargs, valid_keys=keys):
        return False, []
    result_str = ", ".join(key for key in kwargs["result"])
    condition_str = " AND ".join('{}="{}"'.format(key, kwargs[key]) for key in kwargs.keys() if key != 'result')
    sql = """SELECT %s FROM %s
               WHERE %s""" % (result_str, tableName, condition_str)
    result = tools.getResults(sql, keys=kwargs["result"])
    return True, result

def selectUniqueItem(tableName, **kwargs):
    '''
    Input:
        tableName: the name of the table
        **kwargs: key-value of table
    Output:
        the status of selection
        the result for the selection
    '''
    if len(kwargs["result"]) != 1:
        print("[FAILED] The number of 'result' is not one.")
        return ''
    key = kwargs["result"][0]
    _, result = selectOperator(tableName=tableName, **kwargs)
    unique = ''
    if len(result) == 1:
        unique = result[0][key]
    return unique

def updateOperator(rstName, pwd, tableName, **kwargs):
    '''
    Input:
        rstName: the name of the restaurant
        pwd: the password of the restaurant
        tableName: the name of the table
        **kwargs: one key-value of table
    Output:
        the status of updating
    '''
    # identify the number of input
    if len([key for key in kwargs.keys() if 'new' in key]) != 1:
        print('[FAILED] The number of input is invalid.')
        return False
    # identify the restaurantName and password
    if not identifyOperator(tableName="Restaurant", **{"restaurantName" : rstName, "password" : pwd}):
        print('[FAILED] Username is not existed or password is wrong.')
        return False
    # check the correction of keys
    keys = tools.getTableKeys(tableName=tableName)
    if not keys:
        return False
    new_keys = keys.copy()
    for key in keys:
        new_keys.append("new_%s" % key)
    if not tools.checkKeysCorrection(input=kwargs, valid_keys=new_keys):
        return False
    # generate sql sentence
    result_str = ", ".join("{}='{}'".format(key.replace("new_", ""), kwargs[key]) for key in kwargs.keys() if 'new' in key)
    condition_str = " AND ".join('{}="{}"'.format(key, kwargs[key]) for key in kwargs.keys() if 'new' not in key)
    condition = {}
    for key in kwargs.keys():
        if 'new' not in key:
            condition[key] = kwargs[key]
    # execute sql
    if identifyOperator(tableName=tableName, **condition):
        try:
            sql = """UPDATE %s
                       SET %s
                       WHERE %s;""" % (tableName, result_str , condition_str)
            tools.executeSQL(sql)
            print("[SUCCESS] %s has been updated to %s." % (result_str.split("=")[0], result_str.split("=")[1]) )
            return True
        except:
            print("[FAILED] %s %s has been existed." % (result_str.split("=")[0], result_str.split("=")[1]) )
    else:
        print("[FAILED] CONDITION ' %s ' is not found." % condition_str)
        return False