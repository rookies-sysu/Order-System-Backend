import unittest
from dbTools import *

class TestDbRecommendationDetails(unittest.TestCase):
    def setUp(self):
        print("SetUp 'RecommendationDetails'...")
        
    def test_insert(self):
        self.rcdOpt = RecommendationDetailsOperator()
        self.rcdOpt.insertRecommendationDetailsItem(
            recommendationID=6, dishID=10, description="balabalabala...")
        self.rcdOpt.insertRecommendationDetailsItem(
            recommendationID=3, dishID=12, description="balabalabala...")
        self.rcdOpt.insertRecommendationDetailsItem(
            recommendationID=4, dishID=10, description="balabalabala...")
        self.rcdOpt.insertRecommendationDetailsItem(
            recommendationID=3, dishID=10, description="balabalabala...")
        self.rcdOpt.insertRecommendationDetailsItem(
            recommendationID=3, dishID=11, description="balabalabala...")
    def test_delete(self):
        self.rcdOpt = RecommendationDetailsOperator()
        self.rcdOpt.deleteRecommendationDetailsByRecommendationID(recommendationID=8)
        self.rcdOpt.deleteRecommendationDetailsByDishID(dishID=12)
        self.rcdOpt.deleteRecommendationDetailsByDishID(dishID=10)
        self.rcdOpt.deleteRecommendationDetailsByRecommendationID(recommendationID=3)