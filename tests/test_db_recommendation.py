import unittest
from dbTools import *

class TestDbRecommendation(unittest.TestCase):
    test_cases_insert = [
        {
            'signIn': [False, '', ''],
            'title': 'spring',
            'tag': '123',
            'imageURL': 'http://img1.jpg',
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'title': 'spring',
            'tag': '123',
            'imageURL': 'http://img1.jpg',
            'result': True
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'title': 'summer',
            'tag': '456',
            'imageURL': 'http://img2.jpg',
            'result': True
        },
        {
            'signIn': [True, 'rName2', '123456'],
            'title': 'fall',
            'tag': '123',
            'imageURL': 'http://img3.jpg',
            'result': True
        },
        {
            'signIn': [True, 'rName2', '123456'],
            'title': 'winter',
            'tag': '456',
            'imageURL': 'http://img4.jpg',
            'result': True
        }
    ]

    test_cases_delete = [
        {
            'signIn': [False, '', ''],
            'recommendationID': 2,
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'recommendationID': 6,
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'recommendationID': 4,
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'recommendationID': 2,
            'result': True
        }
    ]

    def setUp(self):
        print("SetUp 'Recommendation'...")

    def test_insert(self):
        self.rcOpt = RecommendationOperator()
        for ca in self.test_cases_insert:
            if ca['signIn'][0]:
                self.rcOpt.manageRecommendationTable(restaurantName=ca['signIn'][1], password=ca['signIn'][2])
            state = self.rcOpt.insertRecommendationItem(title=ca['title'], tag=ca['tag'], imageURL=ca['imageURL'])
            self.assertEqual(ca['result'], state)

    def test_delete(self):
        self.rcOpt = RecommendationOperator()
        for ca in self.test_cases_delete:
            if ca['signIn'][0]:
                self.rcOpt.manageRecommendationTable(restaurantName=ca['signIn'][1], password=ca['signIn'][2])
            state = self.rcOpt.deleteRecommendationByID(recommendationID=ca['recommendationID'])
            self.assertEqual(ca['result'], state)