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
                `dishTypeID` INT UNSIGNED NOT NULL,
                `menuID` INT UNSIGNED NOT NULL,
                PRIMARY KEY (`dishID`, `dishTypeID`, `menuID`),
                UNIQUE INDEX `dishID_UNIQUE` (`dishID` ASC),
                INDEX `fk_Dish_DishType1_idx` (`dishTypeID` ASC),
                INDEX `fk_Dish_Menu1_idx` (`menuID` ASC),
                CONSTRAINT `fk_Dish_DishType1`
                  FOREIGN KEY (`dishTypeID`)
                  REFERENCES `TINYHIPPO`.`DishType` (`dishTypeID`)
                  ON DELETE NO ACTION
                  ON UPDATE NO ACTION,
                CONSTRAINT `fk_Dish_Menu1`
                  FOREIGN KEY (`menuID`)
                  REFERENCES `TINYHIPPO`.`Menu` (`menuID`)
                  ON DELETE NO ACTION
                  ON UPDATE NO ACTION);"""

## -----------------------------------------------------
## Table `TINYHIPPO`.`DishType`
## -----------------------------------------------------
sql_dishType = """CREATE TABLE IF NOT EXISTS `TINYHIPPO`.`DishType` (
                    `dishTypeID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
                    `dishTypeName` VARCHAR(45) NOT NULL,
                    `resturantID` INT UNSIGNED NOT NULL,
                    PRIMARY KEY (`dishTypeID`, `resturantID`),
                    UNIQUE INDEX `dishTypeID_UNIQUE` (`dishTypeID` ASC),
                    INDEX `fk_DishType_Resturant1_idx` (`resturantID` ASC),
                    CONSTRAINT `fk_DishType_Resturant1`
                      FOREIGN KEY (`resturantID`)
                      REFERENCES `TINYHIPPO`.`Resturant` (`resturantID`)
                      ON DELETE NO ACTION
                      ON UPDATE NO ACTION);"""

## -----------------------------------------------------
## Table `TINYHIPPO`.`Menu`
## -----------------------------------------------------
sql_menu = """CREATE TABLE IF NOT EXISTS `TINYHIPPO`.`Menu` (
                `menuID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
                `menuTitle` VARCHAR(45) NOT NULL,
                `resturantID` INT UNSIGNED NOT NULL,
                PRIMARY KEY (`menuID`, `resturantID`),
                UNIQUE INDEX `menuID_UNIQUE` (`menuID` ASC),
                INDEX `fk_Menu_Resturant1_idx` (`resturantID` ASC),
                CONSTRAINT `fk_Menu_Resturant1`
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

# execute sql commands
cursor.execute(sql_resturant)
cursor.execute(sql_menu)
cursor.execute(sql_dishType)
cursor.execute(sql_table)
cursor.execute(sql_QRlink)
cursor.execute(sql_edit)
cursor.execute(sql_customer)
cursor.execute(sql_order)
cursor.execute(sql_dish)
 
# close the connection
db.close()