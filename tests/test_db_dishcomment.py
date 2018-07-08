import unittest
from dbTools import *

class TestDbDishComment(unittest.TestCase):
    test_cases_insert = [
        {
            'comment': 'good1',
            'dishID': 11,
            'result': False
        },
        {
            'comment': 'good1',
            'dishID': 9,
            'result': True
        },
        {
            'comment': 'good2',
            'dishID': 9,
            'result': True
        },
        {
            'comment': 'good2',
            'dishID': 10,
            'result': True
        }
    ]

    test_cases_delete = [
        {
            'dishCommentID': 5,
            'dishID': '',
            'result': False
        },
        {
            'dishCommentID': 4,
            'dishID': '',
            'result': True
        },
        {
            'dishCommentID': '',
            'dishID': 10,
            'result': False
        },
        {
            'dishCommentID': '',
            'dishID': 9,
            'result': True
        }
    ]

    def setUp(self):
        print("SetUp 'DishComment'...")
        dOpt = dishOperator()
        dOpt.manageDishTable(restaurantName='rName1', password='123456')
        dOpt.insertDishItem(dishName="dish1", dishDescription="This is dish1.",
                            price=1.0, dishImageURL="http://dish1.com", dishTypeID=6)
        dOpt.insertDishItem(dishName="dish2", dishDescription="This is dish2.",
                            price=1.0, dishImageURL="http://dish2.com", dishTypeID=6)

    def test_insert(self):
        self.dcOpt = dishCommentOperator()
        for ca in self.test_cases_insert:
            state = self.dcOpt.insertDishCommentItem(comment=ca['comment'], dishID=ca['dishID'])
            self.assertEqual(ca['result'], state)

    def test_delete(self):
        self.dcOpt = dishCommentOperator()
        for ca in self.test_cases_delete:
            if ca['dishCommentID'] == '':
                state = self.dcOpt.deleteDishCommentsWithDishID(dishID=ca['dishID'])
            else:
                state = self.dcOpt.deleteDishCommentByCommentID(dishCommentID=ca['dishCommentID'])
            self.assertEqual(ca['result'], state)
