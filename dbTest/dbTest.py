from dbOperators import *
from tools import *

## -----------------------------------------------------
## Table `TINYHIPPO`.`Restaurant`
## -----------------------------------------------------
print("---------- Test for 'Restaurant' ----------")
rOpt = restaurantOperator()
# insert
rOpt.insertRestaurantItem(restaurantName='rName1', password='123456', phone='10293847567', email='rName1@mail.com')
rOpt.insertRestaurantItem(restaurantName='rName1', password='123456', phone='10293847568', email='rName2@mail.com')
rOpt.insertRestaurantItem(restaurantName='rName2', password ='12345', phone='10293847568', email='rName2@mail.com')
rOpt.insertRestaurantItem(restaurantName='rName2', password='111111111111111111111', phone='10293847568', email='rName2@mail.com')
rOpt.insertRestaurantItem(restaurantName='rName2', password='123456', phone='10293847567', email='rName2@mail.com')
rOpt.insertRestaurantItem(restaurantName='rName2', password='123456', phone='10293847568', email='rName1@mail.com')
rOpt.insertRestaurantItem(restaurantName='rName2', password='123456', phone='10293847568', email='rName2@mail.com')
# select
print( selectOperator(tableName="Restaurants", restaurantName='rName1', result=["restaurantID"]) )
print( selectOperator(tableName="Restaurant", restaurantName='rName1', result=["restaurantIDs"]) )
print( selectOperator(tableName="Restaurant", restaurantName='rName1', result=["restaurantID"]) )
print( selectOperator(tableName="Restaurant", restaurantName='rName1', phone='10293847567', result=["restaurantID", "email"]))
print( selectOperator(tableName="Restaurant", restaurantName='rName3', result=["restaurantID"]) )
print( selectOperator(tableName="Restaurant", restaurantName='rName3', phone='10293847567', result=["restaurantID"]))
# update
updateOperator(rstName='null', pwd='123456', tableName='Restaurant', restaurantName='rName1', new_password='1234567')
updateOperator(rstName='rName1', pwd='123456', tableName='Restaurants', restaurantName='rName1', new_password='1234567')
updateOperator(rstName='rName1', pwd='1234567', tableName='Restaurant', restaurantName='rName1', new_phone='10293847569', new_restaurantName='rName2')
updateOperator(rstName='rName1', pwd='123456', tableName='Restaurant', restaurantName='rName1', new_password='1234567')
updateOperator(rstName='rName1', pwd='1234567', tableName='Restaurant', restaurantName='rName1', new_restaurantName='rName2')
# delete
rOpt = restaurantOperator()
rOpt.deleteRestaurantByID(restaurantID=2)
rOpt.manageRestaurantTable(restaurantName='rName1', password='1234567')
rOpt.deleteRestaurantByID(restaurantID=3)
rOpt.deleteRestaurantByName(restaurantName="rName2")
rOpt.deleteRestaurantByID(restaurantID=1)
rOpt.manageRestaurantTable(restaurantName='rName2', password='123456')
rOpt.deleteRestaurantByName(restaurantName="rName2")

## -----------------------------------------------------
## Table `TINYHIPPO`.`DishType`
## -----------------------------------------------------
# initialize
rOpt = restaurantOperator()
rOpt.insertRestaurantItem(restaurantName='rName1', password='123456', phone='10293847567', email='rName1@mail.com')
rOpt.insertRestaurantItem(restaurantName='rName2', password='123456', phone='10293847568', email='rName2@mail.com')

print("\n---------- Test for 'DishType' ----------")
# insert
dtOpt = dishTypeOperator()
dtOpt.insertDishTypeItem(dishTypeName="dtype1")
dtOpt.manageDishTypeTable(restaurantName='rName1', password='123456')
dtOpt.insertDishTypeItem(dishTypeName="dtype1")
dtOpt.insertDishTypeItem(dishTypeName="dtype1")
dtOpt.insertDishTypeItem(dishTypeName="dtype2")
dtOpt.manageDishTypeTable(restaurantName='rName2', password='123456')
dtOpt.insertDishTypeItem(dishTypeName="dtype1")
dtOpt.insertDishTypeItem(dishTypeName="dtype3")
# delete
dtOpt = dishTypeOperator()
dtOpt.deleteDishTypeByID(dishTypeID=1)
dtOpt.manageDishTypeTable(restaurantName='rName1', password='123456')
dtOpt.deleteDishTypeByID(dishTypeID=3)
dtOpt.deleteDishTypeByID(dishTypeID=5)
dtOpt.deleteDishTypeByName(dishTypeName="dtype3")
dtOpt.deleteDishTypeByName(dishTypeName="dtype5")
dtOpt.deleteDishTypeByID(dishTypeID=1)
dtOpt.deleteDishTypeByName(dishTypeName="dtype2")

