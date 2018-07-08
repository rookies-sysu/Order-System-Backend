import datetime
import time
import json
import random

import logging

from flask import Flask, jsonify, render_template, request, session, abort, make_response
from flask_cors import CORS
import redis

from dbTools import *

# 引入OS模块中的产生一个24位的随机字符串的函数
import os

app = Flask(__name__, instance_relative_config=True)
CORS(app, supports_credentials=True)

# 随机产生24位的字符串作为SECRET_KEY
app.config['SECRET_KEY'] = os.urandom(24)
# json输出中文
app.config['JSON_AS_ASCII'] = False

app.debug = True

# 解决跨域问题
def jsonResponse(dump_json):
    '''
    参数值为已格式化的json
    返回值为进行包装后的response
    '''
    res = make_response(dump_json)
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'POST,GET,PUT,DELETE,OPTIONS'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res

rInfo = {}

# 操作restaurant
restaurant_opt = restaurantOperator()
# 操作dishType
dish_type_opt = dishTypeOperator()
# 操作dish
dish_opt = dishOperator()
# 操作Orderlist
orderlist_opt = orderListOperator()

cache = redis.Redis(host='redis', port=6379)

############################################################################################################
# docker 开发测试api接口
def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


def get_index_menu_database():
    filename = os.path.join('./data/', 'menu_database.json')
    f = open(filename, encoding='utf-8')
    res = json.load(f)
    return jsonify(res)


@app.route('/', methods=['GET'])
def index():
    """
    api 直接读取 ./instance 中的数据返回给前端进行测试
    """
    return get_index_menu_database()


@app.route('/testRedis', methods=['GET'])
def testRedis():
    """
    api 测试 redis 是否已经正确连接
    """
    count = get_hit_count()
    return 'Hello Tiny-Hippo Backend!! I have been seen {} times.\n'.format(count)
##############################################################################################################


@app.route('/restaurant/recommendation', methods=['GET', 'POST'])
def restaurantRecommendation():
    '''
    api使用情况如下:
    methods='GET'时,用于获取餐店推荐菜品列表
    methods='POST'时,用于新增餐店推荐菜品
    '''
    if request.method == 'GET':
        dish_json = []
        restaurant_id = selectUniqueItem(
            tableName="Restaurant", restaurantName='TINYHIPPO', result=["restaurantID"])
        _, result = selectOperator(
            tableName="Recommendation", restaurantID=restaurant_id, result=["recommendationID"])

        recommendation_ids = []
        for r in result:
            recommendation_ids.append(r['recommendationID'])

        for recommendation_id in recommendation_ids:
            dish_ids = []
            descriptions = []
            _, result = selectOperator(tableName="RecommendationDetails",
                                       recommendationID=recommendation_id, result=["dishID", "description"])
            for r in result:
                dish_ids.append(r["dishID"])
                descriptions.append(r["description"])

            details = []
            for i in range(len(dish_ids)):
                detail_obj = {}
                detail_obj["dish"] = {
                    "dishID": dish_ids[i],
                    "categoryId": selectUniqueItem(tableName="Dish", dishID=dish_ids[i], result=["dishTypeID"]),
                    "name": selectUniqueItem(tableName="Dish", dishID=dish_ids[i], result=["dishName"]),
                    "price": selectUniqueItem(tableName="Dish", dishID=dish_ids[i], result=["price"]),
                    "imageUrl": selectUniqueItem(tableName="Dish", dishID=dish_ids[i], result=["dishImageURL"])
                }
                detail_obj["description"] = descriptions[i]
                details.append(detail_obj)

            obj = {}
            obj['title'] = selectUniqueItem(
                tableName="Recommendation", recommendationID=recommendation_id, result=["title"])
            obj['tag'] = selectUniqueItem(
                tableName="Recommendation", recommendationID=recommendation_id, result=["tag"])
            obj['imageUrl'] = selectUniqueItem(
                tableName="Recommendation", recommendationID=recommendation_id, result=["imageURL"])
            obj['recommendationId'] = recommendation_id
            obj['details'] = details
            dish_json.append(obj)

        return jsonResponse(jsonify(dish_json))
    elif request.method == 'POST':
        if not request.json or ('details' not in request.json) or ('imageUrl' not in request.json) or ('tag' not in request.json) or ('title' not in request.json):
            abort(400)
        # get restaurant info
        restaurantID = selectUniqueItem(
            tableName="Restaurant", restaurantName='TINYHIPPO', result=["restaurantID"])
        rstName = selectUniqueItem(
            tableName="Restaurant", restaurantID=restaurantID, result=["restaurantName"])
        pwd = selectUniqueItem(tableName="Restaurant",
                               restaurantID=restaurantID, result=["password"])
        rcOpt = RecommendationOperator(restaurantName=rstName, password=pwd)
        rcdOpt = RecommendationDetailsOperator()
        # get json info
        imageUrl = request.json['imageUrl']
        tag = request.json['tag']
        title = request.json['title']
        details = request.json['details']
        # insert recommendation item
        if not rcOpt.insertRecommendationItem(title=title, tag=tag, imageURL=imageUrl):
            dump_json = jsonify("Recommendation '%s' fail to insert." % title)
            return jsonResponse(dump_json)
        recommendationId = selectUniqueItem(
            tableName='Recommendation', title=title,  result=['recommendationID'])
        result = selectOperator(tableName='Recommendation', title=title,  result=[
                                'recommendationID', 'title', 'res'])
        print(result)
        # insert relationship of recommendation and dishes
        for detail in details:
            description = detail['description']
            dishName = detail['dishName']
            dishID = selectUniqueItem(
                tableName='Dish', dishName=dishName, restaurantID=restaurantID, result=['dishID'])
            rcdOpt.insertRecommendationDetailsItem(
                recommendationID=recommendationId, dishID=dishID, description=description)
        dump_json = jsonify("Insert recommedation into db.")
        return jsonResponse(dump_json)
    else:
        abort(400)


