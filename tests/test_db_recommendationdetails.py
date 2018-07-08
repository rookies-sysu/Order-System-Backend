import unittest
from dbTools import *

class TestDbRecommendationDetails(unittest.TestCase):
    def setUp(self):
        print("SetUp 'RecommendationDetails'...")
        
    def test_insert(self):
        self.rcdOpt = RecommendationDetailsOperator()
        state = self.rcdOpt.insertRecommendationDetailsItem(
            recommendationID=6, dishID=10, description="balabalabala...")
        self.assertEqual(False, state)
        state = self.rcdOpt.insertRecommendationDetailsItem(
            recommendationID=3, dishID=11, description="balabalabala...")
        self.assertEqual(False, state)
        state = self.rcdOpt.insertRecommendationDetailsItem(
            recommendationID=4, dishID=10, description="balabalabala...")
        self.assertEqual(False, state)
        state = self.rcdOpt.insertRecommendationDetailsItem(
            recommendationID=4, dishID=8, description="balabalabala...")
        self.assertEqual(True, state)
        state = self.rcdOpt.insertRecommendationDetailsItem(
            recommendationID=4, dishID=9, description="balabalabala...")
        self.assertEqual(True, state)
    def test_delete(self):
        self.rcdOpt = RecommendationDetailsOperator()
        state = self.rcdOpt.deleteRecommendationDetailsByRecommendationID(recommendationID=8)
        self.assertEqual(False, state)
        state = self.rcdOpt.deleteRecommendationDetailsByDishID(dishID=11)
        self.assertEqual(False, state)
        state = self.rcdOpt.deleteRecommendationDetailsByDishID(dishID=9)
        self.assertEqual(True, state)
        state = self.rcdOpt.deleteRecommendationDetailsByRecommendationID(recommendationID=4)
        self.assertEqual(True, state)