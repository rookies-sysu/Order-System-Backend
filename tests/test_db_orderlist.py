import unittest
from dbTools import *

class TestDbOrderList(unittest.TestCase):
    def setUp(self):
        print('setUp...')
        self.opt = orderListOperator()
        self.opt.manageOrderListTable(restaurantName='rName1', password='123456')

    def test_insert_and_delete(self):
        #插入用于辅助测试的table
        tOpt = tableOperator(restaurantName='rName1', password='123456')
        tOpt.insertTableItem(tableNumber=10)
        _, table = selectOperator(tableName="RestaurantTable", tableNumber=10, result=["tableID"])

        #插入order
        number = self.opt.insertOrderItem(orderDetail="testOrderDetail", total=10.0, 
                                    customerID="testCustomerID", tableID=table[0]['tableID'])
        if (number != -1):
            self.assertEqual(True, True)

        _, orderId = selectOperator(tableName="OrderList", orderNumber=number, result=["orderID"])
        #首次删除order
        state = self.opt.deleteOrderItemWithOrderID(orderID=orderId[0]['orderID'])
        self.assertEqual(True, state)
        #重复删除order
        state = self.opt.deleteOrderItemWithOrderID(orderID=orderId[0]['orderID'])
        self.assertEqual(False, state)

        tOpt.deleteTableByNumber(tableNumber=10)