@app.route('/restaurant/getdish/<int:dish_id>', methods=['GET'])
def getDish(dish_id):
    '''
    api使用情况如下:
    methods='GET'时, 根据参数dish_id获取特定菜品的信息并返回
    '''
    if not identifyOperator(tableName="Dish", dishID=dish_id):
        abort(400, {'message': '菜品不存在'})
    dish_json = []
    # get comment
    _, result = selectOperator(
        tableName="DishComment", dishID=dish_id, result=["comment"])
    comment = []
    for r in result:
        comment.append(r["comment"])

    dish_json.append({
        "dishID": dish_id,
        "CategoryID": selectUniqueItem(tableName="Dish", dishID=dish_id, result=["dishTypeID"]),
        "name": selectUniqueItem(tableName="Dish", dishID=dish_id, result=["dishName"]),
        "price": selectUniqueItem(tableName="Dish", dishID=dish_id, result=["price"]),
        "imageURL": selectUniqueItem(tableName="Dish", dishID=dish_id, result=["dishImageURL"]),
        "description": [
            {
                "comment": comment,
                "monthlySales": selectUniqueItem(tableName="Dish", dishID=dish_id, result=["monthlySales"]),
                "hot": selectUniqueItem(tableName="Dish", dishID=dish_id, result=["dishHot"])
            }
        ]
    })
    return jsonResponse(jsonify(dish_json))

@app.route('/restaurant/customer/record', methods=['POST'])
def customerRecord():
    '''
    api使用情况如下:
    methods='POST'时, 登记顾客信息
    记录顾客的CustomerID和TableID作为session,并由POST信息生成特定的key-value存储在redis上
    '''
    if not request.json or ('customerId' not in request.json) or ('customerName' not in request.json) or ('table' not in request.json) or ('customerImageUrl' not in request.json):
        abort(400)
    # 将用户信息记录至session并保存至redis
    session['CustomerID'] = request.json['customerId']
    session['TableID'] = request.json['table']
    # 记录用户的customerImageUrl和customerName至redis
    cache.set(session['CustomerID']+'-ImageUrl',
              request.json['customerImageUrl'])
    cache.set(session['CustomerID']+'-Name', request.json['customerName'])
    # 对某一张Table增添顾客(set操作 元素不重复)
    cache.sadd('TableID-'+str(session['TableID']), session['CustomerID'])
    # 将CustomerID和TableID组合作为key
    new_key = 'TID-'+str(session['TableID'])+'-CID-'+session['CustomerID']
    if cache.get(new_key) != None:
        dump_json = jsonify(new_key+" had been Recorded before!")
        return jsonResponse(dump_json)
    cache.set(new_key, '')
    dump_json = jsonify(new_key+" is Recorded")
    return jsonResponse(dump_json)

