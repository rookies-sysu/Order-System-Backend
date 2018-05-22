from dbOperators import *

#############
# Resturant #
#############
# rOpt = resturantOperator()
# # sign in
# rOpt.manageResturantTable(resturantName='test4', password='123456')
# # insert
# rOpt.insertResturantItem(resturantName='test1', password='123456', phone='123', email='123@email.com')
# rOpt.insertResturantItem(resturantName='test2', password='123456', phone='321', email='321@email.com')
# rOpt.insertResturantItem(resturantName='test3', password='123456', phone='1234', email='1234@email.com')
# rOpt.insertResturantItem(resturantName='test4', password='123456', phone='4321', email='4321@email.com')
# # update
# rOpt.updateResturantName(newName='test2')
# rOpt.updateResturantPhone(newPhone='321')
# rOpt.updateResturantEmail(newEmail='321@email.com')
# rOpt.updateResturantPassword(newPassword='654321', oldPassword='123456')
# # select
# print(rOpt.selectResturantIDWithName(resturantName='test2'))
# print(rOpt.selectResturantIDWithName(resturantName='test3'))
# print(rOpt.selectResturantIDWithPhone(phone='123'))
# print(rOpt.selectResturantIDWithPhone(phone='1234'))
# print(rOpt.selectResturantIDWithEmail(email='321@email.com'))
# print(rOpt.selectResturantIDWithEmail(email='4321@email.com'))
# print(rOpt.selectResturantNameWithID(resturantID=1))
# print(rOpt.selectResturantNameWithID(resturantID=10))

# print(rOpt.identifyResturantName(resturantName='test2'))
# print(rOpt.identifyResturantName(resturantName='test3'))
# print(rOpt.identifyResturantPhone(phone='123'))
# print(rOpt.identifyResturantPhone(phone='4123'))
# print(rOpt.identifyResturantEmail(email='321@email.com'))
# print(rOpt.identifyResturantEmail(email='321'))
# print(rOpt.identifyResturantID(resturantID=1))
# print(rOpt.identifyResturantID(resturantID=10))
# # delete
# rOpt.deleteResturantByID(resturantID=1)
# rOpt.deleteResturantByID(resturantID=1)
# rOpt.deleteResturantByName(resturantName='test2')
# rOpt.deleteResturantByName(resturantName='test4')


########
# Menu #
########
# mOpt = menuOperator()
# # sign in
# mOpt.manageMenuTable(resturantName='test4', password='123456')
# # insert
# mOpt.insertMenuItem(menuTitle='spring')
# mOpt.insertMenuItem(menuTitle='summer')
# # update
# mOpt.updateMenuTitle(oldTitle='spring', newTitle='spring2')
# #select
# print(mOpt.selectMenuIDWithTitle(menuTitle='spring2', resturantID=4))
# print(mOpt.selectMenuTitleWithID(menuID=2))
# print(mOpt.selectResturantIDWithMenuID(menuID=2))
# print(mOpt.selectMenuIDsWithResturantID(resturantID=4))
# print(mOpt.identifyMenuTitle(menuTitle='spring2'))
# print(mOpt.identifyMenuID(menuID=2))
# # delete
# mOpt.deleteMenuByID(menuID=1)
# mOpt.deleteMenuByTitle(menuTitle='spring')
# mOpt.deleteMenuByResturantID(resturantID=3)


############
# DishType #
############
# dtOpt = dishTypeOperator()
# # sign in
# dtOpt.manageDishTypeTable(resturantName='test4', password='123456')
# # insert
# dtOpt.insertDishTypeItem(dishTypeName='dtype1')
# dtOpt.insertDishTypeItem(dishTypeName='dtype2')
# dtOpt.insertDishTypeItem(dishTypeName='dtype3')
# # update
# dtOpt.updateDishTypeName(oldName='dtype1', newName='dtype2')
# # select
# print(dtOpt.selectDishTypeIDWithName(name='dtype2', resturantID=3))
# print(dtOpt.selectDishTypeIDWithName(name='dtype1', resturantID=3))
# print(dtOpt.selectDishTypeIDWithName(name='dtype0', resturantID=3))
# print(dtOpt.selectDishTypeNameWithID(dishTypeID=3))
# print(dtOpt.selectDishTypeIDsWithResturantID(resturantID=3))
# print(dtOpt.identifyDishTypeName(name='dtype2', resturantID=3))
# print(dtOpt.identifyDishTypeName(name='dtype1', resturantID=3))
# print(dtOpt.identifyDishTypeID(dishTypeID=4))
# print(dtOpt.identifyDishTypeID(dishTypeID=5))
# # delete
# dtOpt.deleteDishTypeByID(dishTypeID=1)
# dtOpt.deleteDishTypeByName(dishTypeName='dtype1')
# dtOpt.deleteDishTypeByResturantID(resturantID=4)


