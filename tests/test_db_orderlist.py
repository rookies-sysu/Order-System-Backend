import unittest
from dbTools import *

class TestDbOrderList(unittest.TestCase):
    test_cases_insert = [
        {
            'signIn': [False, '', ''],
            'customerID': 'c1',
            'tableID': 6,
            'result': -1
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'customerID': 'c5',
            'tableID': 8,
            'result': -1
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'customerID': 'c1',
            'tableID': 6,
            'result': 2
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'customerID': 'c2',
            'tableID': 6,
            'result': 2
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'customerID': 'c3',
            'tableID': 6,
            'result': 2
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'customerID': 'c4',
            'tableID': 6,
            'result': 2
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'customerID': 'c5',
            'tableID': 7,
            'result': 3
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'customerID': 'c6',
            'tableID': 6,
            'result': 2
        }
    ]

    test_cases_delete = [
        {
            'signIn': [False, '', ''],
            'orderID': 2,
            'tableID': '',
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'orderID': 11,
            'tableID': '',
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'orderID': '',
            'tableID': 8,
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'orderID': 2,
            'tableID': '',
            'result': True
        }
    ]

    def setUp(self):
        print("SetUp 'OrderList'...")

    def test_insert(self):
        self.oOpt = orderListOperator()
        for ca in self.test_cases_insert:
            if ca['signIn'][0]:
                self.oOpt.manageOrderListTable(restaurantName=ca['signIn'][1], password=ca['signIn'][2])
            state = self.oOpt.insertOrderItem(orderDetail='details', total=100.0, customerID=ca['customerID'], tableID=ca['tableID'])
            self.assertEqual(ca['result'], state)

    def test_delete(self):
        self.oOpt = orderListOperator()
        for ca in self.test_cases_delete:
            if ca['signIn'][0]:
                self.oOpt.manageOrderListTable(restaurantName=ca['signIn'][1], password=ca['signIn'][2])
            if ca['orderID'] == '':
                state = self.oOpt.deleteOrderItemsWithTableID(tableID=ca['tableID'])
            else:
                state = self.oOpt.deleteOrderItemWithOrderID(orderID=ca['orderID'])
            self.assertEqual(ca['result'], state)