@app.route('/restaurant/customer/edit', methods=['PUT'])
def customerEdit():
    '''
    api使用情况如下:
    methods='PUT'时, 顾客编写小订单
    根据顾客自身的session(CustomerID和TableID)来搜索在redis上存储的key-value,然后由PUT信息进行替换
    '''
    dump_json = jsonify("CustomerID or TableID is None")
    if session.get('CustomerID') != None and session.get('TableID') != None:
        # 查找编写的edit-key
        edit_key = 'TID-'+str(session['TableID'])+'-CID-'+session['CustomerID']
        if cache.get(edit_key) != None:
            # 更新编写的小订单
            edit_update_order = request.json['orderInfo']
            cache.set(edit_key, edit_update_order)
            dump_json = jsonify(edit_key+' is Updated')
        else:
            dump_json = jsonify(edit_key+" cache had been clear!")
    return jsonResponse(dump_json)


@app.route('/restaurant/customer/read', methods=['GET'])
def customerRead():
    '''
    api使用情况如下:
    methods='GET'时, 顾客查看个人小订单
    根据顾客自身的session(CustomerID和TableID)来搜索在redis上存储的key-value,然后组合成json返回
    '''
    dump_json = jsonify("CustomerID or TableID is None")
    if session.get('CustomerID') != None and session.get('TableID') != None:
        # 查找要查看的read-key
        read_key = 'TID-'+str(session['TableID'])+'-CID-'+session['CustomerID']
        if cache.get(read_key) != None:
            read_current_order = cache.get(read_key).decode()
            if read_current_order != '':
                read_current_order = eval(read_current_order)
            name = cache.get(session['CustomerID']+"-Name").decode()
            image = cache.get(session['CustomerID']+"-ImageUrl").decode()
            # eval将字符串str当成有效的表达式来求值并返回计算结果(即json内容)
            dump_json = jsonify({"orderInfo": read_current_order,
                                 "customerName": name,
                                 "customerImageUrl": image})
        else:
            dump_json = jsonify(read_key+" cache had been clear!")
    return jsonResponse(dump_json)

@app.route('/restaurant/table/read', methods=['GET'])
def tableRead():
    '''
    api使用情况如下:
    methods='GET'时, 顾客查看同一餐桌上所有的订单
    根据顾客自身的session(TableID)来搜索在redis上存储的key-value,然后组合成json返回
    '''
    dump_json = jsonify("TableID is None")
    if session.get('TableID') != None:
        table_items = []
        read_table_key = 'TableID-'+str(session['TableID'])
        # 判断table上是否有customer
        if cache.scard(read_table_key) == 0:
            dump_json = jsonify(read_table_key+" cache had been clear!")
            return jsonResponse(dump_json)
        # 读取同一桌所有的CustomerID
        customers_ids = cache.smembers(read_table_key)
        for i in customers_ids:
            i = i.decode()
            # 加入每个Customer编写的小订单
            read_key = 'TID-'+str(session['TableID'])+'-CID-'+str(i)
            read_current_order = str(cache.get(read_key).decode())
            if read_current_order != '':
                read_current_order = eval(read_current_order)
            name = cache.get(str(i)+"-Name").decode()
            image = cache.get(str(i)+"-ImageUrl").decode()
            table_items.append({"orderInfo": read_current_order,
                                "customer_name": name,
                                "customer_image": image})
        dump_json = jsonify(table_items)
    return jsonResponse(dump_json)


