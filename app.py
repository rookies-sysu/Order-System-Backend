import datetime, time, json, random

from flask import Flask, jsonify, render_template, request, session, abort, make_response

#引入OS模块中的产生一个24位的随机字符串的函数
import os

#调用数据库操作
import sys;
sys.path.append("./db")
from dbOperators import *

app = Flask(__name__, instance_relative_config=True)

#随机产生24位的字符串作为SECRET_KEY
app.config['SECRET_KEY'] = os.urandom(24) 

app.debug = True

#操作dishType
dish_type_opt = dishTypeOperator()
#dish_type_opt.manageDishTypeTable(resturantName='test4', password='123456')
#操作dish
dish_opt = dishOperator()
#dish_opt.manageDishTable(resturantName='test4', password='123456')
#操作customer
customer_opt = customerOperator()
#操作Orderlist
orderlist_opt = orderListOperator()
#orderlist_opt.manageOrderListTable(resturantName='test4', password='123456')


#顾客账号获取用户自身信息 
@app.route('/restaurant/customer/self', methods=['GET'])
def customer_info():
    if (session.get('CustomerID') == None):
        #查找session中的customerName和linkID信息用于创建新的Customer
        #customer_opt.insertCustomerItem(customerName='customer-4-1-1', linkID=30)
        session['CustomerID'] = customer_opt.selectCustomerIDWithName(customerName='customer-4-1-1')
    return jsonify({'CustomerID':session['CustomerID']})

#顾客账号获取菜单
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

#顾客账号下单
@app.route('/restaurant/self/order', methods=['POST'])
def customer_post_order():
    if not request.json:
        abort(400)
    #订单信息
    dish_json = str(request.json['items']['dish'])
    price = request.json['items']['price']
    table = request.json['items']['table']
    customerId = request.json['items']['customerId']
    #生成新订单
    #目前dish_json内容无法插入
    new_order_id = orderlist_opt.insertOrderItem(orderDetail="dish_json",
                                                 total=price, tableID=table, customerID=customerId)
    #返回订单ID
    return jsonify({"OrderID": new_order_id})

#顾客账号支付订单
@app.route('/restaurant/self/payment', methods=['POST'])
def customer_post_payment():
    if not request.json:
        abort(400)
    #改变支付状态
    orderlist_opt.updateIsPaid(orderID=request.json['items']['OrderID'])
    return jsonify("Paid is Updated")

#餐厅账号进行或退出登录
@app.route('/restaurant/session', methods=['POST', 'DELETE'])
def restaurant_login():
    #将餐厅账号的信息存放至session
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

#餐厅账号获取菜单或新增菜品
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
                            dishTypeID=request.json['items']['CategoryID'])
        dish_id = dish_opt.selectDishIDsWithDishName(request.json['items']['name'])
        return jsonify({"DishID": dish_id})

#餐厅账号修改菜品信息或删除菜品
@app.route('/restaurant/dish/<int:dish_id>', methods=['PUT', 'DELETE'])
def restaurant_dish_change(dish_id):
    if request.method == 'PUT':
        if not request.json:
            abort(400)
        #根据POST信息修改dish 需要登录restaurant
        #dish_opt.manageDishTable(resturantName='test4', password='123456')
        dish_opt.updateDishName(request.json['items']['name'], dish_id)
        dish_opt.updateCategoryID(request.json['items']['CategoryID'], dish_id)
        #POST信息中不包含OnSales
        #dish_opt.updateOnSaleWithDishID(onSale, dish_id)
        dish_opt.updatePriceWithDishID(request.json['items']['price'], dish_id)
        dish_opt.updateDishImageURLWithDishID(request.json['items']['imageURL'], dish_id)
        dish_opt.updateDishCommentWithDishID(request.json['items']['description']['comment'], dish_id)
        dish_opt.updateDishHotWithDishID(request.json['items']['description']['hot'], dish_id)
        dish_opt.updateMonthlySalesWithDishID(request.json['items']['description']['monthlySales'], dish_id)
        return jsonify("Update Dish")
    if request.method == 'DELETE':
        dish_opt.deleteDishItemWithDishID(dishID=dish_id)
        return jsonify("Delete Dish")

#餐厅账号新增分类
@app.route('/restaurant/category/', methods=['POST'])
def restaurant_category_add():
    #异常返回
    if not request.json or not 'name' in request.json:
        abort(400)
    #插入新的分类
    new_dish_type_name = request.json['name']
    dish_type_opt.insertDishTypeItem(dishTypeName=new_dish_type_name)
    return jsonify("Insert New DishType")

#餐厅账号修改分类信息或删除分类           
@app.route('/restaurant/category/<int:category_id>', methods=['PUT', 'DELETE'])
def restaurant_category_change(category_id):
    if request.method == 'PUT':
        if not request.json:
            abort(400)
        #修改分类信息
        old_dish_type_name = dish_type_opt.selectDishTypeNameWithID(category_id)
        dish_type_opt.updateDishTypeName(old_dish_type_name, request.json['items']['name'])
        return jsonify("Update DishType")
    if request.method == 'DELETE':
        dish_type_opt.deleteDishTypeByID(dishTypeID=category_id)
        return jsonify("Delete DishType")

#餐厅账号获取订单(所有)
@app.route('/restaurant/order', methods=['GET'])
def restaurant_order():
    all_order = orderlist_opt.selectAllOrder()
    all_order_json = {"items": []}
    for row in all_order:
        all_order_json['items'].append({
            "orderID": row[0],
            "dish": row[2],
            "status": row[4],
            "price": row[3],
            "payment": row[5],
            "time": row[6],
            "table": row[7],
            "customerId": row[8]
        })
    return jsonify(all_order_json)


#处理404样式
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

#处理400样式
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify([{'code': 'string', 'message': 'string'}]), 400)

if __name__ == '__main__':
    app.run()
