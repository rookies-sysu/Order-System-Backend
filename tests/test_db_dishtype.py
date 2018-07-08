import unittest
from dbTools import *

class TestDbDishType(unittest.TestCase):
    def setUp(self):
        print('setUp...')
        self.opt = dishTypeOperator()

    def test_insert_and_delete(self):
        #未登录
        state = self.opt.insertDishTypeItem(dishTypeName="testDishType")
        self.assertEqual(False, state)
        #登录
        self.opt.manageDishTypeTable(restaurantName='rName1', password='123456')
        #首次插入dishtype
        state = self.opt.insertDishTypeItem(dishTypeName="testDishType")
        self.assertEqual(True, state)
        #重复插入dishtype
        state = self.opt.insertDishTypeItem(dishTypeName="testDishType")
        self.assertEqual(False, state)
        #首次删除dishtype
        state = self.opt.deleteDishTypeByName(dishTypeName="testDishType")
        self.assertEqual(True, state)
        #重复删除dishtype
        state = self.opt.deleteDishTypeByName(dishTypeName="testDishType")
        self.assertEqual(False, state)