@app.route('/restaurant/table/payment', methods=['GET'])
def tablePayment():
    '''
    api使用情况如下:
    methods='GET'时, 顾客支付订单
    根据顾客自身的session(TableID)来搜索在redis上存储的key-value,并写入后台订单数据库,随后在redis上进行删除
    '''
    dump_json = jsonify("TableID is None")
    if session.get('TableID') != None:
        # get info of restaurant
        restaurantID = selectUniqueItem(
            tableName="Restaurant", restaurantName='TINYHIPPO', result=["restaurantID"])
        rstName = selectUniqueItem(
            tableName="Restaurant", restaurantID=restaurantID, result=["restaurantName"])
        pwd = selectUniqueItem(tableName="Restaurant",
                               restaurantID=restaurantID, result=["password"])
        orderlist_opt.manageOrderListTable(
            restaurantName=rstName, password=pwd)
        # 读取同一桌所有的CustomerID
        tableID = session['TableID']
        read_table_key = 'TableID-'+str(tableID)
        # 判断table上是否有customer
        if cache.scard(read_table_key) == 0:
            dump_json = jsonify(read_table_key+" cache had been clear!")
            return jsonResponse(dump_json)
        customer_ids = cache.smembers(read_table_key)
        for customer_id in customer_ids:
            customer_id = customer_id.decode()
            read_key = 'TID-'+str(tableID)+'-CID-'+customer_id
            read_current_order = str(cache.get(read_key).decode())
            if read_current_order != '':
                read_current_order = eval(read_current_order)
                # 插入订单 & 确认支付
                order_detail = {"dish": read_current_order['dish'],
                                "requirement": read_current_order['requirement']}
                print(order_detail)
                orderNumber = orderlist_opt.insertOrderItem(orderDetail=order_detail,
                                                            total=read_current_order['totalPrice'], customerID=customer_id, tableID=tableID)
                updateOperator(rstName=rstName, pwd=pwd, tableName="OrderList",
                               orderNumber=orderNumber, status='todo', new_isPaid=True)
                updateOperator(rstName=rstName, pwd=pwd, tableName="OrderList",
                               orderNumber=orderNumber, status='todo', new_status='done')

            cache.delete(read_key)
            cache.delete(customer_id+"-Name")
            cache.delete(customer_id+"-ImageUrl")
        cache.delete(read_table_key)
        dump_json = jsonify("OK")
    return jsonResponse(dump_json)


@app.route('/restaurant/customer/history', methods=['GET'])
def customerHistory():
    '''
    api使用情况如下:
    methods='GET'时, 顾客查看历史订单
    根据顾客自身的session(CustomerID)来查询后台数据库中与顾客相关的历史订单,然后组合成json返回
    '''
    dump_json = jsonify("error")
    if (session.get('CustomerID') == None):
        return jsonResponse(dump_json)
    # get orderIDs by CustomerID
    customerOrderIDs = []
    # get customer OrderIDs
    _, result = selectOperator(
        tableName='OrderList', customerID=session['CustomerID'], result=["orderID"])
    for r in result:
        customerOrderIDs.append(r["orderID"])
    history_json = []
    # 查找Customer对应的订单记录
    for cOrderID in customerOrderIDs:
        # get order details
        orderDetail = selectUniqueItem(
            tableName='OrderList', orderID=cOrderID, result=["orderDetail"])
        history_json.append(orderDetail)
    dump_json = jsonify(history_json)
    return jsonResponse(dump_json)


@app.route('/restaurant/customer/category', methods=['GET'])
def customerGetCategory():
    '''
    api使用情况如下:
    methods='GET'时, 顾客获取餐厅菜品列表
    '''
    # get restaurant ID
    restaurantID = selectUniqueItem(
        tableName="Restaurant", restaurantName='TINYHIPPO', result=["restaurantID"])
    # get all dishTypeIDs by restaurantID
    dishTypeIDs = []
    _, result = selectOperator(
        tableName="DishType", restaurantID=restaurantID, result=["dishTypeID"])
    for r in result:
        dishTypeIDs.append(r["dishTypeID"])
    menu_json = []
    for dishTypeID in dishTypeIDs:
        # get all dishIDs by dishTypeID
        dishIDs = []
        _, result = selectOperator(
            tableName="Dish", dishTypeID=dishTypeID, result=["dishID"])
        for r in result:
            dishIDs.append(r["dishID"])
        all_dish_json = []
        for dishID in dishIDs:
            # get comment
            _, result = selectOperator(
                tableName="DishComment", dishID=dishID, result=["comment"])
            comment = []
            for r in result:
                comment.append(r["comment"])
            all_dish_json.append({
                "dishId": dishID,
                "categoryId": selectUniqueItem(tableName="Dish", dishID=dishID, result=["dishTypeID"]),
                "name": selectUniqueItem(tableName="Dish", dishID=dishID, result=["dishName"]),
                "price": selectUniqueItem(tableName="Dish", dishID=dishID, result=["price"]),
                "imageUrl": selectUniqueItem(tableName="Dish", dishID=dishID, result=["dishImageURL"])
            })
        menu_json.append({
            "categoryId": dishTypeID,
            "name": selectUniqueItem(tableName="DishType", dishTypeID=dishTypeID, result=["dishTypeName"]),
            "dish": all_dish_json
        })
    dump_json = jsonify(menu_json)
    return jsonResponse(dump_json)


