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
                    `orderID` INT UNSIGNED NOT NULL,
                    `tableID` INT UNSIGNED NOT NULL,
                    PRIMARY KEY (`customerID`, `tableID`),
                    UNIQUE INDEX `customer_id_UNIQUE` (`customerID` ASC),
                    INDEX `fk_Customer_Edit1_idx` (`orderID` ASC),
                    INDEX `fk_Customer_Table1_idx` (`tableID` ASC),
                    UNIQUE INDEX `customerName_UNIQUE` (`customerName` ASC),
                    CONSTRAINT `fk_Customer_Edit1`
                      FOREIGN KEY (`orderID`)
                      REFERENCES `TINYHIPPO`.`Edit` (`orderID`)
                      ON DELETE NO ACTION
                      ON UPDATE NO ACTION,
                    CONSTRAINT `fk_Customer_Table1`
                      FOREIGN KEY (`tableID`)
                      REFERENCES `TINYHIPPO`.`Table` (`tableID`)
                      ON DELETE NO ACTION
                      ON UPDATE NO ACTION);"""

## -----------------------------------------------------
## Table `TINYHIPPO`.`Resturant`
## -----------------------------------------------------
sql_resturant = """CREATE TABLE IF NOT EXISTS `TINYHIPPO`.`Resturant` (
                     `resturantID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
                     `resturantName` VARCHAR(50) NOT NULL,
                     `password` VARCHAR(45) NOT NULL,
                     PRIMARY KEY (`resturantID`),
                     UNIQUE INDEX `resturantID_UNIQUE` (`resturantID` ASC),
                     UNIQUE INDEX `resturantName_UNIQUE` (`resturantName` ASC));"""

## -----------------------------------------------------
## Table `TINYHIPPO`.`Order`
## -----------------------------------------------------
sql_order = """CREATE TABLE IF NOT EXISTS `TINYHIPPO`.`Order` (
                 `orderID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
                 `orderDishes` VARCHAR(500) NOT NULL,
                 `status` VARCHAR(20) NOT NULL,
                 `total` FLOAT NOT NULL,
                 `isPaid` VARCHAR(10) NOT NULL,
                 `customerID` INT UNSIGNED NOT NULL,
                 PRIMARY KEY (`orderID`, `customerID`),
                 INDEX `fk_Order_Edit_idx` (`customerID` ASC),
                 UNIQUE INDEX `orderID_UNIQUE` (`orderID` ASC),
                 CONSTRAINT `fk_Order_Edit`
                   FOREIGN KEY (`customerID`)
                   REFERENCES `TINYHIPPO`.`Edit` (`customerID`)
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
                PRIMARY KEY (`dishID`, `orderID`, `dishTypeID`, `menuID`),
                UNIQUE INDEX `dishID_UNIQUE` (`dishID` ASC),
                INDEX `fk_Dish_DishType1_idx` (`dishTypeID` ASC),
                INDEX `fk_Dish_Order1_idx` (`orderID` ASC),
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
## Table `TINYHIPPO`.`Table`
## -----------------------------------------------------
sql_table = """CREATE TABLE IF NOT EXISTS `TINYHIPPO`.`Table` (
                 `tableID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
                 `tableNumber` INT UNSIGNED NOT NULL,
                 `resturantID` INT UNSIGNED NOT NULL,
                 PRIMARY KEY (`tableID`, `resturantID`),
                 UNIQUE INDEX `tableNumber_UNIQUE` (`tableNumber` ASC),
                 UNIQUE INDEX `tableID_UNIQUE` (`tableID` ASC),
                 INDEX `fk_Table_Resturant1_idx` (`resturantID` ASC),
                 CONSTRAINT `fk_Table_Resturant1`
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
                  INDEX `fk_QRlink_Table1_idx` (`tableID` ASC),
                  CONSTRAINT `fk_QRlink_Table1`
                    FOREIGN KEY (`tableID`)
                    REFERENCES `TINYHIPPO`.`Table` (`tableID`)
                    ON DELETE NO ACTION
                    ON UPDATE NO ACTION);"""

## -----------------------------------------------------
## Table `TINYHIPPO`.`Edit`
## -----------------------------------------------------
sql_edit = """CREATE TABLE IF NOT EXISTS `TINYHIPPO`.`Edit` (
                `customerID` INT UNSIGNED NOT NULL,
                `orderID` INT UNSIGNED NOT NULL,
                `editedTime` DATE NOT NULL,
                PRIMARY KEY (`customerID`, `orderID`),
                UNIQUE INDEX `customerID_UNIQUE` (`customerID` ASC),
                UNIQUE INDEX `orderID_UNIQUE` (`orderID` ASC));"""

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