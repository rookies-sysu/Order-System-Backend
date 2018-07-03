import json
from .dbOperators import *
from .tools import *

def dbInit():
    """
    Insert initial information of our database.
    """
    try:
        # create tools
        tools = Tools()
        # load jsons
        rDB = tools.getConfig("./data/restaurant_database.json")
        mDB = tools.getConfig("./data/menu_database.json")
        rcDB = tools.getConfig("./data/recommendation.json")
        # restaurant information
        insertRestaurantInfo(rDB)
        # menu information
        insertMenuInfo(mDB)
        # recommendation information
        insertRecommendationInfo(rcDB)
        return 'insert fake data 2 success!'
    except:
        return 'insert fake data 2 failed!'

def insertRestaurantInfo(rDB):
    """ Insert the initial information of Restaurant.
    Arg:
        rDB: the data of Restaurant in the form of json.
    """
    for rInfo in rDB:
        rOpt = restaurantOperator()
        rOpt.insertRestaurantItem(restaurantName=rInfo["restaurantName"],
                                  password=rInfo["password"],
                                  phone=rInfo["phone"],
                                  email=rInfo["email"])
        tOpt = tableOperator(restaurantName=rInfo["restaurantName"], password=rInfo["password"])
        qrOpt = QRlinkOperator(restaurantName=rInfo["restaurantName"], password=rInfo["password"])
        for tInfo in rInfo["table"]:
            # table
            tOpt.insertTableItem(tableNumber=tInfo["tableNumber"])
            # QRlink
            qrOpt.insertQRlinkItem(
                    linkImageURL=tInfo["QRlink"]["linkImageURL"], tableNumber=tInfo["tableNumber"])

def insertMenuInfo(mDB):
    """ Insert the initial information of Menu.
    Arg:
        mDB: the data of Menu in the form of json.
    """
    for mInfo in mDB:
        rOpt = restaurantOperator()
        rOpt.manageRestaurantTable(restaurantName="TINYHIPPO", password="123456")
        restaurantID = selectUniqueItem(tableName="Restaurant", restaurantName="TINYHIPPO", result=["restaurantID"])
        # dishType
        dtOpt = dishTypeOperator(restaurantName="TINYHIPPO", password="123456")
        dtOpt.insertDishTypeItem(dishTypeName=mInfo["name"])
        dishTypeID = selectUniqueItem(tableName="DishType", dishTypeName=mInfo["name"], restaurantID=restaurantID, result=["dishTypeID"])
        # dish
        dOpt = dishOperator(restaurantName="TINYHIPPO", password="123456")
        for dInfo in mInfo["dish"]:
            dOpt.insertDishItem(dishName=dInfo["name"], dishDescription="",
                                price=dInfo["price"], dishImageURL=dInfo["imageUrl"], dishTypeID=dishTypeID)

def insertRecommendationInfo(rcDB):
    """ Insert the initial information of Recommendation.
    Arg:
        rcDB: the data of Recommendation in the form of json.
    """
    rcOpt = RecommendationOperator()
    rcOpt.manageRecommendationTable(restaurantName="TINYHIPPO", password="123456")
    rcdOpt = RecommendationDetailsOperator()
    for rcInfo in rcDB["data"]:
        # Insert Recommendation Item
        rcOpt.insertRecommendationItem(title=rcInfo['title'], tag=rcInfo['tag'], imageURL=rcInfo['image'])
        rcid = selectUniqueItem(tableName="Recommendation", restaurantID=1,
                                title=rcInfo['title'], result=["recommendationID"])
        # Build the relationship between Recommendation and Dish
        for obj in rcInfo['details']:
            rcdOpt.insertRecommendationDetailsItem(recommendationID=rcid, dishID=obj["dish_id"], description=obj["description"])

if __name__ == '__main__':
    dbInit()
