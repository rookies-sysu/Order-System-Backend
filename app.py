'''
from flask import Flask
import json
from flask.json import jsonify
import os

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_index_json():
    filename = os.path.join(app.instance_path, 'menu_database.json')
    f = open(filename, encoding='utf-8')
    res = json.load(f)
    return jsonify(res)


# @app.route('/confirm', methods=['POST'])
# def buy():
#     blablabla...

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
'''    

import config

import datetime, time, json, random

from flask import Flask, jsonify, render_template, request, session, abort, make_response

#特殊id
from uuid import uuid4
#验证信息
from flask_httpauth import HTTPBasicAuth
#引入OS模块中的产生一个24位的随机字符串的函数
import os

#调用数据库操作
import sys;
sys.path.append("./db")
from dbOperators import *

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

#随机产生24位的字符串作为SECRET_KEY
app.config['SECRET_KEY'] = os.urandom(24) 

app.debug = True

#提供认证机制
auth = HTTPBasicAuth()

#操作edit
edit_opt = editOperator()
edit_opt.manageEditTable(resturantName='test4', password='123456')
#操作dishType
dish_type_opt = dishTypeOperator()
dish_type_opt.manageDishTypeTable(resturantName='test4', password='123456')
#操作dish
dish_opt = dishOperator()
dish_opt.manageDishTable(resturantName='test4', password='123456')
#操作customer
customer_opt = customerOperator()
#操作Orderlist
orderlist_opt = orderListOperator()
orderlist_opt.manageOrderListTable(resturantName='test4', password='123456')
#操作Menu
menu_opt = menuOperator()
menu_opt.manageMenuTable(resturantName='test4', password='123456')
#操作Edit
edit_opt = editOperator()
edit_opt.manageEditTable(resturantName='test4', password='123456')


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
    all_menu = menu_opt.selectAllMenu()
    menu_json = []
    for menu_row in all_menu:
        all_dish = dish_opt.selectAllDishWithMenuID(menu_row[0])
        all_dish_json = []
        for dish_row in all_dish:
            all_dish_json.append({
                "dishID": dish_row[0],
                "CategoryID": menu_row[0],
                "name": dish_row[1],
                "price": dish_row[2],
                "imageURL": dish_row[3],
                "description": [
                    {
                        "comment": dish_row[4],
                        "monthlySales":  dish_row[6],
                        "hot": dish_row[5]
                    }
                ]
            })
        menu_json.append({
            "CategoryID": menu_row[0],
            "name": menu_row[1],
            "dish": all_dish_json
        })   
    return jsonify(menu_json)

#顾客账号下单
@app.route('/restaurant/self/order', methods=['POST'])
def customer_post_order():
    if not request.json:
        abort(400)
    dish_json = str(request.json['items']['dish'])
    price = request.json['items']['price']
    #生成新订单
    new_order_id = orderlist_opt.insertOrderItem(orderDishes=dish_json, total=price)
    #添加编写关系
    edit_opt.insertEditItem(customerName=session['customerName'], orderNumber=new_order_id)
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
        return jsonify("OK")
    if request.method == 'DELETE':
        session.pop('phone')
        session.pop('password')
        return jsonify("OK")

#餐厅账号获取菜单或新增菜品
@app.route('/restaurant/category', methods=['GET', 'POST'])
def restaurant_category():
    if request.method == 'GET':
        all_menu = menu_opt.selectAllMenu()
        menu_json = []
        for menu_row in all_menu:
            all_dish = dish_opt.selectAllDishWithMenuID(menu_row[0])
            all_dish_json = []
            for dish_row in all_dish:
                all_dish_json.append({
                    "dishID": dish_row[0],
                    "CategoryID": menu_row[0],
                    "name": dish_row[1],
                    "price": dish_row[2],
                    "imageURL": dish_row[3],
                    "description": [
                        {
                            "comment": dish_row[4],
                            "monthlySales":  dish_row[6],
                            "hot": dish_row[5]
                        }
                    ]
                })
            menu_json.append({
                "CategoryID": menu_row[0],
                "name": menu_row[1],
                "dish": all_dish_json
            })   
        return jsonify(menu_json)
    if request.method == 'POST':
        if not request.json:
            abort(400)
        dish_opt.insertDishItemByMenuID(dishName=request.json['items']['name'],
                            price=request.json['items']['price'],
                            dishImageURL=request.json['items']['imageURL'],
                            dishTypeName=dish_type_opt.selectDishTypeNameWithID(dishTypeID=request.json['items']['CategoryID']),
                            menuID=request.json['items']['CategoryID'])
        dish_id = dish_opt.selectDishIDsWithDishName(request.json['items']['name'])
        return jsonify({"DishID": dish_id})

#餐厅账号修改菜品信息或删除菜品
@app.route('/restaurant/dish/<int:dish_id>', methods=['PUT', 'DELETE'])
def restaurant_dish_change(dish_id):
    if request.method == 'PUT':
        if not request.json:
            abort(400)
            #根据POST信息修改dish

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
    new_dishtype_name = request.json['name']
    dish_type_opt.insertDishTypeItem(dishTypeName=new_dishtype_name)
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
            "orderID": row[1],
            "orderDishes": row[2],
            "status": row[3],
            "totalPrice": row[4],
            "isPaid": row[5]
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

'''
#回调函数,获取用户的密码
@auth.get_password
def get_password(username):
    if username == 'user':
        return '123456'
    return None
#回调函数,用于给客户端发送未授权错误代码
@auth.error_handler
def unauthorized():
    #当请求收到一个 401 的错误，网页浏览都会跳出一个登录框
    #403 错误表示 “禁止” 的错误
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

# 设置session
@app.route('/')
def set():
    session['username'] = 'liefyuan' # 设置“字典”键值对
    return 'success'
# 读取session
@app.route('/get')
def get():
    # session['username'] 如果内容不存在，将会报异常
    # session.get('username') 如果内容不存在，将返回None
    return session.get('username')
# 删除session
@app.route('/delete')
def delete():
    print (session.get('username'))
    session.pop('username')
    print (session.get('username'))
    return 'success'
# 清除session中所有数据
@app.route('/clear')
def clear():
    print (session.get('username'))
    # 清除session中所有数据
    session.clear
    print (session.get('username'))
    return 'success'
'''

if __name__ == '__main__':
    app.run()
