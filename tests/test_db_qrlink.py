import unittest
from dbTools import *

class TestDbQRLink(unittest.TestCase):
    def setUp(self):
        print('setUp...')
        self.opt = QRlinkOperator()

    def test_insert_and_delete(self):
        tOpt = tableOperator(restaurantName='rName1', password='123456')
        tOpt.insertTableItem(tableNumber=1)


        state = self.opt.insertQRlinkItem(linkImageURL="testlinkImageURL", tableNumber=1)
        self.assertEqual(False, state)

        self.opt.manageQRlinkTable(restaurantName='rName1', password='123456')

        state = self.opt.insertQRlinkItem(linkImageURL="testlinkImageURL", tableNumber=1)
        self.assertEqual(True, state)
        state = self.opt.insertQRlinkItem(linkImageURL="testlinkImageURL", tableNumber=1)
        self.assertEqual(False, state)


        state = self.opt.deleteLinkByURL(linkImageURL="testlinkImageURL")
        self.assertEqual(True, state)
        state = self.opt.deleteLinkByURL(linkImageURL="testlinkImageURL")
        self.assertEqual(False, state)

        tOpt.deleteTableByNumber(tableNumber=1)

