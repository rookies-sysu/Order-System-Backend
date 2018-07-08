import unittest
from dbTools import *

class TestDbDish(unittest.TestCase):
    def setUp(self):
        print('setUp...')
        self.opt = dishOperator()
        self.opt.manageDishTable(restaurantName='rName1', password='123456')

    def test_insert_and_delete(self):
        #插入用于辅助测试的dishtype
        dish_type_opt = dishTypeOperator(restaurantName='rName1', password='123456')
        dish_type_opt.insertDishTypeItem(dishTypeName="dishtype1")
        _, dishtype = selectOperator(tableName="DishType", dishTypeName="dishtype1", result=["dishTypeID"])
        
        #首次插入该dish
        state = self.opt.insertDishItem(dishName="testDishName", dishDescription="testDishDescription",
                                    price=10.0, dishImageURL="testDishImageURL", dishTypeID=dishtype[0]['dishTypeID'])
        self.assertEqual(True, state)
        #重复插入该dish
        state = self.opt.insertDishItem(dishName="testDishName", dishDescription="testDishDescription",
                                    price=10.0, dishImageURL="testDishImageURL", dishTypeID=dishtype[0]['dishTypeID'])
        self.assertEqual(False, state)
        #删除该dish
        _, result = selectOperator(tableName="Dish", dishName="testDishName", result=["dishID"])
        state = self.opt.deleteDishItemWithDishID(result[0]['dishID'])
        self.assertEqual(True, state)
        #重复删除dish
        state = self.opt.deleteDishItemWithDishID(result[0]['dishID'])
        self.assertEqual(False, state)

        dish_type_opt.deleteDishTypeByName(dishTypeName="dishtype1")

        pass

