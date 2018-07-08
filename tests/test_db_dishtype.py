import unittest
from dbTools import *

class TestDbDishType(unittest.TestCase):
    test_cases_insert = [
        {
            'signIn': [False, '', ''],
            'dishTypeName': 'dtype1',
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'dishTypeName': 'dtype1',
            'result': True
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'dishTypeName': 'dtype1',
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'dishTypeName': 'dtype2',
            'result': True
        },
        {
            'signIn': [True, 'rName2', '123456'],
            'dishTypeName': 'dtype1',
            'result': True
        },
        {
            'signIn': [True, 'rName2', '123456'],
            'dishTypeName': 'dtype3',
            'result': True
        }
    ]

    test_cases_delete = [
        {
            'signIn': [False, '', ''],
            'dishTypeName': '',
            'dishTypeID': 1,
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'dishTypeName': '',
            'dishTypeID': 4,
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'dishTypeName': '',
            'dishTypeID': 6,
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'dishTypeName': 'dtype3',
            'dishTypeID': '',
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'dishTypeName': 'dtype5',
            'dishTypeID': '',
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'dishTypeName': '',
            'dishTypeID': 2,
            'result': True
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'dishTypeName': 'dtype2',
            'dishTypeID': '',
            'result': True
        }
    ]
    def setUp(self):
        print("SetUp 'DishType'...")
        rOpt = restaurantOperator()
        rOpt.insertRestaurantItem(restaurantName='rName1', password='123456',
                                phone='10293847567', email='rName1@mail.com')
        rOpt.insertRestaurantItem(restaurantName='rName2', password='123456',
                                phone='10293847568', email='rName2@mail.com')

    def test_insert(self):
        self.dtOpt = dishTypeOperator()
        for ca in self.test_cases_insert:
            if ca['signIn'][0]:
                self.dtOpt.manageDishTypeTable(restaurantName=ca['signIn'][1], password=ca['signIn'][2])
            state = self.dtOpt.insertDishTypeItem(dishTypeName=ca['dishTypeName'])
            self.assertEqual(ca['result'], state)

    def test_delete(self):
        self.dtOpt = dishTypeOperator()
        for ca in self.test_cases_delete:
            if ca['signIn'][0]:
                self.dtOpt.manageDishTypeTable(restaurantName=ca['signIn'][1], password=ca['signIn'][2])
            if ca['dishTypeName'] == '':
                state = self.dtOpt.deleteDishTypeByID(dishTypeID=ca['dishTypeID'])
            else:
                state = self.dtOpt.deleteDishTypeByName(dishTypeName=ca['dishTypeName'])
            self.assertEqual(ca['result'], state)