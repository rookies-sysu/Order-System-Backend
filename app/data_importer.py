import json
from dbOperators import *
from tools import *

def insert_fake_data2():
    try:
        # create tools
        tools = Tools()

        # load jsons
        rDB = tools.get_config("./data/restaurant_database.json")
        mDB = tools.get_config("./data/menu_database.json")
        rcDB = tools.get_config("./data/recommendation.json")

        # restaurant information
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
                qrOpt.insertQRlinkItem(linkImageURL=tInfo["QRlink"]["linkImageURL"], tableNumber=tInfo["tableNumber"])

        # menu information
        for mInfo in mDB:
            rOpt = restaurantOperator()
            rOpt.manageRestaurantTable(restaurantName="TINYHIPPO", password="123456")
            _, result = selectOperator(tableName="Restaurant", restaurantName="TINYHIPPO", result=["restaurantID"])
            restaurantID = result[0]["restaurantID"]
            # dishType
            dtOpt = dishTypeOperator(restaurantName="TINYHIPPO", password="123456")
            dtOpt.insertDishTypeItem(dishTypeName=mInfo["name"])
            _, result = selectOperator(tableName="DishType", dishTypeName=mInfo["name"], restaurantID=restaurantID, result=["dishTypeID"])
            dishTypeID = result[0]["dishTypeID"]
            # dish
            dOpt = dishOperator(restaurantName="TINYHIPPO", password="123456")
            for dInfo in mInfo["dish"]:
                dOpt.insertDishItem(dishName=dInfo["name"], dishDescription="", 
                        price=dInfo["price"], dishImageURL=dInfo["imageUrl"], dishTypeID=dishTypeID)
                        
        # recommendation information
        rcOpt = RecommendationOperator()
        rcOpt.manageRecommendationTable(restaurantName="TINYHIPPO", password="123456")
        rcdOpt = RecommendationDetailsOperator()
        for rcInfo in rcDB["data"]:  
            rcOpt.insertRecommendationItem(title=rcInfo['title'], tag=rcInfo['tag'], imageURL=rcInfo['image'])
            rcid = selectUniqueItem(tableName="Recommendation", restaurantID=1, title=rcInfo['title'], result=["recommendationID"])
            for obj in rcInfo['details']:
                rcdOpt.insertRecommendationDetailsItem(recommendationID=rcid, dishID=obj["dish_id"], description=obj["description"])
        
        return 'insert fake data 2 success!'
    except:
        return 'insert fake data 2 failed!'
