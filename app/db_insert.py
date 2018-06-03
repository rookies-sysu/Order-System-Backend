from dbOperators import *


def insert_fake_data1():
    try:
        #############
        # Resturant #
        #############
        rOpt = resturantOperator()
        # sign in
        rOpt.manageResturantTable(resturantName='test4', password='123456')
        # insert
        rOpt.insertResturantItem(resturantName='test1',
                                 password='123456', phone='123', email='123@email.com')
        rOpt.insertResturantItem(resturantName='test2',
                                 password='123456', phone='321', email='321@email.com')
        rOpt.insertResturantItem(
            resturantName='test3', password='123456', phone='1234', email='1234@email.com')
        rOpt.insertResturantItem(
            resturantName='test4', password='123456', phone='4321', email='4321@email.com')

        ############
        # DishType #
        ############
        dtOpt = dishTypeOperator()
        # sign in
        dtOpt.manageDishTypeTable(resturantName='test4', password='123456')
        # insert
        dtOpt.insertDishTypeItem(dishTypeName='dtype1')
        dtOpt.insertDishTypeItem(dishTypeName='dtype2')
        dtOpt.insertDishTypeItem(dishTypeName='dtype3')

        ##################
        # ResturantTable #
        ##################
        tOpt = tableOperator()
        # sign in
        tOpt.manageTableTable(resturantName='test4', password='123456')
        # insert
        tOpt.insertTableItem(tableNumber=1)
        tOpt.insertTableItem(tableNumber=2)
        tOpt.insertTableItem(tableNumber=3)
        tOpt.insertTableItem(tableNumber=4)

        ##########
        # QRlink #
        ##########
        lOpt = QRlinkOperator()
        # sign in
        lOpt.manageQRlinkTable(resturantName='test4', password='123456')
        # insert
        lOpt.insertQRlinkItem(linkImageURL='link-URL-4-1', tableNumber=1)
        lOpt.insertQRlinkItem(linkImageURL='link-URL-4-2', tableNumber=2)
        lOpt.insertQRlinkItem(linkImageURL='link-URL-4-3', tableNumber=3)
        lOpt.insertQRlinkItem(linkImageURL='link-URL-4-4', tableNumber=4)

        ########
        # Dish #
        ########
        dOpt = dishOperator()
        # sign in
        dOpt.manageDishTable(resturantName='test4', password='123456')
        # insert
        dOpt.insertDishItem(dishName='dish1', price=1,
                            dishImageURL='dish-img-URL-4-1', dishTypeID=1, dishDescription='aaa')
        dOpt.insertDishItem(dishName='dish2', price=2,
                            dishImageURL='dish-img-URL-4-2', dishTypeID=1, dishDescription='bbb')
        dOpt.insertDishItem(dishName='dish3', price=3,
                            dishImageURL='dish-img-URL-4-3', dishTypeID=2, dishDescription='ccc')

        ############
        # Customer #
        ############
        cOpt = customerOperator()
        # insert
        cOpt.insertCustomerItem(customerName='customer-4-1-1', linkID=1)
        cOpt.insertCustomerItem(customerName='customer-4-1-2', linkID=1)
        cOpt.insertCustomerItem(customerName='customer-4-1-3', linkID=1)
        cOpt.insertCustomerItem(customerName='customer-4-1-4', linkID=2)
        cOpt.insertCustomerItem(customerName='customer-4-2-1', linkID=2)
        cOpt.insertCustomerItem(customerName='customer-4-2-2', linkID=2)
        cOpt.insertCustomerItem(customerName='customer-4-2-3', linkID=3)

        # -----------------------------------------------------
        # Table `TINYHIPPO`.`Order`
        # -----------------------------------------------------
        oOpt = orderListOperator()
        # sign in
        # oOpt.manageOrderListTable(resturantName='test4', password='123456')
        # insert
        oOpt.insertOrderItem(orderDetail='json1',
                             total=100.0, tableID=1, customerID=1)
        oOpt.insertOrderItem(orderDetail='json2',
                             total=200.0, tableID=2, customerID=2)
        oOpt.insertOrderItem(orderDetail='json3',
                             total=300.0, tableID=3, customerID=3)
    except:
        return 'bad createDB'
    return 'Good createDB'