##################
# ResturantTable #
##################
# tOpt = tableOperator()
# # sign in
# tOpt.manageTableTable(resturantName='test4', password='123456')
# # insert
# tOpt.insertTableItem(tableNumber=1)
# tOpt.insertTableItem(tableNumber=2)
# tOpt.insertTableItem(tableNumber=3)
# tOpt.insertTableItem(tableNumber=4)
# # update
# tOpt.updateTableByNumber(oldNumber=5, newNumber=1)
# tOpt.updateTableByNumber(oldNumber=1, newNumber=5)
# # select
# print(tOpt.selectTableIDWithNumber(tableNumber=5, resturantID=1))
# print(tOpt.selectTableIDWithNumber(tableNumber=1, resturantID=1))
# print(tOpt.selectTableNumberWithID(tableID=1))
# print(tOpt.selectTableIDsWithResturantID(resturantID=1))
# print(tOpt.selectTableIDsWithResturantID(resturantID=2))
# print(tOpt.identifyTableNumber(number=1))
# print(tOpt.identifyTableNumber(number=2))
# print(tOpt.identifyTableID(tableID=1))
# print(tOpt.identifyTableID(tableID=17))
# delete
# tOpt.deleteTableByID(tableID=16)
# tOpt.deleteTableByID(tableID=17)
# tOpt.deleteTableByNumber(tableNumber=1)
# tOpt.deleteTableByResturantID(resturantID=4)


##########
# QRlink #
##########
# lOpt= QRlinkOperator()
# # sign in
# lOpt.manageQRlinkTable(resturantName='test4', password='123456')
# # insert
# lOpt.insertQRlinkItem(linkImageURL='link-URL-4-1', tableNumber=1)
# lOpt.insertQRlinkItem(linkImageURL='link-URL-4-2', tableNumber=2)
# lOpt.insertQRlinkItem(linkImageURL='link-URL-4-3', tableNumber=3)
# lOpt.insertQRlinkItem(linkImageURL='link-URL-4-4', tableNumber=4)
# # update
# lOpt.updateLinkImageURL(oldURL='link-URL-1', newURL='link-URL-1-1')
# lOpt.updateLinkImageURL(oldURL='link-URL-2', newURL='link-URL-1-2')
# lOpt.updateLinkImageURL(oldURL='link-URL-3', newURL='link-URL-1-3')
# lOpt.updateLinkImageURL(oldURL='link-URL-4', newURL='link-URL-1-4')
# lOpt.updateTableID(oldTableID=1, newTableID=2)
# # select
# print(lOpt.selectLinkIDWithURL(linkImageURL='link-URL-1-1'))
# print(lOpt.selectLinkIDWithURL(linkImageURL='link-URL-1-5'))
# print(lOpt.selectURLWithID(linkID=1))
# print(lOpt.selectURLWithID(linkID=18))
# print(lOpt.selectLinkIDWithTableID(tableID=1))
# print(lOpt.selectLinkIDWithTableID(tableID=18))
# print(lOpt.selectTableIDWithLinkID(linkID=1))
# print(lOpt.selectTableIDWithLinkID(linkID=18))
# print(lOpt.identifyLinkImageURL(linkImageURL='link-URL-1-1'))
# print(lOpt.identifyLinkImageURL(linkImageURL='link-URL-1-5'))
# print(lOpt.identifyLinkID(linkID=1))
# print(lOpt.identifyLinkID(linkID=18))
# # delete
# lOpt.deleteLinkByID(linkID=17)
# lOpt.deleteLinkByID(linkID=18)
# lOpt.deleteLinkByURL(linkImageURL='link-URL-4-2')
# lOpt.deleteLinkByURL(linkImageURL='link-URL-4-1')
# lOpt.deleteLinkByTableID(tableID=23)
# lOpt.deleteLinkByTableID(tableID=24)
# lOpt.deleteLinkByTableID(tableID=25)

########
# Dish #
########
# dOpt = dishOperator()
# # sign in
# dOpt.manageDishTable(resturantName='test4', password='123456')
# # insert
# dOpt.insertDishItem(dishName='dish1', price=1, dishImageURL='dish-img-URL-4-1', dishTypeName='dtype1', menuTitle='spring')
# dOpt.insertDishItem(dishName='dish2', price=2, dishImageURL='dish-img-URL-4-2', dishTypeName='dtype2', menuTitle='spring')
# dOpt.insertDishItem(dishName='dish3', price=3, dishImageURL='dish-img-URL-4-3', dishTypeName='dtype3', menuTitle='summer')

