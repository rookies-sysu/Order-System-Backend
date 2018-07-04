-- MySQL Script generated by MySQL Workbench
-- Thu July 04 10:01:43 2018
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS
, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS
, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE
, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema TINYHIPPOTEST
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema TINYHIPPOTEST
-- -----------------------------------------------------
CREATE SCHEMA
IF NOT EXISTS `TINYHIPPOTEST` DEFAULT CHARACTER
SET utf8 ;
USE `TINYHIPPOTEST`
;

-- -----------------------------------------------------
-- Table `TINYHIPPOTEST`.`Restaurant`
-- -----------------------------------------------------
CREATE TABLE
IF NOT EXISTS `TINYHIPPOTEST`.`Restaurant`
(
  `restaurantID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `restaurantName` VARCHAR
(50) NOT NULL,
  `password` VARCHAR
(45) NOT NULL,
  `phone` VARCHAR
(45) NOT NULL,
  `email` VARCHAR
(45) NOT NULL,
  PRIMARY KEY
(`restaurantID`),
  UNIQUE INDEX `restaurantID_UNIQUE`
(`restaurantID` ASC),
  UNIQUE INDEX `restaurantName_UNIQUE`
(`restaurantName` ASC),
  UNIQUE INDEX `phone_UNIQUE`
(`phone` ASC),
  UNIQUE INDEX `email_UNIQUE`
(`email` ASC));


-- -----------------------------------------------------
-- Table `TINYHIPPOTEST`.`RestaurantTable`
-- -----------------------------------------------------
CREATE TABLE
IF NOT EXISTS `TINYHIPPOTEST`.`RestaurantTable`
(
  `tableID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `tableNumber` INT UNSIGNED NOT NULL,
  `currentOrderNumber` INT NOT NULL,
  `restaurantID` INT UNSIGNED NOT NULL,
  PRIMARY KEY
(`tableID`, `restaurantID`),
  UNIQUE INDEX `tableID_UNIQUE`
(`tableID` ASC),
  INDEX `fk_Table_Restaurant1_idx`
(`restaurantID` ASC),
  CONSTRAINT `fk_Table_Restaurant1`
    FOREIGN KEY
(`restaurantID`)
    REFERENCES `TINYHIPPOTEST`.`Restaurant`
(`restaurantID`)
    ON
DELETE NO ACTION
    ON
UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `TINYHIPPOTEST`.`OrderList`
-- -----------------------------------------------------
CREATE TABLE
IF NOT EXISTS `TINYHIPPOTEST`.`OrderList`
(
  `orderID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `orderNumber` INT NOT NULL,
  `orderDetail` VARCHAR
(5000) NOT NULL,
  `total` FLOAT NOT NULL,
  `isPaid` VARCHAR
(10) NOT NULL,
  `status` VARCHAR
(10) NOT NULL,
  `editedTime` DATETIME NOT NULL,
  `customerID` VARCHAR
(45) NOT NULL,
  `tableID` INT UNSIGNED NOT NULL,
  `restaurantID` INT UNSIGNED NOT NULL,
  PRIMARY KEY
(`orderID`, `tableID`),
  UNIQUE INDEX `orderID_UNIQUE`
(`orderID` ASC),
  INDEX `fk_OrderList_Table1_idx`
(`tableID` ASC),
  INDEX `fk_OrderList_Restaurant1_idx`
(`restaurantID` ASC),
  CONSTRAINT `fk_OrderList_Table1`
    FOREIGN KEY
(`tableID`)
    REFERENCES `TINYHIPPOTEST`.`RestaurantTable`
(`tableID`)
    ON
DELETE NO ACTION
    ON
UPDATE NO ACTION,
  CONSTRAINT `fk_OrderList_Restaurant1`
    FOREIGN KEY
(`restaurantID`)
    REFERENCES `TINYHIPPOTEST`.`Restaurant`
(`restaurantID`)
    ON
DELETE NO ACTION
    ON
UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `TINYHIPPOTEST`.`QRlink`
-- -----------------------------------------------------
CREATE TABLE
IF NOT EXISTS `TINYHIPPOTEST`.`QRlink`
(
  `linkID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `linkImageURL` VARCHAR
(255) NOT NULL,
  `tableID` INT UNSIGNED NOT NULL,
  PRIMARY KEY
(`linkID`, `tableID`),
  UNIQUE INDEX `linkID_UNIQUE`
(`linkID` ASC),
  UNIQUE INDEX `tableID_UNIQUE`
(`tableID` ASC),
  INDEX `fk_QRlink_RestaurantTable1_idx`
(`tableID` ASC),
  CONSTRAINT `fk_QRlink_RestaurantTable1`
    FOREIGN KEY
(`tableID`)
    REFERENCES `TINYHIPPOTEST`.`RestaurantTable`
(`tableID`)
    ON
DELETE NO ACTION
    ON
UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `TINYHIPPOTEST`.`DishType`
-- -----------------------------------------------------
CREATE TABLE
IF NOT EXISTS `TINYHIPPOTEST`.`DishType`
(
  `dishTypeID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `dishTypeName` VARCHAR
(255) NOT NULL,
  `restaurantID` INT UNSIGNED NOT NULL,
  PRIMARY KEY
(`dishTypeID`, `restaurantID`),
  UNIQUE INDEX `dishTypeID_UNIQUE`
(`dishTypeID` ASC),
  INDEX `fk_DishType_Restaurant1_idx`
(`restaurantID` ASC),
  CONSTRAINT `fk_DishType_Restaurant1`
    FOREIGN KEY
(`restaurantID`)
    REFERENCES `TINYHIPPOTEST`.`Restaurant`
(`restaurantID`)
    ON
DELETE NO ACTION
    ON
UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `TINYHIPPOTEST`.`Dish`
-- -----------------------------------------------------
CREATE TABLE
IF NOT EXISTS `TINYHIPPOTEST`.`Dish`
(
  `dishID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `dishName` VARCHAR
(255) NOT NULL,
  `dishDescription` VARCHAR
(255) NOT NULL,
  `onSale` TINYINT NOT NULL,
  `price` FLOAT NOT NULL,
  `dishImageURL` VARCHAR
(255) NOT NULL,
  `dishHot` TINYINT UNSIGNED NOT NULL,
  `monthlySales` INT UNSIGNED NOT NULL,
  `restaurantID` INT UNSIGNED NOT NULL,
  `dishTypeID` INT UNSIGNED NOT NULL,
  PRIMARY KEY
(`dishID`, `restaurantID`, `dishTypeID`),
  UNIQUE INDEX `dishID_UNIQUE`
(`dishID` ASC),
  INDEX `fk_Dish_Restaurant1_idx`
(`restaurantID` ASC),
  INDEX `fk_Dish_DishType1_idx`
(`dishTypeID` ASC),
  CONSTRAINT `fk_Dish_Restaurant1`
    FOREIGN KEY
(`restaurantID`)
    REFERENCES `TINYHIPPOTEST`.`Restaurant`
(`restaurantID`)
    ON
DELETE NO ACTION
    ON
UPDATE NO ACTION,
  CONSTRAINT `fk_Dish_DishType1`
    FOREIGN KEY
(`dishTypeID`)
    REFERENCES `TINYHIPPOTEST`.`DishType`
(`dishTypeID`)
    ON
DELETE NO ACTION
    ON
UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `TINYHIPPOTEST`.`DishComment`
-- -----------------------------------------------------
CREATE TABLE
IF NOT EXISTS `TINYHIPPOTEST`.`DishComment`
(
  `dishCommentID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `comment` VARCHAR
(255) NOT NULL,
  `dishID` INT UNSIGNED NOT NULL,
  PRIMARY KEY
(`dishCommentID`, `dishID`),
  UNIQUE INDEX `dishCommentID_UNIQUE`
(`dishCommentID` ASC),
  INDEX `fk_DishComment_Dish1_idx`
(`dishID` ASC),
  CONSTRAINT `fk_DishComment_Dish1`
    FOREIGN KEY
(`dishID`)
    REFERENCES `TINYHIPPOTEST`.`Dish`
(`dishID`)
    ON
DELETE NO ACTION
    ON
UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `TINYHIPPOTEST`.`Recommendation`
-- -----------------------------------------------------
CREATE TABLE
IF NOT EXISTS `TINYHIPPOTEST`.`Recommendation`
(
  `recommendationID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `title` VARCHAR
(45) NOT NULL,
  `tag` VARCHAR
(45) NOT NULL,
  `imageURL` VARCHAR
(255) NOT NULL,
  `editedTime` DATETIME NOT NULL,
  `restaurantID` INT UNSIGNED NOT NULL,
  INDEX `fk_Recommendation_Restaurant1_idx`
(`restaurantID` ASC),
  PRIMARY KEY
(`recommendationID`, `restaurantID`),
  CONSTRAINT `fk_Recommendation_Restaurant1`
    FOREIGN KEY
(`restaurantID`)
    REFERENCES `TINYHIPPOTEST`.`Restaurant`
(`restaurantID`)
    ON
DELETE NO ACTION
    ON
UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `TINYHIPPOTEST`.`RecommendationDetails`
-- -----------------------------------------------------
CREATE TABLE
IF NOT EXISTS `TINYHIPPOTEST`.`RecommendationDetails`
(
  `recommendationID` INT UNSIGNED NOT NULL,
  `dishID` INT UNSIGNED NOT NULL,
  `description` VARCHAR
(5000) NOT NULL,
  INDEX `fk_Recommendation_has_Dish_Recommendation1_idx`
(`recommendationID` ASC),
  CONSTRAINT `fk_Recommendation_has_Dish_Recommendation1`
    FOREIGN KEY
(`recommendationID`)
    REFERENCES `TINYHIPPOTEST`.`Recommendation`
(`recommendationID`)
    ON
DELETE NO ACTION
    ON
UPDATE NO ACTION,
  CONSTRAINT `fk_Recommendation_has_Dish_Dish1`
    FOREIGN KEY
(`dishID`)
    REFERENCES `TINYHIPPOTEST`.`Dish`
(`dishID`)
    ON
DELETE NO ACTION
    ON
UPDATE NO ACTION);

-- Insert Test Fake data for testing db select & update

INSERT INTO `
TINYHIPPOTEST`.`Restaurant
`
(restaurantName, password, phone, email) VALUES
('testName', 'testPassword', 'testPhone', 'testEmail');

SET SQL_MODE
=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS
=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS
=@OLD_UNIQUE_CHECKS;