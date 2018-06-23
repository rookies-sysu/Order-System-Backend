import datetime
import time
import json
import random

from flask import Flask, jsonify, render_template, request, session, abort, make_response
from flask_cors import CORS
import redis

# 引入OS模块中的产生一个24位的随机字符串的函数
import os

# 调用数据库操作
import sys
from dbOperators import *

# # 复用不优雅的数据插入假数据
# import db_insert
# import data_importer

app = Flask(__name__, instance_relative_config=True)
CORS(app)

# 随机产生24位的字符串作为SECRET_KEY
app.config['SECRET_KEY'] = os.urandom(24)
# json输出中文
app.config['JSON_AS_ASCII'] = False


app.debug = True

#操作restaurant
restaurant_opt = resturantOperator()
#restaurant_opt.manageResturantTable(resturantName='TINYHIPPO', password='123456')
# 操作dishType
dish_type_opt = dishTypeOperator()
#dish_type_opt.manageDishTypeTable(resturantName='TINYHIPPO', password='123456')
# 操作dish
dish_opt = dishOperator()
#dish_opt.manageDishTable(resturantName='TINYHIPPO', password='123456')
# 操作customer
customer_opt = customerOperator()
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


#顾客信息记录(传入CustomerID和TableID)
@app.route('/restaurant/customer/record', methods=['POST'])
def customer_record():
    if session.get('CustomerID') == None and session.get('TableID') == None:
        #将用户信息记录至session并保存至redis
        session['CustomerID'] = str(request.json['CustomerID'])
        session['TableID'] = str(request.json['table'])
        #对某一张Table增添顾客(list操作)
        cache.rpush('TableID-'+str(session['TableID']), session['CustomerID'])
        #将CustomerID和TableID组合作为key
        new_key = 'TID-'+str(session['TableID'])+'-CID-'+str(session['CustomerID'])
        cache.set(new_key, '')
        return jsonify(new_key)
    return jsonify('Record is Finished')

#顾客编写小订单
@app.route('/restaurant/customer/edit', methods=['POST'])
def customer_edit():
    if session.get('CustomerID') != None and session.get('TableID') != None:
        #查找编写的edit-key
        edit_key = 'TID-'+str(session['TableID'])+'-CID-'+str(session['CustomerID'])
        #更新编写的小订单
        edit_update_order = request.json['items']
        cache.set(edit_key, edit_update_order)
        return jsonify(edit_key+' is Updated')
    return jsonify("error")

#顾客查看小订单  
@app.route('/restaurant/customer/read', methods=['GET'])
def customer_read():
    if session.get('CustomerID') != None and session.get('TableID') != None:
        #查找要查看的read-key
        read_key = 'TID-'+str(session['TableID'])+'-CID-'+str(session['CustomerID'])
        read_current_order = str(cache.get(read_key).decode())
        #eval将字符串str当成有效的表达式来求值并返回计算结果(即json内容)
        return jsonify({"items":eval(read_current_order)})
    return jsonify("error")

#餐桌查看当前的Customer订单
@app.route('/restaurant/table/read', methods=['GET'])
def table_read():
    if session.get('TableID') != None:
        items = []
        #读取同一桌所有的CustomerID
        read_table_key = 'TableID-'+str(session['TableID'])
        customers_id = cache.lrange(read_table_key, 0, -1)
        for i in customers_id:
            i = i.decode()
            #加入每个Customer编写的小订单
            read_key = 'TID-'+str(session['TableID'])+'-CID-'+str(i)
            read_current_order = str(cache.get(read_key).decode())
            items.append(eval(read_current_order))
        return jsonify(items)
    return jsonify("error")

#餐桌支付订单
@app.route('/restaurant/table/payment', methods=['GET'])
def table_payment():
    if session.get('TableID') != None:
        #读取同一桌所有的CustomerID
        read_table_key = 'TableID-'+str(session['TableID'])
        customers_id = cache.lrange(read_table_key, 0, -1)
        for i in customers_id:
            i = i.decode()
            read_key = 'TID-'+str(session['TableID'])+'-CID-'+str(i)
            read_current_order = str(cache.get(read_key).decode())
            read_current_order = eval(read_current_order)
            #将每个小订单写入数据库
            new_order_id = orderlist_opt.insertOrderItem(orderDetail='json',
                                                    total=read_current_order['price'], 
                                                    tableID=read_current_order['table'],
                                                    customerID=read_current_order['customerId'])
            #确认支付
            orderlist_opt.updateIsPaid(isPaid=1, orderID=new_order_id)                              
        return jsonify("OK")
    return jsonify("error")

#顾客查看历史
@app.route('/restaurant/customer/history', methods=['GET'])
def customer_history():
    if (session.get('CustomerID') == None):
        return jsonify("Error")
    all_order = orderlist_opt.selectAllOrder()
    history_json = []
    #查找Customer对应的订单记录
    for row in all_order:
        if row[8] == session['CustomerID']:
            history_json.append(row[2])
    return jsonify(history_json)

