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

        # restaurant infomation
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

        # menu infomation
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
            for dInfo in mInfo["foods"]:
                dOpt.insertDishItem(dishName=dInfo["name"], dishDescription=dInfo["description"], 
                        price=dInfo["price"], dishImageURL=dInfo["image_url"], dishTypeID=dishTypeID)

        rcOpt = RecommendationOperator()
        rcdOpt = RecommendationDetailsOperator()
        for rcInfo in rcDB:
            rcOpt.insertRecommendationItem(rcInfo['title'], rcInfo['tag'], rcInfo['image'])
            rcid = selectUniqueItem(tableName="Recommedation", restaurantID=1, title=rcInfo['title'], result=["recommendationID"])
            for obj in rcInfo['details']:
                rcdOpt.insertRecommendationDetailsItem(rcid, obj.dish_id, obj.description)

        return 'insert fake data 2 success!'
    except:
        return 'insert fake data 2 failed!'