@app.route('/restaurant/session', methods=['POST', 'DELETE'])
def restaurantLogin():
    '''
    api使用情况如下:
    methods='POST'时,进行登录,根据POST信息查找数据库中对应的restaurant,随后组合成json返回
    methods='DELETE'时,退出登录,返回Login Off
    '''
    if request.method == 'POST':
        if not request.json or (not 'phone' in request.json) or (not 'password' in request.json):
            abort(400)
        # save info of restaurant into session
        phone = str(request.json['phone'])
        password = str(request.json['password'])
        restaurantName = selectUniqueItem(
            tableName="Restaurant", phone=phone, password=password, result=["restaurantName"])
        email = selectUniqueItem(
            tableName="Restaurant", phone=phone, password=password, result=["email"])
        # 操作restaurant
        restaurant_opt.manageRestaurantTable(
            restaurantName=restaurantName, password=password)
        # 操作dishType
        dish_type_opt.manageDishTypeTable(
            restaurantName=restaurantName, password=password)
        # 操作dish
        dish_opt.manageDishTable(
            restaurantName=restaurantName, password=password)
        # 操作Orderlist
        orderlist_opt.manageOrderListTable(
            restaurantName=restaurantName, password=password)
        # generate json
        restaurant_json = {
            "restaurantName": restaurantName,
            "password": password,
            "phone": phone,
            "email": email,
        }
        dump_json = jsonify(restaurant_json)
        return jsonResponse(dump_json)
    elif request.method == 'DELETE':    
        dump_json = jsonify("Login Off")
        return jsonResponse(dump_json)
    else:
        # neither 'get' nor 'post'
        abort(400)


@app.route('/restaurant/category', methods=['GET', 'POST'])
def restaurantCategory():
    '''
    api使用情况如下:
    methods='GET'时,用于获取餐店菜品列表
    methods='POST'时,用于新增餐店菜品
    '''
    if request.method == 'GET':
        # 需要 RestaurantID
        restaurantID = selectUniqueItem(
            tableName="Restaurant", restaurantName='TINYHIPPO', result=["restaurantID"])
        # get all dishTypeIDs by restaurantID
        dishTypeIDs = []
        _, result = selectOperator(
            tableName="DishType", restaurantID=restaurantID, result=["dishTypeID"])
        for r in result:
            dishTypeIDs.append(r["dishTypeID"])
        menu_json = []
        for dishTypeID in dishTypeIDs:
            # get all dishIDs by dishTypeID
            dishIDs = []
            _, result = selectOperator(
                tableName="Dish", dishTypeID=dishTypeID, result=["dishID"])
            for r in result:
                dishIDs.append(r["dishID"])
            all_dish_json = []
            for dishID in dishIDs:
                # # get comment
                # result = selectResultSet(tableName="DishComment", dishID=dishID, result=["comment"])
                # comment = result["comment"]
                all_dish_json.append({
                    "dishId": dishID,
                    "categoryId": selectUniqueItem(tableName="Dish", dishID=dishID, result=["dishTypeID"]),
                    "name": selectUniqueItem(tableName="Dish", dishID=dishID, result=["dishName"]),
                    "price": selectUniqueItem(tableName="Dish", dishID=dishID, result=["price"]),
                    "imageUrl": selectUniqueItem(tableName="Dish", dishID=dishID, result=["dishImageURL"])
                })
            menu_json.append({
                "categoryId": dishTypeID,
                "name": selectUniqueItem(tableName="DishType", dishTypeID=dishTypeID, result=["dishTypeName"]),
                "dish": all_dish_json
            })
        dump_json = jsonify(menu_json)
        return jsonResponse(dump_json)
    elif request.method == 'POST':
        if not request.json:
            abort(400)
        # get info of restaurant
        restaurantID = selectUniqueItem(
            tableName="Restaurant", restaurantName='TINYHIPPO', result=["restaurantID"])
        rstName = selectUniqueItem(
            tableName="Restaurant", restaurantID=restaurantID, result=["restaurantName"])
        pwd = selectUniqueItem(tableName="Restaurant",
                               restaurantID=restaurantID, result=["password"])
        # 获取 POST 信息
        name = str(request.json['name'])
        price = float(request.json['price'])
        imageURL = str(request.json['imageUrl'])
        dishID = int(request.json['dishId'])
        categoryID = int(request.json['categoryId'])
        # 插入菜品，默认不管 description
        dish_opt.manageDishTable(restaurantName=rstName, password=pwd)
        dish_opt.insertDishItem(dishName=name,
                                dishDescription="",
                                price=price,
                                dishImageURL=imageURL,
                                dishTypeID=categoryID)
        dump_json = jsonify("Insert Successfully")
        return jsonResponse(dump_json)
    else:
        # neither 'get' nor 'post'
        abort(400)


