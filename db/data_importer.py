import json
from dbOperators import *
from tools import *

# load jsons
rDB = get_config("./data/resturant_database.json")
mDB = get_config("./data/menu_database.json")

# resturant infomation
for rInfo in rDB:
    rOpt = resturantOperator()
    rOpt.insertResturantItem(resturantName=rInfo["resturantName"],
        password=rInfo["password"],
        phone=rInfo["phone"],
        email=rInfo["email"])
    tOpt = tableOperator(resturantName=rInfo["resturantName"], password=rInfo["password"])
    qrOpt = QRlinkOperator(resturantName=rInfo["resturantName"], password=rInfo["password"])
    for tInfo in rInfo["table"]:
        # table
        tOpt.insertTableItem(tableNumber=tInfo["tableNumber"])
        # QRlink
        qrOpt.insertQRlinkItem(linkImageURL=tInfo["QRlink"]["linkImageURL"], tableNumber=tInfo["tableNumber"])

# menu infomation
for mInfo in mDB:
    rOpt = resturantOperator()
    rOpt.manageResturantTable(resturantName="TINYHIPPO", password="123456")
    resturantID = rOpt.selectResturantIDWithName("TINYHIPPO")
    # dishType
    dtOpt = dishTypeOperator(resturantName="TINYHIPPO", password="123456")
    dtOpt.insertDishTypeItem(dishTypeName=mInfo["name"])
    dishTypeID = dtOpt.selectDishTypeIDWithName(dishTypeName=mInfo["name"], resturantID=resturantID)
    # dish
    dOpt = dishOperator(resturantName="TINYHIPPO", password="123456")
    for dInfo in mInfo["foods"]:
        dOpt.insertDishItem(dishName=dInfo["name"], dishDescription=dInfo["description"], price=dInfo["price"], dishImageURL=dInfo["image_url"], dishTypeID=dishTypeID)