#顾客账号获取用户自身信息 
@app.route('/restaurant/customer/self', methods=['GET'])
def customer_info():
    if (session.get('CustomerID') == None):
        return jsonify("Error")
    return jsonify({'CustomerID':session['CustomerID']})

# 顾客账号获取菜单
@app.route('/restaurant/customer/category', methods=['GET'])
def customer_get_category():
    all_dish_type = dish_type_opt.selectAllDishType()
    menu_json = []
    for dish_type_row in all_dish_type:
        all_dish = dish_opt.selectAllDishWithDishTypeID(dish_type_row[0])
        all_dish_json = []
        for dish_id in all_dish:
            all_dish_json.append({
                "dishID": dish_id,
                "CategoryID": dish_type_row[0],
                "name": dish_opt.selectDishNameWithDishID(dish_id),
                "price": dish_opt.selectPriceWithDishID(dish_id),
                "imageURL": dish_opt.selectDishImageURLWithDishID(dish_id),
                "description": [
                    {
                        "comment": dish_opt.selectDishCommentWithDishID(dish_id),
                        "monthlySales": dish_opt.selectMonthlySalesWithDishID(dish_id),
                        "hot": dish_opt.selectDishHotWithDishID(dish_id)
                    }
                ]
            })
        menu_json.append({
            "CategoryID": dish_type_row[0],
            "name": dish_type_row[1],
            "dish": all_dish_json
        })
    return jsonify(menu_json)

# 顾客账号下单
@app.route('/restaurant/self/order', methods=['POST'])
def customer_post_order():
    if not request.json:
        abort(400)
    # 订单信息
    dish_json = str(request.json['items']['dish'])
    price = request.json['items']['price']
    table = request.json['items']['table']
    customerId = request.json['items']['customerId']
    # 生成新订单
    # 目前dish_json内容无法插入
    new_order_id = orderlist_opt.insertOrderItem(orderDetail='json',
                                                 total=price, tableID=table, customerID=customerId)

    # 返回订单ID
    return jsonify({"OrderID": new_order_id})

# 顾客账号支付订单
@app.route('/restaurant/self/payment', methods=['POST'])
def customer_post_payment():
    if not request.json:
        abort(400)
    # 改变支付状态
    orderlist_opt.updateIsPaid(isPaid=request.json['items']['payment'],
                               orderID=request.json['items']['OrderID'])
    return jsonify("Paid is Updated")

# 餐厅账号进行或退出登录
@app.route('/restaurant/session', methods=['POST', 'DELETE'])
def restaurant_login():
    #将餐厅账号的信息存放至session
    if request.method == 'POST':
        if not request.json or not 'phone' or not 'password' in request.json:
            abort(400)
        phone = str(request.json['phone'])
        password = str(request.json['password'])
        session['phone'] = phone
        session['password'] = password
        restaurant_info = restaurant_opt.selectResturantInfoWithPP(phone,password)        
        restaurant_json = {
            "restaurantName": restaurant_info[0][1],
            "password": restaurant_info[0][2],
            "phone": restaurant_info[0][3],
            "email": restaurant_info[0][4],
        }
        return jsonify(restaurant_json)
    if request.method == 'DELETE':
        session.pop('phone')
        session.pop('password')
        return jsonify("Login Off")

# 餐厅账号获取菜单或新增菜品
@app.route('/restaurant/category', methods=['GET', 'POST'])
def restaurant_category():
    if request.method == 'GET':
        all_dish_type = dish_type_opt.selectAllDishType()
        menu_json = []
        for dish_type_row in all_dish_type:
            all_dish = dish_opt.selectAllDishWithDishTypeID(dish_type_row[0])
            all_dish_json = []
            for dish_id in all_dish:
                all_dish_json.append({
                    "dishID": dish_id,
                    "CategoryID": dish_type_row[0],
                    "name": dish_opt.selectDishNameWithDishID(dish_id),
                    "price": dish_opt.selectPriceWithDishID(dish_id),
                    "imageURL": dish_opt.selectDishImageURLWithDishID(dish_id),
                    "description": [
                        {
                            "comment": dish_opt.selectDishCommentWithDishID(dish_id),
                            "monthlySales": dish_opt.selectMonthlySalesWithDishID(dish_id),
                            "hot": dish_opt.selectDishHotWithDishID(dish_id)
                        }
                    ]
                })
            menu_json.append({
                "CategoryID": dish_type_row[0],
                "name": dish_type_row[1],
                "dish": all_dish_json
            })
        return jsonify(menu_json)
    if request.method == 'POST':
        if not request.json:
            abort(400)
        #dish的插入需要登录restaurant
        #dish_opt.manageDishTable(resturantName='test4', password='123456')
        #description的信息需要改动
        dish_opt.insertDishItem(dishName=request.json['items']['name'],
                                dishDescription="",
                                price=request.json['items']['price'],
                                dishImageURL=request.json['items']['imageURL'],
                                dishTypeID=request.json['items']['CategoryID'])
        dish_id = dish_opt.selectDishIDsWithDishName(
            request.json['items']['name'])
        return jsonify({"DishID": dish_id})


