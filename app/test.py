import json
# from dbOperators import *
from tools import *

# create tools
tools = Tools()

# load jsons
rDB = tools.get_config("./data/restaurant_database.json")
mDB = tools.get_config("./data/menu_database.json")
rcDB = tools.get_config("./data/recommendation.json")

        

# rcOpt = RecommendationOperator()
# rcdOpt = RecommendationDetailsOperator()
# print(rcDB) 
for rcInfo in rcDB["data"]:
    print(rcInfo['title'])
    print(rcInfo['tag'])
    print(rcInfo['image'])
    for obj in rcInfo['details']:
        print(obj["dish_id"])
        print(obj["description"])
    # rcOpt.insertRecommendationItem(title=rcInfo['title'], tag=rcInfo['tag'], imageURL=rcInfo['image'])
    # rcid = selectUniqueItem(tableName="Recommedation", restaurantID=1, title=rcInfo['title'], result=["recommendationID"])
    # for obj in rcInfo['details']:
    #     rcdOpt.insertRecommendationDetailsItem(rcid, obj.dish_id, obj.description)
