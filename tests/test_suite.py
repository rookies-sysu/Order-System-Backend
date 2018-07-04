import unittest
from test_db_basic import TestDbBasic
from test_db_restaurant import TestDbRestaurant

if __name__ == '__main__':
    suite = unittest.TestSuite()

    basic_tests = [TestDbBasic('test_select'), TestDbBasic('test_update')]
    suite.addTests(basic_tests)

    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDbRestaurant))

    with open('UnittestTextReport.txt', 'w') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        runner.run(suite)