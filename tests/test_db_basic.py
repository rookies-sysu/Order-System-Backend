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
        state = updateOperator(rstName='rName1', pwd='1234567', tableName='Restaurant',
                    restaurantName='rName1', new_phone='10293847569', new_restaurantName='rName2')
        self.assertEqual(False, state)
        state = updateOperator(rstName='rName1', pwd='123456', tableName='Restaurant',
                    restaurantName='rName1', new_password='1234567')
        self.assertEqual(True, state)
        state = updateOperator(rstName='rName1', pwd='1234567', tableName='Restaurant',
                    restaurantName='rName1', new_restaurantName='rName2')
        self.assertEqual(True, state)
        state = updateOperator(rstName='rName2', pwd='1234567', tableName='Restaurant',
                    restaurantName='rName2', new_password='123456')
        self.assertEqual(True, state)
        state = updateOperator(rstName='rName2', pwd='123456', tableName='Restaurant',
                    restaurantName='rName2', new_restaurantName='rName1')
        self.assertEqual(True, state)

        
