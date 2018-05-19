import pymysql
from getpass import getpass

# input the secrect of db
secrect = getpass("Connecting db..\n--> password: ")
# connect to dataset
db = pymysql.connect("localhost", "root", secrect, "TINYHIPPO" )
print('success!')
# create a cursor
cursor = db.cursor()

## -----------------------------------------------------
## Table `TINYHIPPO`.`Customer`
## -----------------------------------------------------
sql_customer = """CREATE TABLE IF NOT EXISTS `TINYHIPPO`.`Customer` (
                    `customerID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
                    `customerName` VARCHAR(20) NOT NULL,
                    `tableID` INT UNSIGNED NOT NULL,
                    PRIMARY KEY (`customerID`, `tableID`),
                    UNIQUE INDEX `customer_id_UNIQUE` (`customerID` ASC),
                    INDEX `fk_Customer_ResturantTable1_idx` (`tableID` ASC),
                    UNIQUE INDEX `customerName_UNIQUE` (`customerName` ASC),
                    CONSTRAINT `fk_Customer_ResturantTable1`
                      FOREIGN KEY (`tableID`)
                      REFERENCES `TINYHIPPO`.`ResturantTable` (`tableID`)
                      ON DELETE NO ACTION
                      ON UPDATE NO ACTION);"""

## -----------------------------------------------------
## Table `TINYHIPPO`.`Resturant`
## -----------------------------------------------------
sql_resturant = """CREATE TABLE IF NOT EXISTS `TINYHIPPO`.`Resturant` (
                     `resturantID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
                     `resturantName` VARCHAR(50) NOT NULL,
                     `password` VARCHAR(45) NOT NULL,
                     `phone` VARCHAR(45) NOT NULL,
                     `email` VARCHAR(45) NOT NULL,
                     PRIMARY KEY (`resturantID`),
                     UNIQUE INDEX `resturantID_UNIQUE` (`resturantID` ASC),
                     UNIQUE INDEX `resturantName_UNIQUE` (`resturantName` ASC));"""

## -----------------------------------------------------
## Table `TINYHIPPO`.`OrderList`
## -----------------------------------------------------
sql_order = """CREATE TABLE IF NOT EXISTS `TINYHIPPO`.`OrderList` (
                 `orderID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
                 `orderNumber` INT UNSIGNED NOT NULL,
                 `orderDishes` VARCHAR(500) NOT NULL,
                 `status` VARCHAR(20) NOT NULL,
                 `total` FLOAT NOT NULL,
                 `isPaid` VARCHAR(10) NOT NULL,
                 `resturantID` INT UNSIGNED NOT NULL,
                 PRIMARY KEY (`orderID`, `resturantID`),
                 UNIQUE INDEX `orderID_UNIQUE` (`orderID` ASC),
                 INDEX `fk_OrderList_Resturant1_idx` (`resturantID` ASC),
                 CONSTRAINT `fk_OrderList_Resturant1`
                   FOREIGN KEY (`resturantID`)
                   REFERENCES `TINYHIPPO`.`Resturant` (`resturantID`)
                   ON DELETE NO ACTION
                   ON UPDATE NO ACTION);"""

## -----------------------------------------------------
## Table `TINYHIPPO`.`Dish`
## -----------------------------------------------------
sql_dish = """CREATE TABLE IF NOT EXISTS `TINYHIPPO`.`Dish` (
                `dishID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
                `dishName` VARCHAR(255) NOT NULL,
                `price` FLOAT NOT NULL,
                `dishImageURL` VARCHAR(255) NOT NULL,
                `dishComment` VARCHAR(255) NOT NULL,
                `dishHot` INT UNSIGNED NOT NULL,
                `monthlySales` INT UNSIGNED NOT NULL,
                `resturantID` INT UNSIGNED NOT NULL,
                PRIMARY KEY (`dishID`, `resturantID`),
                UNIQUE INDEX `dishID_UNIQUE` (`dishID` ASC),
                INDEX `fk_Dish_Resturant1_idx` (`resturantID` ASC),
                CONSTRAINT `fk_Dish_Resturant1`
                  FOREIGN KEY (`resturantID`)
                  REFERENCES `TINYHIPPO`.`Resturant` (`resturantID`)
                  ON DELETE NO ACTION
                  ON UPDATE NO ACTION);"""

