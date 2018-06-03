import datetime
import time
import json
import random

from flask import Flask, jsonify, render_template, request, session, abort, make_response
import redis

# 引入OS模块中的产生一个24位的随机字符串的函数
import os

# 调用数据库操作
import sys
from dbOperators import *

app = Flask(__name__, instance_relative_config=True)

# 随机产生24位的字符串作为SECRET_KEY
app.config['SECRET_KEY'] = os.urandom(24)

app.debug = True

# 操作dishType
dish_type_opt = dishTypeOperator()
#dish_type_opt.manageDishTypeTable(resturantName='test4', password='123456')
# 操作dish
dish_opt = dishOperator()
#dish_opt.manageDishTable(resturantName='test4', password='123456')
# 操作customer
customer_opt = customerOperator()
# 操作Orderlist
orderlist_opt = orderListOperator()
#orderlist_opt.manageOrderListTable(resturantName='test4', password='123456')


cache = redis.Redis(host='redis', port=6379)


# redis 样例
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


@app.route('/', methods=['GET'])
def index():
    count = get_hit_count()
    return 'Hello Tiny-Hippo Backend!! I have been seen {} times.\n'.format(count)

# 顾客账号获取用户自身信息


@app.route('/restaurant/customer/self', methods=['GET'])
def customer_info():
    if (session.get('CustomerID') == None):
        # 查找session中的customerName和linkID信息用于创建新的Customer
        #customer_opt.insertCustomerItem(customerName='customer-4-1-1', linkID=30)
        session['CustomerID'] = customer_opt.selectCustomerIDWithName(
            customerName='customer-4-1-1')
    return jsonify({'CustomerID': session['CustomerID']})

# 顾客账号获取菜单


@app.route('/restaurant/customer/category', methods=['GET'])
def customer_get_category():
    all_dish_type = dish_type_opt.selectAllDishType()
    menu_json = []
    for dish_type_row in all_dish_type:
        all_dish = dish_opt.selectAllDishWithDishTypeID(dish_type_row[0])
        all_dish_json = []
        for dish_row in all_dish:
            all_dish_json.append({
                "dishID": dish_row[0],
                "CategoryID": dish_type_row[0],
                "name": dish_row[1],
                "price": dish_row[3],
                "imageURL": dish_row[4],
                "description": [
                    {
                        "comment": dish_row[5],
                        "monthlySales":  dish_row[7],
                        "hot": dish_row[6]
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
    new_order_id = orderlist_opt.insertOrderItem(orderDetail="dish_json",
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
    # 将餐厅账号的信息存放至session
    if request.method == 'POST':
        if not request.json or not 'phone' or not 'password' in request.json:
            abort(400)
        session['phone'] = request.json['phone']
        session['password'] = request.json['password']
        return jsonify("Login In")
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
            for dish_row in all_dish:
                all_dish_json.append({
                    "dishID": dish_row[0],
                    "CategoryID": dish_type_row[0],
                    "name": dish_row[1],
                    "price": dish_row[3],
                    "imageURL": dish_row[4],
                    "description": [
                        {
                            "comment": dish_row[5],
                            "monthlySales":  dish_row[7],
                            "hot": dish_row[6]
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

        dish_opt.insertDishItem(dishName=request.json['items']['name'],
                                price=request.json['items']['price'],
                                dishImageURL=request.json['items']['imageURL'],
                                dishTypeID=request.json['items']['CategoryID'],
                                dishDescription=request.json['items']['dishDescription'])
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


is_create = False


@app.route('/CreateDB', methods=['GET'])
def createDB():
    try:
        #############
        # Resturant #
        #############
        rOpt = resturantOperator()
        # sign in
        rOpt.manageResturantTable(resturantName='test4', password='123456')
        # insert
        rOpt.insertResturantItem(resturantName='test1',
                                 password='123456', phone='123', email='123@email.com')
        rOpt.insertResturantItem(resturantName='test2',
                                 password='123456', phone='321', email='321@email.com')
        rOpt.insertResturantItem(
            resturantName='test3', password='123456', phone='1234', email='1234@email.com')
        rOpt.insertResturantItem(
            resturantName='test4', password='123456', phone='4321', email='4321@email.com')

        ############
        # DishType #
        ############
        dtOpt = dishTypeOperator()
        # sign in
        dtOpt.manageDishTypeTable(resturantName='test4', password='123456')
        # insert
        dtOpt.insertDishTypeItem(dishTypeName='dtype1')
        dtOpt.insertDishTypeItem(dishTypeName='dtype2')
        dtOpt.insertDishTypeItem(dishTypeName='dtype3')

        ##################
        # ResturantTable #
        ##################
        tOpt = tableOperator()
        # sign in
        tOpt.manageTableTable(resturantName='test4', password='123456')
        # insert
        tOpt.insertTableItem(tableNumber=1)
        tOpt.insertTableItem(tableNumber=2)
        tOpt.insertTableItem(tableNumber=3)
        tOpt.insertTableItem(tableNumber=4)

        ##########
        # QRlink #
        ##########
        lOpt = QRlinkOperator()
        # sign in
        lOpt.manageQRlinkTable(resturantName='test4', password='123456')
        # insert
        lOpt.insertQRlinkItem(linkImageURL='link-URL-4-1', tableNumber=1)
        lOpt.insertQRlinkItem(linkImageURL='link-URL-4-2', tableNumber=2)
        lOpt.insertQRlinkItem(linkImageURL='link-URL-4-3', tableNumber=3)
        lOpt.insertQRlinkItem(linkImageURL='link-URL-4-4', tableNumber=4)

        ########
        # Dish #
        ########
        dOpt = dishOperator()
        # sign in
        dOpt.manageDishTable(resturantName='test4', password='123456')
        # insert
        dOpt.insertDishItem(dishName='dish1', price=1,
                            dishImageURL='dish-img-URL-4-1', dishTypeID=1, dishDescription='aaa')
        dOpt.insertDishItem(dishName='dish2', price=2,
                            dishImageURL='dish-img-URL-4-2', dishTypeID=1, dishDescription='bbb')
        dOpt.insertDishItem(dishName='dish3', price=3,
                            dishImageURL='dish-img-URL-4-3', dishTypeID=2, dishDescription='ccc')

        ############
        # Customer #
        ############
        cOpt = customerOperator()
        # insert
        cOpt.insertCustomerItem(customerName='customer-4-1-1', linkID=1)
        cOpt.insertCustomerItem(customerName='customer-4-1-2', linkID=1)
        cOpt.insertCustomerItem(customerName='customer-4-1-3', linkID=1)
        cOpt.insertCustomerItem(customerName='customer-4-1-4', linkID=2)
        cOpt.insertCustomerItem(customerName='customer-4-2-1', linkID=2)
        cOpt.insertCustomerItem(customerName='customer-4-2-2', linkID=2)
        cOpt.insertCustomerItem(customerName='customer-4-2-3', linkID=3)

        # -----------------------------------------------------
        # Table `TINYHIPPO`.`Order`
        # -----------------------------------------------------
        oOpt = orderListOperator()
        # sign in
        # oOpt.manageOrderListTable(resturantName='test4', password='123456')
        # insert
        oOpt.insertOrderItem(orderDetail='json1',
                             total=100.0, tableID=1, customerID=1)
        oOpt.insertOrderItem(orderDetail='json2',
                             total=200.0, tableID=2, customerID=2)
        oOpt.insertOrderItem(orderDetail='json3',
                             total=300.0, tableID=3, customerID=3)
    except:
        return 'bad createDB'
    return 'Good createDB'

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