# 餐厅账号修改菜品信息或删除菜品
@app.route('/restaurant/dish/<int:dish_id>', methods=['PUT', 'DELETE'])
def restaurant_dish_change(dish_id):
    if request.method == 'PUT':
        if not request.json | ~dish_opt.identifyDishID(dishID=dish_id):
            abort(400)
        # 根据POST信息修改dish 需要先登录restaurant
        #dish_opt.manageDishTable(resturantName='test4', password='123456')
        dish_opt.updateDishName(request.json['items']['name'], dish_id)

        # 不注释这句话会报错： longj
        # dish_opt.updateCategoryID(request.json['items']['CategoryID'], dish_id)

        # POST信息中不包含OnSales
        #dish_opt.updateOnSaleWithDishID(onSale, dish_id)
        dish_opt.updatePriceWithDishID(request.json['items']['price'], dish_id)
        dish_opt.updateDishImageURLWithDishID(
            request.json['items']['imageURL'], dish_id)
        dish_opt.updateDishCommentWithDishID(
            request.json['items']['description']['comment'], dish_id)
        dish_opt.updateDishHotWithDishID(
            request.json['items']['description']['hot'], dish_id)
        dish_opt.updateMonthlySalesWithDishID(
            request.json['items']['description']['monthlySales'], dish_id)
        return jsonify("Update Dish")
    if request.method == 'DELETE':
        if not request.json | ~dish_opt.identifyDishID(dishID=dish_id):
            abort(400)
        dish_opt.deleteDishItemWithDishID(dishID=dish_id)
        return jsonify("Delete Dish")

# 餐厅账号新增分类
@app.route('/restaurant/category/', methods=['POST'])
def restaurant_category_add():
    # 异常返回
    if not request.json or not 'name' in request.json:
        abort(400)
    # 根据POST信息新增dishtype 需要先登录restaurant
    #dish_type_opt.manageDishTypeTable(resturantName='test4', password='123456')
    # 插入新的分类
    new_dish_type_name = request.json['name']
    dish_type_opt.insertDishTypeItem(dishTypeName=new_dish_type_name)
    return jsonify("Insert New DishType")


# 餐厅账号修改分类信息或删除分类
@app.route('/restaurant/category/<int:category_id>', methods=['PUT', 'DELETE'])
def restaurant_category_change(category_id):
    # 操作dishtype 需要先登录restaurant
    #dish_type_opt.manageDishTypeTable(resturantName='test4', password='123456')
    if request.method == 'PUT':
        if not request.json | dish_type_opt.selectDishTypeNameWithID(category_id) != '':
            abort(400)
        # 修改分类信息
        old_dish_type_name = dish_type_opt.selectDishTypeNameWithID(
            category_id)
        dish_type_opt.updateDishTypeName(
            old_dish_type_name, request.json['items']['name'])
        return jsonify("Update DishType")
    if request.method == 'DELETE':
        if dish_type_opt.selectDishTypeNameWithID(category_id) != '':
            abort(400)
        dish_type_opt.deleteDishTypeByID(dishTypeID=category_id)
        return jsonify("Delete DishType")


# 餐厅账号获取订单
@app.route('/restaurant/order', methods=['GET'])
def restaurant_order():
    # 每页订单的条目数
    pageSize = int(request.args.get('pageSize'))
    # 第几页订单
    pageNumber = int(request.args.get('pageNumber'))
    all_order = orderlist_opt.selectAllOrder()
    number_order_json = []
    for row in all_order:
        # 根据OrderID排序
        if ((pageNumber-1)*pageSize < row[0]) & (pageNumber*pageSize >= row[0]):
            number_order_json.append({
                "orderID": row[0],
                "dish": row[2],
                "status": row[4],
                "price": row[3],
                "payment": row[5],
                "time": row[6],
                "table": row[7],
                "customerId": row[8]
            })
    return jsonify(number_order_json)


# # 插入假数据的测试api
# @app.route('/insert_fake_data1', methods=['GET'])
# def insert_fake_data1():
#     return db_insert.insert_fake_data1()


# @app.route('/insert_fake_data2', methods=['GET'])
# def insert_fake_data2():
#     return data_importer.insert_fake_data2()


# 处理404样式
@app.errorhandler(404)
def not_found_404(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# 处理400样式
@app.errorhandler(400)
def not_found_400(error):
    return make_response(jsonify([{'code': 'string', 'message': 'string'}]), 400)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
