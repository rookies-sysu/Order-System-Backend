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

    suite.addTests([TestDbRestaurant('test_insert'), TestDbRestaurant('test_delete')])
    suite.addTests([TestDbDishType('test_insert'), TestDbDishType('test_delete')])
    suite.addTests([TestDbRestaurantTable('test_insert'), TestDbRestaurantTable('test_delete')])
    suite.addTests([TestDbQRLink('test_insert'), TestDbQRLink('test_delete')])
    suite.addTests([TestDbDish('test_insert'), TestDbDish('test_delete')])
    suite.addTests([TestDbDishComment('test_insert'), TestDbDishComment('test_delete')])
    suite.addTests([TestDbOrderList('test_insert'), TestDbOrderList('test_delete')])
    suite.addTests([TestDbRecommendation('test_insert'), TestDbRecommendation('test_delete')])
    suite.addTests([TestDbRecommendationDetails('test_insert'), TestDbRecommendationDetails('test_delete')])
    suite.addTests([TestDbBasic('test_select'), TestDbBasic('test_update')])
    
    with open('UnittestTextReport.txt', 'w') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        runner.run(suite)