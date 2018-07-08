import unittest
from dbTools import *

class TestDbDishType(unittest.TestCase):
    def setUp(self):
        print('setUp...')
        self.opt = dishTypeOperator()
        self.opt.manageDishTypeTable(restaurantName='rName1', password='123456')

    def test_insert_and_delete(self):
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
