import unittest
from dbTools import *

class TestDbRestaurantTable(unittest.TestCase):
    test_cases_insert = [
        {
            'signIn': [False, '', ''],
            'tableNumber': 2,
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'tableNumber': 2,
            'result': True
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'tableNumber': 2,
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'tableNumber': 3,
            'result': True
        },
        {
            'signIn': [True, 'rName2', '123456'],
            'tableNumber': 2,
            'result': True
        },
        {
            'signIn': [True, 'rName2', '123456'],
            'tableNumber': 4,
            'result': True
        }
    ]

    test_cases_delete = [
        {
            'signIn': [False, '', ''],
            'tableID': 2,
            'tableNumber': '',
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'tableID': 4,
            'tableNumber': '',
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'tableID': 6,
            'tableNumber': '',
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'tableID': '',
            'tableNumber': 4,
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'tableID': '',
            'tableNumber': 6,
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'tableID': 2,
            'tableNumber': '',
            'result': True
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'tableID': '',
            'tableNumber': 3,
            'result': True
        }
    ]
    def setUp(self):
        print("SetUp 'RestaurantTable'...")

    def test_insert(self):
        self.tOpt = tableOperator()
        for ca in self.test_cases_insert:
            if ca['signIn'][0]:
                self.tOpt.manageTableTable(restaurantName=ca['signIn'][1], password=ca['signIn'][2])
            state = self.tOpt.insertTableItem(tableNumber=ca['tableNumber'])
            self.assertEqual(ca['result'], state)

    def test_delete(self):
        self.tOpt = tableOperator()
        for ca in self.test_cases_delete:
            if ca['signIn'][0]:
                self.tOpt.manageTableTable(restaurantName=ca['signIn'][1], password=ca['signIn'][2])
            if ca['tableNumber'] == '':
                state = self.tOpt.deleteTableByID(tableID=ca['tableID'])
            else:
                state = self.tOpt.deleteTableByNumber(tableNumber=ca['tableNumber'])
            self.assertEqual(ca['result'], state)