## -----------------------------------------------------
## Table `TINYHIPPO`.`RestaurantTable`
## -----------------------------------------------------
print("\n---------- Test for 'RestaurantTable' ----------")
# insert
tOpt = tableOperator()
tOpt.insertTableItem(tableNumber=1)
tOpt.manageTableTable(restaurantName='rName1', password='123456')
tOpt.insertTableItem(tableNumber=1)
tOpt.insertTableItem(tableNumber=1)
tOpt.insertTableItem(tableNumber=2)
tOpt.manageTableTable(restaurantName='rName2', password='123456')
tOpt.insertTableItem(tableNumber=1)
tOpt.insertTableItem(tableNumber=3)
# delete
tOpt = tableOperator()
tOpt.deleteTableByID(tableID=1)
tOpt.manageTableTable(restaurantName='rName1', password='123456')
tOpt.deleteTableByID(tableID=3)
tOpt.deleteTableByID(tableID=5)
tOpt.deleteTableByNumber(tableNumber=3)
tOpt.deleteTableByNumber(tableNumber=5)
tOpt.deleteTableByID(tableID=1)
tOpt.deleteTableByNumber(tableNumber=2)

## -----------------------------------------------------
## Table `TINYHIPPO`.`QRlink`
## -----------------------------------------------------
# initialize
tOpt = tableOperator()
tOpt.manageTableTable(restaurantName='rName1', password='123456')
tOpt.insertTableItem(tableNumber=1)
tOpt.insertTableItem(tableNumber=2)

print("\n---------- Test for 'QRlink' ----------")
# insert
qrOpt = QRlinkOperator()
qrOpt.insertQRlinkItem(linkImageURL="http://qrlink1.com", tableNumber=1)
qrOpt.manageQRlinkTable(restaurantName='rName1', password='123456')
qrOpt.insertQRlinkItem(linkImageURL="http://qrlink1.com", tableNumber=1)
qrOpt.insertQRlinkItem(linkImageURL="http://qrlink1.com", tableNumber=2)
qrOpt.insertQRlinkItem(linkImageURL="http://qrlink2.com", tableNumber=1)
qrOpt.insertQRlinkItem(linkImageURL="http://qrlink2.com", tableNumber=2)
qrOpt.manageQRlinkTable(restaurantName='rName2', password='123456')
qrOpt.insertQRlinkItem(linkImageURL="http://qrlink1.com", tableNumber=1)
qrOpt.insertQRlinkItem(linkImageURL="http://qrlink3.com", tableNumber=1)
qrOpt.insertQRlinkItem(linkImageURL="http://qrlink4.com", tableNumber=3)
# delete
qrOpt = QRlinkOperator()
qrOpt.deleteLinkByID(linkID=1)
qrOpt.manageQRlinkTable(restaurantName='rName1', password='123456')
qrOpt.deleteLinkByID(linkID=3)
qrOpt.deleteLinkByID(linkID=5)
qrOpt.deleteLinkByURL(linkImageURL="http://qrlink3.com")
qrOpt.deleteLinkByURL(linkImageURL="http://qrlink5.com")
qrOpt.deleteLinkByID(linkID=1)
qrOpt.deleteLinkByURL(linkImageURL="http://qrlink2.com")

## -----------------------------------------------------
## Table `TINYHIPPO`.`Dish`
## -----------------------------------------------------
# initialize
dtOpt = dishTypeOperator()
dtOpt.manageDishTypeTable(restaurantName='rName1', password='123456')
dtOpt.insertDishTypeItem(dishTypeName="dtype1")
dtOpt.insertDishTypeItem(dishTypeName="dtype2")