# update
# dOpt.updateDishName(oldDishName='dish1', newDishName='dish4', menuTitle='spring')
# dOpt.updatePrice(newPrice=4, dishName='dish4', menuTitle='spring')
# dOpt.updateDishImageURL(newDishImageURL='dish-img-URL-4-4', dishName='dish4', menuTitle='spring')
# dOpt.updateDishComment(newDishComment='good', dishName='dish4', menuTitle='spring')
# dOpt.updateDishHot(newDishHot=5, dishName='dish4', menuTitle='spring')
# dOpt.updateMonthlySales(newMonthlySales=50, dishName='dish4', menuTitle='spring')

# dOpt.updateDishName(oldDishName='dish1', newDishName='dish4', menuTitle='spring')
# dOpt.updatePrice(newPrice=4, dishName='dish1', menuTitle='spring')
# dOpt.updateDishImageURL(newDishImageURL='dish-img-URL-4-4', dishName='dish1', menuTitle='spring')
# dOpt.updateDishComment(newDishComment='good', dishName='dish1', menuTitle='spring')
# dOpt.updateDishHot(newDishHot=5, dishName='dish1', menuTitle='spring')
# dOpt.updateMonthlySales(newMonthlySales=50, dishName='dish1', menuTitle='spring')

# # select
# print(dOpt.selectPriceWithDishID(dishID=10))
# print(dOpt.selectDishImageURLWithDishID(dishID=10))
# print(dOpt.selectDishCommentWithDishID(dishID=10))
# print(dOpt.selectDishHotWithDishID(dishID=10))
# print(dOpt.selectMonthlySalesWithDishID(dishID=10))
# print(dOpt.selectDishIDWithDishName(dishName='dish4', menuID=13))
# print(dOpt.selectDishNameWithDishID(dishID=1, menuID=9))
# print(dOpt.selectMenuIDWithDishID(dishID=1))
# print(dOpt.selectDishIDsWithMenuID(menuID=9))
# print(dOpt.selectDishIDsWithDishTypeID(dishTypeID=13))
# print(dOpt.identifyDishID(dishID=1, menuID=9))
# print(dOpt.identifyDishName(dishName='dish1', menuID=9))

# print(dOpt.selectPriceWithDishID(dishID=21))
# print(dOpt.selectDishImageURLWithDishID(dishID=21))
# print(dOpt.selectDishCommentWithDishID(dishID=21))
# print(dOpt.selectDishHotWithDishID(dishID=21))
# print(dOpt.selectMonthlySalesWithDishID(dishID=21))
# print(dOpt.selectDishIDWithDishName(dishName='dish-img-URL-1-1', menuID=1))
# print(dOpt.selectDishNameWithDishID(dishID=1, menuID=1))
# print(dOpt.selectMenuIDWithDishID(dishID=10))
# print(dOpt.selectDishIDsWithMenuID(menuID=1))
# print(dOpt.selectDishIDsWithDishTypeID(dishTypeID=1))
# print(dOpt.identifyDishID(dishID=1, menuID=1))
# print(dOpt.identifyDishName(dishName='dish1', menuID=1))

# # delete
# dOpt.deleteDishItemWithDishID(dishID=10)
# dOpt.deleteDishItemsWithMenuID(menuID=13)
# dOpt.deleteDishItemsWithDishTypeID(dishTypeID=21)

# dOpt.deleteDishItemWithDishID(dishID=10)
# dOpt.deleteDishItemsWithMenuID(menuID=13)
# dOpt.deleteDishItemsWithDishTypeID(dishTypeID=21)

############
# Customer #
############
# cOpt = customerOperator()
# # insert
# cOpt.insertCustomerItem(customerName='customer-4-1-1', linkID=30)
# cOpt.insertCustomerItem(customerName='customer-4-1-2', linkID=30)
# cOpt.insertCustomerItem(customerName='customer-4-1-3', linkID=30)
# cOpt.insertCustomerItem(customerName='customer-4-1-4', linkID=30)
# cOpt.insertCustomerItem(customerName='customer-4-2-1', linkID=31)
# cOpt.insertCustomerItem(customerName='customer-4-2-2', linkID=31)
# cOpt.insertCustomerItem(customerName='customer-4-2-3', linkID=31)

