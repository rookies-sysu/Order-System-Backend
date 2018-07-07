import unittest
from dbTools import *

class TestDbRestaurant(unittest.TestCase):
    test_cases = [
        {
            'id': 1,
            'restaurantName': 'rName1',
            'password': '123456',
            'phone': '10293847567',
            'email': 'rName1@mail.com'
        }
    ]

    def setUp(self):
        print('setUp...')
        self.rOpt = restaurantOperator()

    def test_insert(self):
        ca = self.test_cases[0]
        self.rOpt.insertRestaurantItem(restaurantName=ca['restaurantName'], password=ca['password'],
                            phone=ca['phone'], email=ca['email'])

        state, res = selectOperator(tableName='Restaurant', restaurantName=ca['restaurantName'], result=['restaurantName', 'password', 'phone', 'email'])
        print(res)
        self.assertEqual(True, state)
        self.assertEqual(ca['restaurantName'], res[0]['restaurantName'])
        self.assertEqual(ca['password'], res[0]['password'])
        self.assertEqual(ca['phone'], res[0]['phone'])
        self.assertEqual(ca['email'], res[0]['email'])

    def test_delete(self):
        pass
        