print("\n---------- Test for 'Dish' ----------")
# insert
dOpt = dishOperator()
dOpt.insertDishItem(dishName="dish1", dishDescription="This is dish1.", price=1.0, dishImageURL="http://dish1.com", dishTypeID=5)
dOpt.manageDishTable(restaurantName='rName1', password='123456')
dOpt.insertDishItem(dishName="dish1", dishDescription="This is dish1.", price=1.0, dishImageURL="http://dish1.com", dishTypeID=5)
dOpt.insertDishItem(dishName="dish1", dishDescription="This is dish1.", price=1.0, dishImageURL="http://dish1.com", dishTypeID=5)
dOpt.insertDishItem(dishName="dish1", dishDescription="This is dish1.", price=1.0, dishImageURL="http://dish1.com", dishTypeID=7)
dOpt.insertDishItem(dishName="dish1", dishDescription="This is dish1.", price=1.0, dishImageURL="http://dish1.com", dishTypeID=3)
dOpt.insertDishItem(dishName="dish2", dishDescription="This is dish2.", price=1.0, dishImageURL="http://dish2.com", dishTypeID=5)
dOpt.insertDishItem(dishName="dish3", dishDescription="This is dish3.", price=1.0, dishImageURL="http://dish3.com", dishTypeID=6)
dOpt.insertDishItem(dishName="dish4", dishDescription="This is dish4.", price=1.0, dishImageURL="http://dish4.com", dishTypeID=6)
dOpt.insertDishItem(dishName="dish5", dishDescription="This is dish5.", price=1.0, dishImageURL="http://dish5.com", dishTypeID=5)
dOpt.insertDishItem(dishName="dish6", dishDescription="This is dish6.", price=1.0, dishImageURL="http://dish6.com", dishTypeID=5)
dOpt.manageDishTable(restaurantName='rName2', password='123456')
dOpt.insertDishItem(dishName="dish1", dishDescription="This is dish1.", price=1.0, dishImageURL="http://dish1.com", dishTypeID=3)
dOpt.insertDishItem(dishName="dish2", dishDescription="This is dish2.", price=1.0, dishImageURL="http://dish2.com", dishTypeID=3)
# delete
dOpt = dishOperator()
dOpt.deleteDishItemWithDishID(dishID=1)
dOpt.manageDishTable(restaurantName='rName1', password='123456')
dOpt.deleteDishItemWithDishID(dishID=7)
dOpt.deleteDishItemWithDishID(dishID=9)
dOpt.deleteDishItemWithDishID(dishID=1)
dOpt.deleteDishItemsWithDishTypeID(dishTypeID=5)
dOpt.deleteDishItemsWithDishTypeID(dishTypeID=3)
dOpt.deleteDishItemsWithRestaurantID(restaurantID=3)
dOpt.deleteDishItemsWithRestaurantID(restaurantID=4)

## -----------------------------------------------------
## Table `TINYHIPPO`.`DishComment`
## -----------------------------------------------------
# initialize
dOpt = dishOperator()
dOpt.manageDishTable(restaurantName='rName1', password='123456')
dOpt.insertDishItem(dishName="dish1", dishDescription="This is dish1.", price=1.0, dishImageURL="http://dish1.com", dishTypeID=5)
dOpt.insertDishItem(dishName="dish2", dishDescription="This is dish2.", price=1.0, dishImageURL="http://dish2.com", dishTypeID=5)

print("\n---------- Test for 'DishComment' ----------")
# insert
dcOpt = dishCommentOperator()
dcOpt.insertDishTypeItem(comment="good1", dishID=11)
dcOpt.insertDishTypeItem(comment="good1", dishID=9)
dcOpt.insertDishTypeItem(comment="good2", dishID=9)
dcOpt.insertDishTypeItem(comment="good2", dishID=10)
# delete
dcOpt.deleteDishCommentByCommentID(dishCommentID=3)
dcOpt.deleteDishCommentByCommentID(dishCommentID=4)
dcOpt.deleteDishCommentsWithDishID(dishID=9)
dcOpt.deleteDishCommentsWithDishID(dishID=10)