@app.route('/restaurant/dish/<int:dishId>', methods=['PUT', 'DELETE', 'OPTIONS'])
def restaurantDishChange(dishId):
    '''
    api使用情况如下:
    methods='GET'时,根据参数dishId和POST信息修改特定菜品信息
    methods='DELETE'时,根据参数dishId删除特定菜品
    '''
    if not identifyOperator(tableName="Dish", dishID=dishId):
        abort(400)
    if request.method == 'PUT' or request.method == 'OPTIONS':
        if not request.json or 'categoryId' not in request.json or 'name' not in request.json or 'price' not in request.json or 'imageUrl' not in request.json:
            abort(400)
        dish_Id = int(request.json['dishId'])
        restaurantID = selectUniqueItem(
            tableName="Restaurant", restaurantName='TINYHIPPO', result=["restaurantID"])
        rstName = selectUniqueItem(
            tableName="Restaurant", restaurantID=restaurantID, result=["restaurantName"])
        pwd = selectUniqueItem(tableName="Restaurant",
                               restaurantID=restaurantID, result=["password"])
        # 根据POST信息修改dish 需要先登录restaurant
        dishTypeID = request.json['categoryId']
        dishName = str(request.json['name'])
        price = float(request.json['price'])
        dishImageUrl = str(request.json['imageUrl'])
        # update info
        updateOperator(rstName=rstName, pwd=pwd, tableName="Dish",
                       dishID=dish_Id, new_dishTypeID=dishTypeID)
        updateOperator(rstName=rstName, pwd=pwd, tableName="Dish",
                       dishID=dish_Id, new_dishName=dishName)
        updateOperator(rstName=rstName, pwd=pwd, tableName="Dish",
                       dishID=dish_Id, new_price=price)
        updateOperator(rstName=rstName, pwd=pwd, tableName="Dish",
                       dishID=dish_Id, new_dishImageURL=dishImageUrl)
        dump_json = jsonify("Update dish successfully")
        return jsonResponse(dump_json)
    elif request.method == 'DELETE':
        # get info of restaurant
        restaurantID = selectUniqueItem(
            tableName="Restaurant", restaurantName='TINYHIPPO', result=["restaurantID"])
        rstName = selectUniqueItem(
            tableName="Restaurant", restaurantID=restaurantID, result=["restaurantName"])
        pwd = selectUniqueItem(tableName="Restaurant",
                               restaurantID=restaurantID, result=["password"])
        dish_opt.manageDishTable(restaurantName=rstName, password=pwd)
        # delete dish item
        dish_opt.deleteDishItemWithDishID(dishID=dishId)
        dump_json = jsonify("Delete dish successfully")
        return jsonResponse(dump_json)
    else:
        # neither 'get' nor 'post'
        abort(400)


# 餐厅账号新增分类
@app.route('/restaurant/category/', methods=['POST'])
def restaurantCategoryAdd():
    '''
    api使用情况如下:
    methods='POST'时,根据POST信息新增菜品分类
    '''
    # 异常返回
    if not request.json or (not 'categoryName' in request.json):
        abort(400)
    # get info of restaurant
    restaurantID = selectUniqueItem(
        tableName="Restaurant", restaurantName='TINYHIPPO', result=["restaurantID"])
    rstName = selectUniqueItem(
        tableName="Restaurant", restaurantID=restaurantID, result=["restaurantName"])
    pwd = selectUniqueItem(tableName="Restaurant",
                           restaurantID=restaurantID, result=["password"])
    dish_type_opt.manageDishTypeTable(restaurantName=rstName, password=pwd)
    # 插入新的分类
    new_dish_type_name = str(request.json['categoryName'])
    dish_type_opt.insertDishTypeItem(dishTypeName=new_dish_type_name)
    dump_json = jsonify("Insert New DishType")
    return jsonResponse(dump_json)


