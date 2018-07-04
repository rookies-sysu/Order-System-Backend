import unittest
from dbTools import *

class TestDbBasic(unittest.TestCase):
    def setUp(self):
        print('setUp...')
        self.rOpt = restaurantOperator()

    def test_select(self):
        state, res = selectOperator(tableName='Restaurant',
                          restaurantName='testName', result=['restaurantName', 'password', 'phone', 'email'])
        print(state, res)
        self.assertEqual(True, state)
        self.assertEqual('testName', res[0]['restaurantName'])
        self.assertEqual('testPassword', res[0]['password'])
        self.assertEqual('testPhone', res[0]['phone'])
        self.assertEqual('testEmail', res[0]['email'])

    def test_update(self):
        self.assertEqual(True, True)
        