## -----------------------------------------------------
## Table `TINYHIPPO`.`OrderList`
## -----------------------------------------------------
print("\n---------- Test for 'OrderList' ----------")
# insert
rDB = Tools().get_config("./data/restaurant_database.json")
oOpt = orderListOperator()
print("orderNumber:", oOpt.insertOrderItem(orderDetail=rDB, total=100.0, customerID="c1", tableID=5))
oOpt.manageOrderListTable(restaurantName='rName1', password='123456')
print("orderNumber:", oOpt.insertOrderItem(orderDetail="detail1", total=100.0, customerID="c5", tableID=7))
print("orderNumber:", oOpt.insertOrderItem(orderDetail=rDB, total=100.0, customerID="c1", tableID=5))
print("orderNumber:", oOpt.insertOrderItem(orderDetail="detail2", total=100.0, customerID="c2", tableID=5))
print("orderNumber:", oOpt.insertOrderItem(orderDetail="detail3", total=100.0, customerID="c3", tableID=5))
print("orderNumber:", oOpt.insertOrderItem(orderDetail="detail4", total=100.0, customerID="c4", tableID=5))
print("orderNumber:", oOpt.insertOrderItem(orderDetail="detail1", total=100.0, customerID="c5", tableID=6))
print("orderNumber:", oOpt.insertOrderItem(orderDetail="detail5", total=100.0, customerID="c6", tableID=5))
# delete
oOpt = orderListOperator()
oOpt.deleteOrderItemWithOrderID(orderID=1)
oOpt.manageOrderListTable(restaurantName='rName1', password='123456')
oOpt.deleteOrderItemWithOrderID(orderID=10)
oOpt.deleteOrderItemsWithTableID(tableID=7)
oOpt.deleteOrderItemWithOrderID(orderID=1)
oOpt.deleteOrderItemsWithTableID(tableID=5)

## -----------------------------------------------------
## Table `TINYHIPPO`.`Recommendation`
## -----------------------------------------------------
print("\n---------- Test for 'Recommendation' ----------")

# insert
rcOpt = recommendationOperator()
rcOpt.insertRecommendationItem(title="spring", tag="123", imageURL="http://img1.jpg")
rcOpt.manageRecommendationTable(restaurantName='rName1', password='123456')
rcOpt.insertRecommendationItem(title="spring", tag="123", imageURL="http://img1.jpg")
rcOpt.insertRecommendationItem(title="summer", tag="456", imageURL="http://img2.jpg")
rcOpt.manageRecommendationTable(restaurantName='rName2', password='123456')
rcOpt.insertRecommendationItem(title="fall", tag="123", imageURL="http://img3.jpg")
rcOpt.insertRecommendationItem(title="winter", tag="456", imageURL="http://img4.jpg")
# delete
rcOpt = recommendationOperator()
rcOpt.deleteDishCommentByCommentID(recommendationID=1)
rcOpt.manageRecommendationTable(restaurantName='rName1', password='123456')
rcOpt.deleteDishCommentByCommentID(recommendationID=5)
rcOpt.deleteDishCommentByCommentID(recommendationID=3)
rcOpt.deleteDishCommentByCommentID(recommendationID=1)

## -----------------------------------------------------
## Table `TINYHIPPO`.`RecommendationDetails`
## -----------------------------------------------------
print("\n---------- Test for 'RecommendationDetails' ----------")
# insert
rcdOpt = RecommendationDetailsOperator()
rcdOpt.insertRecommendationDetailsItem(recommendationID=5, dishID=9, description="balabalabala...")
rcdOpt.insertRecommendationDetailsItem(recommendationID=2, dishID=11, description="balabalabala...")
rcdOpt.insertRecommendationDetailsItem(recommendationID=3, dishID=9, description="balabalabala...")
rcdOpt.insertRecommendationDetailsItem(recommendationID=2, dishID=9, description="balabalabala...")
rcdOpt.insertRecommendationDetailsItem(recommendationID=2, dishID=10, description="balabalabala...")
# delete
rcdOpt.deleteRecommendationDetailsByRecommendationID(recommendationID=7)
rcdOpt.deleteRecommendationDetailsByDishID(dishID=11)
rcdOpt.deleteRecommendationDetailsByDishID(dishID=9)
rcdOpt.deleteRecommendationDetailsByRecommendationID(recommendationID=2)
