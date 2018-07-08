import unittest
from dbTools import *

class TestDbDishComment(unittest.TestCase):
    def setUp(self):
        print('setUp...')
        self.opt = dishCommentOperator()

    def test_insert_and_delete(self):
        #插入用于辅助测试的dishtype
        dish_type_opt = dishTypeOperator(restaurantName='rName1', password='123456')
        dish_type_opt.insertDishTypeItem(dishTypeName="dishtype1")
        _, dishtype = selectOperator(tableName="DishType", dishTypeName="dishtype1", result=["dishTypeID"])
        #插入用于辅助测试的dish
        dish_opt = dishOperator(restaurantName='rName1', password='123456')
        dish_opt.insertDishItem(dishName="testDishName", dishDescription="testDishDescription",
                            price=10.0, dishImageURL="testDishImageURL", dishTypeID=dishtype[0]['dishTypeID'])
        _, dish = selectOperator(tableName="Dish", dishName="testDishName", result=["dishID"])

        #插入comment
        state = self.opt.insertDishTypeItem(comment="testComment", dishID=dish[0]['dishID'])         
        self.assertEqual(True, state)
        #首次删除comment
        state = self.opt.deleteDishCommentsWithDishID(dish[0]['dishID'])
        self.assertEqual(True, state)
        #重复删除comment
        state = self.opt.deleteDishCommentsWithDishID(dish[0]['dishID'])
        self.assertEqual(False, state)

        dish_opt.deleteDishItemWithDishID(dish[0]['dishID'])
        dish_type_opt.deleteDishTypeByName(dishTypeName="dishtype1")
