import unittest
from dbTools import *

class TestDbDish(unittest.TestCase):
    test_cases_insert = [
        {
            'signIn': [False, '', ''],
            'dishName': 'dish1',
            'dishDescription': 'This is dish1.',
            'price': 1.0,
            'dishImageURL': 'http://dish1.com',
            'dishTypeID': 6,
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'dishName': 'dish1',
            'dishDescription': 'This is dish1.',
            'price': 1.0,
            'dishImageURL': 'http://dish1.com',
            'dishTypeID': 6,
            'result': True
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'dishName': 'dish1',
            'dishDescription': 'This is dish1.',
            'price': 1.0,
            'dishImageURL': 'http://dish1.com',
            'dishTypeID': 6,
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'dishName': 'dish1',
            'dishDescription': 'This is dish1.',
            'price': 1.0,
            'dishImageURL': 'http://dish1.com',
            'dishTypeID': 8,
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'dishName': 'dish1',
            'dishDescription': 'This is dish1.',
            'price': 1.0,
            'dishImageURL': 'http://dish1.com',
            'dishTypeID': 4,
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'dishName': 'dish2',
            'dishDescription': 'This is dish2.',
            'price': 1.0,
            'dishImageURL': 'http://dish2.com',
            'dishTypeID': 6,
            'result': True
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'dishName': 'dish3',
            'dishDescription': 'This is dish3.',
            'price': 1.0,
            'dishImageURL': 'http://dish3.com',
            'dishTypeID': 7,
            'result': True
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'dishName': 'dish4',
            'dishDescription': 'This is dish4.',
            'price': 1.0,
            'dishImageURL': 'http://dish4.com',
            'dishTypeID': 7,
            'result': True
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'dishName': 'dish5',
            'dishDescription': 'This is dish5.',
            'price': 1.0,
            'dishImageURL': 'http://dish5.com',
            'dishTypeID': 6,
            'result': True
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'dishName': 'dish6',
            'dishDescription': 'This is dish6.',
            'price': 1.0,
            'dishImageURL': 'http://dish6.com',
            'dishTypeID': 6,
            'result': True
        },
        {
            'signIn': [True, 'rName2', '123456'],
            'dishName': 'dish1',
            'dishDescription': 'This is dish1.',
            'price': 1.0,
            'dishImageURL': 'http://dish1.com',
            'dishTypeID': 4,
            'result': True
        },
        {
            'signIn': [True, 'rName2', '123456'],
            'dishName': 'dish2',
            'dishDescription': 'This is dish2.',
            'price': 1.0,
            'dishImageURL': 'http://dish2.com',
            'dishTypeID': 4,
            'result': True
        }
    ]

    test_cases_delete = [
        {
            'signIn': [False, '', ''],
            'dishID': 2,
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'dishID': 8,
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'dishID': 10,
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'dishID': 2,
            'result': True
        }
    ]

    def setUp(self):
        print("SetUp 'Dish'...")
        dtOpt = dishTypeOperator()
        dtOpt.manageDishTypeTable(restaurantName='rName1', password='123456')
        dtOpt.insertDishTypeItem(dishTypeName="dtype1")
        dtOpt.insertDishTypeItem(dishTypeName="dtype2")

    def test_insert(self):
        self.dOpt = dishOperator()
        for ca in self.test_cases_insert:
            if ca['signIn'][0]:
                self.dOpt.manageDishTable(restaurantName=ca['signIn'][1], password=ca['signIn'][2])
            state = self.dOpt.insertDishItem(dishName=ca['dishName'], dishDescription=ca['dishDescription'], price=ca['price'], dishImageURL=ca['dishImageURL'], dishTypeID=ca['dishTypeID'])
            self.assertEqual(ca['result'], state)

    def test_delete(self):
        self.dOpt = dishOperator()
        for ca in self.test_cases_delete:
            if ca['signIn'][0]:
                self.dOpt.manageDishTable(restaurantName=ca['signIn'][1], password=ca['signIn'][2])
            state = self.dOpt.deleteDishItemWithDishID(dishID=ca['dishID'])
            self.assertEqual(ca['result'], state)
