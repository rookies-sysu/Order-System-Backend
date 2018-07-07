import unittest
from test_db_basic import TestDbBasic
from test_db_dish import TestDbDish
from test_db_dishcomment import TestDbDishComment
from test_db_dishtype import TestDbDishType
from test_db_orderlist import TestDbOrderList
from test_db_qrlink import TestDbQRLink
from test_db_recommendation import TestDbRecommendation
from test_db_recommendationdetails import TestDbRecommendationDetails
from test_db_restaurant import TestDbRestaurant
from test_db_restauranttable import TestDbRestaurantTable

if __name__ == '__main__':
    suite = unittest.TestSuite()

    basic_tests = [TestDbBasic('test_select'), TestDbBasic('test_update')]
    suite.addTests(basic_tests)

    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDbDish))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDbDishComment))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDbDishType))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDbOrderList))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDbQRLink))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDbRecommendation))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDbRecommendationDetails))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDbRestaurant))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDbRestaurantTable))

    with open('UnittestTextReport.txt', 'w') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        runner.run(suite)