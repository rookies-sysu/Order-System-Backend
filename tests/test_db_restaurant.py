import unittest
from dbTools import *

class TestDbRestaurant(unittest.TestCase):
    test_cases_insert = [
        {
            'restaurantName': 'rName1',
            'password': '123456',
            'phone': '10293847567',
            'email': 'rName1@mail.com',
            'result': True
        },
        {
            'restaurantName': 'rName1',
            'password': '123456',
            'phone': '10293847568',
            'email': 'rName2@mail.com',
            'result': False
        },
        {
            'restaurantName': 'rName2',
            'password': '12345',
            'phone': '10293847568',
            'email': 'rName2@mail.com',
            'result': False
        },
        {
            'restaurantName': 'rName2',
            'password': '111111111111111111111',
            'phone': '10293847568',
            'email': 'rName2@mail.com',
            'result': False
        },
        {
            'restaurantName': 'rName2',
            'password': '123456',
            'phone': '10293847567',
            'email': 'rName2@mail.com',
            'result': False
        },
        {
            'restaurantName': 'rName2',
            'password': '123456',
            'phone': '10293847568',
            'email': 'rName1@mail.com',
            'result': False
        },
        {
            'restaurantName': 'rName2',
            'password': '123456',
            'phone': '10293847568',
            'email': 'rName2@mail.com',
            'result': True
        }
    ]

    test_cases_delete = [
        {
            'signIn': [False, '', ''],
            'restaurantName': 'rName1',
            'restaurantID': '',
            'result': False
        },
        {
            'signIn': [False, '', ''],
            'restaurantName': '',
            'restaurantID': 2,
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'restaurantName': 'rName3',
            'restaurantID': '',
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'restaurantName': 'rName2',
            'restaurantID': '',
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'restaurantName': '',
            'restaurantID': 4,
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'restaurantName': 'rName1',
            'restaurantID': '',
            'result': True
        },
        {
            'signIn': [True, 'rName2', '123456'],
            'restaurantName': '',
            'restaurantID': 3,
            'result': True
        }
    ]

    def setUp(self):
        print("SetUp 'Restaurant'...")
        

    def test_insert(self):
        self.rOpt = restaurantOperator()
        for ca in self.test_cases_insert:
            state = self.rOpt.insertRestaurantItem(restaurantName=ca['restaurantName'], password=ca['password'],
                                phone=ca['phone'], email=ca['email'])
            self.assertEqual(ca['result'], state)
            if state:
                state, res = selectOperator(tableName='Restaurant', restaurantName=ca['restaurantName'], result=['restaurantName', 'password', 'phone', 'email'])
                self.assertEqual(True, state)
                self.assertEqual(ca['restaurantName'], res[0]['restaurantName'])
                self.assertEqual(ca['password'], res[0]['password'])
                self.assertEqual(ca['phone'], res[0]['phone'])
                self.assertEqual(ca['email'], res[0]['email'])

    def test_delete(self):
        self.rOpt = restaurantOperator()
        for ca in self.test_cases_delete:
            if ca['signIn'][0]:
                self.rOpt.manageRestaurantTable(restaurantName=ca['signIn'][1], password=ca['signIn'][2])
            if ca['restaurantName'] == '':
                state = self.rOpt.deleteRestaurantByID(restaurantID=ca['restaurantID'])
            else:
                state = self.rOpt.deleteRestaurantByName(restaurantName=ca['restaurantName'])
            self.assertEqual(ca['result'], state)
        