# # update
# cOpt.updateCustomerName(oldCustomerName='customer-4-1-4', newCustomerName='customer-4-2-3')
# cOpt.updateTableIDWithCustomerName(customerName='customer-4-2-3', oldTableID=33, newTableID=34)

# # select
# print(cOpt.selectCustomerIDWithName(customerName='customer-4-1-1'))
# print(cOpt.selectCustomerNameWithID(customerID=1))
# print(cOpt.selectCustomerIDsWithTableID(tableID=33))
# print(cOpt.identifyCustomerName(customerName='customer-4-1-1'))
# print(cOpt.identifyCustomerID(customerID=1))
# print(cOpt.identifyTableID(tableID=33))

# print(cOpt.selectCustomerIDWithName(customerName='customer-4-1-4'))
# print(cOpt.selectCustomerNameWithID(customerID=9))
# print(cOpt.selectCustomerIDsWithTableID(tableID=35))
# print(cOpt.identifyCustomerName(customerName='customer-4-1-4'))
# print(cOpt.identifyCustomerID(customerID=9))
# print(cOpt.identifyTableID(tableID=35))

# # delete
# cOpt.deleteCustomerItemByCustomerID(customerID=5)
# cOpt.deleteCustomerItemByCustomerName(customerName='customer-4-2-2')
# cOpt.deleteCustomerItemsByTableID(tableID=34)

## -----------------------------------------------------
## Table `TINYHIPPO`.`Order`
## -----------------------------------------------------
# oOpt = orderListOperator()
# # sign in
# oOpt.manageOrderListTable(resturantName='test4', password='123456')
# insert
# oOpt.insertOrderItem(orderDishes='json1', total=100.0)
# oOpt.insertOrderItem(orderDishes='json2', total=200.0)

# # update
# oOpt.updateOrderDishes(newOrderDishes='json3', total=150.0, orderID=3)
# oOpt.updateTotal(total=180.0, orderID=3)
# oOpt.updateIsPaid(orderID=3)
# oOpt.updateStatusToDone(orderID=3)

# # select
# print(oOpt.selectOrderDishesWithOrderID(orderID=1))
# print(oOpt.selectStatusWithOrderID(orderID=1))
# print(oOpt.selectTotalWithOrderID(orderID=1))
# print(oOpt.selectIsPaidWithOrderID(orderID=1))
# print(oOpt.identifyOrderID(orderID=1))
# print(oOpt.selectOrderIDWithOrderNumber(orderNumber=1))
# print(oOpt.getMaxNumber())

# print(oOpt.selectOrderDishesWithOrderID(orderID=5))
# print(oOpt.selectStatusWithOrderID(orderID=5))
# print(oOpt.selectTotalWithOrderID(orderID=5))
# print(oOpt.selectIsPaidWithOrderID(orderID=5))
# print(oOpt.identifyOrderID(orderID=5))

# # delete
# oOpt.deleteOrderItemWithOrderID(orderID=9)
# oOpt.deleteOrderItemWithOrderID(orderID=6)
# oOpt.deleteOrderItemWithOrderID(orderID=7)

########
# Edit #
########

# eOpt = editOperator()
# # sign in
# eOpt.manageEditTable(resturantName='test4', password='123456')

# # insert
# eOpt.insertEditItem(customerName='customer-4-2-1', orderNumber=6)
# eOpt.insertEditItem(customerName='customer-4-2-2', orderNumber=6)
# eOpt.insertEditItem(customerName='customer-4-2-3', orderNumber=6)

# # update
# eOpt.updateOrderDishes(customerName='customer-4-2-1', orderNumber=6, newOrderDishes='json4', total=200.5)
# eOpt.updateIsPaid(isPaid='True', customerName='customer-4-2-1', orderNumber=6)
# eOpt.updateStatusToDone(customerName='customer-4-2-1', orderNumber=6)
# # select
# print(eOpt.selectCustomerIDsWithOrderID(orderID=8))
# print(eOpt.selectOrderIDsWithCustomerID(customerID=7))
# print(eOpt.selectEditedTimeWithCustomerIDAndOrderID(customerID=7, orderID=8))

# print(eOpt.identifyEditItem(customerID=7, orderID=8))
# print(eOpt.identifyEditItemWithCustomerID(customerID=7))
# print(eOpt.identifyEditItemWithOrderID(orderID=8))

# delete
# eOpt.deleteEditItemByCustomerIDAndOrderID(customerID=7, orderID=8)
# eOpt.deleteEditItemByCustomerID(customerID=8)
# eOpt.deleteEditItemByOrderID(orderID=8)