## -----------------------------------------------------
## Table `TINYHIPPO`.`Category`
## -----------------------------------------------------
sql_category = """CREATE TABLE IF NOT EXISTS `TINYHIPPO`.`Category` (
                `categoryID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
                `categoryTitle` VARCHAR(45) NOT NULL,
                `resturantID` INT UNSIGNED NOT NULL,
                PRIMARY KEY (`categoryID`, `resturantID`),
                UNIQUE INDEX `categoryID_UNIQUE` (`categoryID` ASC),
                INDEX `fk_Category_Resturant1_idx` (`resturantID` ASC),
                CONSTRAINT `fk_Category_Resturant1`
                  FOREIGN KEY (`resturantID`)
                  REFERENCES `TINYHIPPO`.`Resturant` (`resturantID`)
                  ON DELETE NO ACTION
                  ON UPDATE NO ACTION);"""

## -----------------------------------------------------
## Table `TINYHIPPO`.`ResturantTable`
## -----------------------------------------------------
sql_table = """CREATE TABLE IF NOT EXISTS `TINYHIPPO`.`ResturantTable` (
                 `tableID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
                 `tableNumber` INT UNSIGNED NOT NULL,
                 `resturantID` INT UNSIGNED NOT NULL,
                 PRIMARY KEY (`tableID`, `resturantID`),
                 UNIQUE INDEX `tableID_UNIQUE` (`tableID` ASC),
                 INDEX `fk_ResturantTable_Resturant1_idx` (`resturantID` ASC),
                 CONSTRAINT `fk_ResturantTable_Resturant1`
                   FOREIGN KEY (`resturantID`)
                   REFERENCES `TINYHIPPO`.`Resturant` (`resturantID`)
                   ON DELETE NO ACTION
                   ON UPDATE NO ACTION);"""

## -----------------------------------------------------
## Table `TINYHIPPO`.`QRlink`
## -----------------------------------------------------
sql_QRlink = """CREATE TABLE IF NOT EXISTS `TINYHIPPO`.`QRlink` (
                  `linkID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
                  `linkImageURL` VARCHAR(255) NOT NULL,
                  `tableID` INT UNSIGNED NOT NULL,
                  PRIMARY KEY (`linkID`, `tableID`),
                  UNIQUE INDEX `linkID_UNIQUE` (`linkID` ASC),
                  INDEX `fk_QRlink_ResturantTable1_idx` (`tableID` ASC),
                  CONSTRAINT `fk_QRlink_ResturantTable1`
                    FOREIGN KEY (`tableID`)
                    REFERENCES `TINYHIPPO`.`ResturantTable` (`tableID`)
                    ON DELETE NO ACTION
                    ON UPDATE NO ACTION);"""

## -----------------------------------------------------
## Table `TINYHIPPO`.`EditRelation`
## -----------------------------------------------------
sql_edit = """CREATE TABLE IF NOT EXISTS `TINYHIPPO`.`EditRelation` (
                `customerID` INT UNSIGNED NOT NULL,
                `orderID` INT UNSIGNED NOT NULL,
                `editedTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
                `resturantID` INT UNSIGNED NOT NULL,
                PRIMARY KEY (`customerID`, `orderID`, `resturantID`),
                UNIQUE INDEX `customerID_UNIQUE` (`customerID` ASC),
                INDEX `fk_EditRelation_Resturant1_idx` (`resturantID` ASC),
                CONSTRAINT `fk_EditRelation_Resturant1`
                  FOREIGN KEY (`resturantID`)
                  REFERENCES `TINYHIPPO`.`Resturant` (`resturantID`)
                  ON DELETE NO ACTION
                  ON UPDATE NO ACTION);"""
## -----------------------------------------------------
## Table `TINYHIPPO`.`ManageCategory`
## -----------------------------------------------------
sql_manageCategory = """CREATE TABLE IF NOT EXISTS `TINYHIPPO`.`ManageCategory` (
                      `categoryID` INT UNSIGNED NOT NULL,
                      `dishID` INT UNSIGNED NOT NULL,
                      `resturantID` INT UNSIGNED NOT NULL,
                      PRIMARY KEY (`categoryID`, `dishID`, `resturantID`),
                      UNIQUE INDEX `customerID_UNIQUE` (`categoryID` ASC),
                      INDEX `fk_ManageCategory_Resturant1_idx` (`resturantID` ASC),
                      CONSTRAINT `fk_ManageCategory_Resturant1`
                        FOREIGN KEY (`resturantID`)
                        REFERENCES `TINYHIPPO`.`Resturant` (`resturantID`)
                        ON DELETE NO ACTION
                        ON UPDATE NO ACTION);"""

# execute sql commands
cursor.execute(sql_resturant)
cursor.execute(sql_category)
cursor.execute(sql_table)
cursor.execute(sql_QRlink)
cursor.execute(sql_edit)
cursor.execute(sql_customer)
cursor.execute(sql_order)
cursor.execute(sql_dish)
cursor.execute(sql_manageCategory)
 
# close the connection
db.close()