@app.route('/restaurant/category/<int:categoryId>', methods=['PUT', 'DELETE'])
def restaurantCategoryChange(categoryId):
    '''
    api使用情况如下:
    methods='PUT'时,根据参数categoryId和PUT信息修改特定分类信息
    methods='DELETE'时,根据参数categoryId删除特定分类
    '''
    # get info of restaurant
    restaurantID = selectUniqueItem(
        tableName="Restaurant", restaurantName='TINYHIPPO', result=["restaurantID"])
    rstName = selectUniqueItem(
        tableName="Restaurant", restaurantID=restaurantID, result=["restaurantName"])
    pwd = selectUniqueItem(tableName="Restaurant",
                           restaurantID=restaurantID, result=["password"])
    if request.method == 'PUT':
        print('/restaurant/category/<int:categoryId> PUT')
        if (not request.json) or (not identifyOperator(tableName="DishType", dishTypeID=categoryId)):
            abort(400)
        # 修改分类信息
        updateOperator(rstName=rstName, pwd=pwd, tableName="DishType",
                       dishTypeID=categoryId, new_dishTypeName=str(request.json['name']))
        dump_json = jsonify("Update DishType")
        return jsonResponse(dump_json)
    if request.method == 'DELETE':
        if not identifyOperator(tableName="DishType", dishTypeID=categoryId):
            abort(400)
        dish_type_opt.manageDishTypeTable(restaurantName=rstName, password=pwd)
        dish_type_opt.deleteDishTypeByID(dishTypeID=categoryId)
        dump_json = jsonify("Delete DishType")
        return jsonResponse(dump_json)
    else:
        # neither 'get' nor 'post'
        abort(400)

# 餐厅账号获取订单


@app.route('/restaurant/order', methods=['GET'])
def restaurantOrder():
    '''
    api使用情况如下:
    methods='GET'时,根据参数pageSize和pageNumber来返回部分订单条目
    '''
    # 每页订单的条目数
    pageSize = int(request.args.get('pageSize'))
    # 第几页订单
    pageNumber = int(request.args.get('pageNumber'))
    # get restaurantID
    restaurantID = selectUniqueItem(
        tableName="Restaurant", restaurantName='TINYHIPPO', result=["restaurantID"])
    # get all orderIDs by restaurantID
    orderIDs = []
    _, result = selectOperator(
        tableName="OrderList", restaurantID=restaurantID, result=["orderID"])
    for r in result:
        orderIDs.append(r["orderID"])
    number_order_json = []
    for idx, orderID in enumerate(orderIDs):
        # 根据OrderID排序
        if (pageNumber*pageSize > idx):
            orderDetails = eval(selectUniqueItem(
                tableName="OrderList", orderID=orderID, result=["orderDetail"]))
            print(orderDetails)
            # if not orderDetails:
            #     orderDetails = {'dish': [], 'requirement':''}
            number_order_json.append({
                "orderId": orderID,
                "table": selectUniqueItem(tableName="OrderList", orderID=orderID, result=["tableID"]),
                "dish": orderDetails['dish'],
                "requirement": orderDetails['requirement'],
                "totalPrice": selectUniqueItem(tableName="OrderList", orderID=orderID, result=["total"]),
                "customerId": selectUniqueItem(tableName="OrderList", orderID=orderID, result=["customerId"]),
                "time": selectUniqueItem(tableName="OrderList", orderID=orderID, result=["editedTime"]),
                "paymentStatus": selectUniqueItem(tableName="OrderList", orderID=orderID, result=["isPaid"]),
                "cookingStatus": selectUniqueItem(tableName="OrderList", orderID=orderID, result=["status"])
            })
    dump_json = jsonify(number_order_json)
    return jsonResponse(dump_json)


# 插入假数据
@app.route('/insert_fake_data2', methods=['GET'])
def insert_fake_data2():
    return dbInit()

# 处理404样式
@app.errorhandler(404)
def not_found_404(error):
    res = make_response(jsonify({'error': 'Not found'}), 404)
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'POST,GET,PUT,DELETE,OPTIONS'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res


# 处理400样式
@app.errorhandler(400)
def not_found_400(error):
    res = make_response(jsonify([{'code': '400', 'message': 'Grammatical formatting of request is wrong'}]), 400)
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'POST,GET,PUT,DELETE,OPTIONS'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
