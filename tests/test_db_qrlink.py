import unittest
from dbTools import *

class TestDbQRLink(unittest.TestCase):
    test_cases_insert = [
        {
            'signIn': [False, '', ''],
            'linkImageURL': 'http://qrlink1.com',
            'tableNumber': 2,
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'linkImageURL': 'http://qrlink1.com',
            'tableNumber': 2,
            'result': True
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'linkImageURL': 'http://qrlink1.com',
            'tableNumber': 3,
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'linkImageURL': 'http://qrlink2.com',
            'tableNumber': 2,
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'linkImageURL': 'http://qrlink2.com',
            'tableNumber': 3,
            'result': True
        },
        {
            'signIn': [True, 'rName2', '123456'],
            'linkImageURL': 'http://qrlink3.com',
            'tableNumber': 2,
            'result': True
        },
        {
            'signIn': [True, 'rName2', '123456'],
            'linkImageURL': 'http://qrlink4.com',
            'tableNumber': 4,
            'result': True
        }
    ]

    test_cases_delete = [
        {
            'signIn': [False, '', ''],
            'linkID': 2,
            'linkImageURL': '',
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'linkID': 4,
            'linkImageURL': '',
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'linkID': 6,
            'linkImageURL': '',
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'linkID': '',
            'linkImageURL': 'http://qrlink3.com',
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'linkID': '',
            'linkImageURL': 'http://qrlink5.com',
            'result': False
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'linkID': 2,
            'linkImageURL': '',
            'result': True
        },
        {
            'signIn': [True, 'rName1', '123456'],
            'linkID': '',
            'linkImageURL': 'http://qrlink2.com',
            'result': True
        }
    ]

    def setUp(self):
        print("SetUp 'QRlink'...")
        tOpt = tableOperator()
        tOpt.manageTableTable(restaurantName='rName1', password='123456')
        tOpt.insertTableItem(tableNumber=2)
        tOpt.insertTableItem(tableNumber=3)

    def test_insert(self):
        self.qrOpt = QRlinkOperator()
        for ca in self.test_cases_insert:
            if ca['signIn'][0]:
                self.qrOpt.manageQRlinkTable(restaurantName=ca['signIn'][1], password=ca['signIn'][2])
            state = self.qrOpt.insertQRlinkItem(linkImageURL=ca['linkImageURL'], tableNumber=ca['tableNumber'])
            self.assertEqual(ca['result'], state)

    def test_delete(self):
        self.qrOpt = QRlinkOperator()
        for ca in self.test_cases_delete:
            if ca['signIn'][0]:
                self.qrOpt.manageQRlinkTable(restaurantName=ca['signIn'][1], password=ca['signIn'][2])
            if ca['linkImageURL'] == '':
                state = self.qrOpt.deleteLinkByID(linkID=ca['linkID'])
            else:
                state = self.qrOpt.deleteLinkByURL(linkImageURL=ca['linkImageURL'])
            self.assertEqual(ca['result'], state)
    