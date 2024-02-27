-- MySQL dump 10.13  Distrib 8.0.33, for Linux (aarch64)
--
-- Host: localhost    Database: banking
-- ------------------------------------------------------
-- Server version       8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `banking`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `banking` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `banking`;

--
-- Table structure for table `Account`
--

DROP TABLE IF EXISTS `Account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Account` (
  `ACCOUNTID` int NOT NULL AUTO_INCREMENT,
  `CUSTOMERID` int DEFAULT NULL,
  `ACCOUNTTYPEID` int DEFAULT NULL,
  `ACCOUNTTYPENAME` varchar(25) DEFAULT NULL,
  `BALANCE` decimal(15,2) DEFAULT '0.00',
  `STARTDATE` datetime DEFAULT NULL,
  `ENDDATE` datetime DEFAULT NULL,
  `ENTITYID` int DEFAULT '1',
  `OFFICEID` int DEFAULT '1',
  `CDID` varchar(25) DEFAULT NULL,
  `ANID` varchar(25) DEFAULT NULL,
  `INTERESRATE` decimal(15,2) DEFAULT '0.00',
  PRIMARY KEY (`ACCOUNTID`),
  KEY `CUSTOMERID` (`CUSTOMERID`),
  KEY `Account_fk2` (`ACCOUNTTYPEID`),
  CONSTRAINT `AccountTypeFK` FOREIGN KEY (`ACCOUNTTYPEID`) REFERENCES `AccountType` (`AcctID`),
  CONSTRAINT `CustomerHasAccountFK` FOREIGN KEY (`CUSTOMERID`) REFERENCES `Customer` (`CUSTOMERID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Account`
--

LOCK TABLES `Account` WRITE;
/*!40000 ALTER TABLE `Account` DISABLE KEYS */;
INSERT INTO `Account` VALUES (6,10602,1,'Checking',1001.00,'2024-02-24 00:00:00',NULL,1,1,NULL,NULL,0.00),(7,10602,2,'Savings',99.00,'2024-02-24 00:00:00','2024-02-27 09:33:49',1,1,NULL,NULL,0.00);
/*!40000 ALTER TABLE `Account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `AccountType`
--

DROP TABLE IF EXISTS `AccountType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `AccountType` (
  `AcctID` int NOT NULL AUTO_INCREMENT,
  `NAME` varchar(25) NOT NULL,
  PRIMARY KEY (`AcctID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AccountType`
--

LOCK TABLES `AccountType` WRITE;
/*!40000 ALTER TABLE `AccountType` DISABLE KEYS */;
INSERT INTO `AccountType` VALUES (1,'Checking'),(2,'Savings');
/*!40000 ALTER TABLE `AccountType` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Branch`
--

DROP TABLE IF EXISTS `Branch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Branch` (
  `OFFICEID` int NOT NULL AUTO_INCREMENT,
  `NAME` varchar(100) DEFAULT NULL,
  `ADDRESS` varchar(100) DEFAULT NULL,
  `STARTDATE` datetime DEFAULT NULL,
  PRIMARY KEY (`OFFICEID`)
) ENGINE=InnoDB AUTO_INCREMENT=123125 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Branch`
--

LOCK TABLES `Branch` WRITE;
/*!40000 ALTER TABLE `Branch` DISABLE KEYS */;
INSERT INTO `Branch` VALUES (3,'Bedfordview Pri15641456165v BNKG Suite sc','Priority House 5 Iris Road Bedfordview Gauteng','2024-02-24 00:00:00'),(4,'Bultfontein Service Centre','President Swart Street Bultfontein','2024-02-24 00:00:00'),(70,'Westridge Park Service Centre','Shop 69 Westridge Park sc.','2024-02-24 00:00:00'),(101,'Jozi ','Centro City 11 Trump st.','2024-02-24 00:00:00'),(102,'Majadahonda','Sta. María de la Cabeza, esq. Dr. Calero 2822','2024-02-24 00:00:00'),(103,'Torrejón','Pl. Mayor, 10 (28850) Torrejón Ardoz','2024-02-24 00:00:00'),(1471,'ImatiaBank Innovation','Edificio Citexvi, Fonte das Abelleiras, s/n · Local 27, 36310 Vigo, Pontevedra','2024-02-24 00:00:00'),(3200,'Pepesfg','Plaza España','2024-02-24 00:00:00'),(123124,'test','RUA ITAQUARI 180 apt 1302','2024-02-24 00:00:00');
/*!40000 ALTER TABLE `Branch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Customer`
--

DROP TABLE IF EXISTS `Customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Customer` (
  `CUSTOMERID` int NOT NULL AUTO_INCREMENT,
  `NAME` varchar(75) DEFAULT NULL,
  `SURNAME` varchar(75) DEFAULT NULL,
  `EMAIL` varchar(100) DEFAULT NULL,
  `ADDRESS` varchar(200) DEFAULT NULL,
  `STARTDATE` datetime DEFAULT NULL,
  `OFFICEID` int DEFAULT '1',
  `PHOTO` mediumblob,
  PRIMARY KEY (`CUSTOMERID`),
  KEY `CustomerInBranchFK` (`OFFICEID`),
  CONSTRAINT `CustomerInBranchFK` FOREIGN KEY (`OFFICEID`) REFERENCES `Branch` (`OFFICEID`)
) ENGINE=InnoDB AUTO_INCREMENT=19536 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Customer`
--

LOCK TABLES `Customer` WRITE;
/*!40000 ALTER TABLE `Customer` DISABLE KEYS */;
INSERT INTO `Customer` VALUES (10602,'James','Alan','james.alan@alan.inc','13, Downing Street','2024-02-24 00:00:00',3,NULL),(10604,'Markus','Bugle','Mark.Bugle@ontimize.com','22 Holloway Road','2024-02-24 00:00:00',3,NULL),(10606,'Tomás Miguel','Baños Márquez','','Al. Huerto los Mortolitos, Totana ','2024-02-24 00:00:00',3,NULL),(10607,'Lidya Esther','Buendía Lorente','','C/ Carlos III, 63 - 7.a A, Cartagena','2024-02-24 00:00:00',3,NULL),(10808,'Billy','Buttercup','Billy.Buttercup@ontimize.com','2 The Piazza','2024-02-24 00:00:00',3,NULL),(10810,'Marie','C.Johnson','marie.johnson@gmail.com','57 Great Marlborough Street, London','2024-02-24 00:00:00',3,NULL),(10811,'Pablo','Fernández Blanco','pablo.fernandez@yahoo.es','C/Barcelona s/n','2024-02-24 00:00:00',3,NULL),(10815,'Bridget','Corbirock','Bridget.Corbirock@yahoo.com','43 Carnaby Street','2024-02-24 00:00:00',3,NULL),(10834,'John','Green','','3 Oxford Street','2024-02-24 00:00:00',3,NULL),(19271,'Aubrey','Engels','Aubrey.Engels@ontimize.com','Tidorestraat 58-128','2024-02-24 00:00:00',4,NULL),(19320,'Heidi','Fischer','Heidi.Fischer@Imatia.com','Glacischaussee 20','2024-02-24 00:00:00',3,NULL),(19336,'Marlene','De Jong','Marlene.DeJong@Imatia.com','12 Rue Marbeau','2024-02-24 00:00:00',3,NULL),(19337,'Louise','Bakker','Louise.Bakker@Imatia.com','Marsopstrasse 2','2024-02-24 00:00:00',3,NULL),(19343,'Jeanne','Galouzeau','Jeanne.Galouzeau@Imatia.com','70 Rue de Miromesnil','2024-02-24 00:00:00',3,NULL),(19352,'Elektra','Christopoulos','Elektra.Christopoulos@Ontimize.com','Paikou 4','2024-02-24 00:00:00',3,NULL),(19359,'Juan','Dominguez ','Juan.Dom@Ontimize.com','Calle de Iparraguirre, 42','2024-02-24 00:00:00',3,NULL),(19362,'Philippe','Brown','Brown@gmail.com','Rosebank Rd 15','2024-02-24 00:00:00',3,NULL),(19363,'Michael','Calaghan','Michael.Calaghan@gmail.com','154-168 Boswall Pkwy, Edinburgh, City of Edinburgh EH5 2','2024-02-24 00:00:00',3,NULL),(19364,'Suez','Ashworth','Sue.Ashworth@Ontimize.com','Nymphenburger Strasse 55','2024-02-24 00:00:00',3,NULL),(19365,'Wing','Andersen','Wing.Andersen@gmail.com','56 Gurranebraher Ave','2024-02-24 00:00:00',3,NULL),(19527,'David','Blanco Balado','ddddde@gmail.com','Cddddd 89','2024-02-24 00:00:00',3,NULL),(19530,'Ruli','Cristobal','Holahola@gmail.com','calle imaginaria 123','2024-02-24 00:00:00',3,NULL),(19532,'Jimmy','Butler','jimmybuckets@gmail.com',NULL,'2024-02-24 00:00:00',3,NULL),(19534,'Michael','Fassbender','fassbender@gmail.com','Massachussets','2024-02-24 00:00:00',3,NULL),(19535,'Patata','Asada',NULL,NULL,'2024-02-24 00:00:00',3,NULL);
/*!40000 ALTER TABLE `Customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Employees`
--

DROP TABLE IF EXISTS `Employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Employees` (
  `EMPLOYEEID` int NOT NULL AUTO_INCREMENT,
  `EMPLOYEETYPEID` int DEFAULT '1',
  `EMPLOYEESURNAME` varchar(15) NOT NULL,
  `EMPLOYEENAME` varchar(15) NOT NULL,
  `OFFICEID` int DEFAULT '1',
  `EMPLOYEEADDRESS` varchar(100) DEFAULT NULL,
  `EMPLOYEESTARTDATE` datetime DEFAULT CURRENT_TIMESTAMP,
  `EMPLOYEEPHOTOTO` mediumblob,
  `NAME` varchar(100) DEFAULT NULL,
  `EMPLOYEEPHONE` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`EMPLOYEEID`),
  KEY `fk_Employee_Branch` (`OFFICEID`),
  CONSTRAINT `EmployeeWorksInBranch` FOREIGN KEY (`OFFICEID`) REFERENCES `Branch` (`OFFICEID`)
) ENGINE=InnoDB AUTO_INCREMENT=6895 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Employees`
--

LOCK TABLES `Employees` WRITE;
/*!40000 ALTER TABLE `Employees` DISABLE KEYS */;
INSERT INTO `Employees` VALUES (6378,1,'Robinson','Mark',3,'12 Brompton Road Knightsbridge. London UK','2024-02-24 00:00:00',NULL,NULL,'0500 430994'),(6379,1,'Smith','Caroline',3,'12 Brixton Road, London. United Kingdom‎','2024-02-24 00:00:00',NULL,NULL,'0845 46 40'),(6539,1,'Periwinkle','Christopher',3,'25 Mortimer Street. London','2024-02-24 00:00:00',NULL,NULL,'(010444) 11899'),(6741,1,'Burdock','Claudy',3,'25 Regent Street. London','2024-02-24 00:00:00',NULL,NULL,'07624 175096'),(6840,1,'Doyle','Antony',3,NULL,'2024-02-24 00:00:00',NULL,NULL,'070 6145 6297'),(6841,1,'Novotny','Cameron',3,NULL,'2024-02-24 00:00:00',NULL,NULL,'055 5182 6835'),(6842,1,'Looper','Christopher',3,NULL,'2024-02-24 00:00:00',NULL,NULL,'07624 810266'),(6843,1,'Anderson','Cecile',3,'46th & 48th Street, 156 Avenue, San Andres Colony. London','2024-02-24 00:00:00',NULL,NULL,'055 9055 6294'),(6844,1,'Anderson','Cheryl',3,NULL,'2024-02-24 00:00:00',NULL,NULL,'0845 46 48'),(6845,1,'Legendre','Charlotte',3,NULL,'2024-02-24 00:00:00',NULL,NULL,'0898 547 2304'),(6846,1,'Singht','Curtis',3,NULL,'2024-02-24 00:00:00',NULL,NULL,'055 3676 5432'),(6890,1,'Lemacks','Craig',3,NULL,'2024-02-24 00:00:00',NULL,NULL,'0800 570661'),(6891,1,'Butt','James',3,'John B Jr','2024-02-24 00:00:00',NULL,NULL,'07624 817175'),(6892,1,'Darakjy','Josephine',3,'Jeffrey A Esq','2024-02-24 00:00:00',NULL,NULL,'0800 177 7086'),(6893,1,'Venere','Art',3,'James L Cpa','2024-02-24 00:00:00',NULL,NULL,'(016977) 4951'),(6894,1,'Paprocki','Lenna',3,'639 Main St','2024-02-24 00:00:00',NULL,NULL,'0898 148 8226');
/*!40000 ALTER TABLE `Employees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Transaction`
--

DROP TABLE IF EXISTS `Transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Transaction` (
  `TransactionID` int NOT NULL AUTO_INCREMENT,
  `AccountID` int DEFAULT NULL,
  `TransactionType` enum('Deposit','Withdrawal','Transfer') DEFAULT NULL,
  `TotalAmount` decimal(15,2) DEFAULT '0.00',
  `Deposit` decimal(15,2) DEFAULT '0.00',
  `Withdrawl` decimal(15,2) DEFAULT '0.00',
  `ItemImage` text,
  `TransactionDate` datetime DEFAULT NULL,
  PRIMARY KEY (`TransactionID`),
  KEY `AccountID` (`AccountID`),
  CONSTRAINT `Transaction_ibfk_1` FOREIGN KEY (`AccountID`) REFERENCES `Account` (`ACCOUNTID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Transaction`
--

LOCK TABLES `Transaction` WRITE;
/*!40000 ALTER TABLE `Transaction` DISABLE KEYS */;
INSERT INTO `Transaction` VALUES (1,6,'Deposit',1000.00,1000.00,0.00,NULL,'2024-02-24 00:00:00'),(2,7,'Deposit',100.00,100.00,0.00,NULL,'2024-02-24 00:00:00'),(4,7,'Withdrawal',-1.00,0.00,1.00,NULL,'2024-02-24 00:00:00'),(5,6,'Deposit',1.00,1.00,0.00,NULL,'2024-02-24 00:00:00');
/*!40000 ALTER TABLE `Transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Transfer`
--

DROP TABLE IF EXISTS `Transfer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Transfer` (
  `TransactionID` int NOT NULL AUTO_INCREMENT,
  `FromAccountID` int DEFAULT NULL,
  `ToAccountID` int DEFAULT NULL,
  `Amount` decimal(15,2) DEFAULT '0.00',
  `TransactionDate` datetime DEFAULT NULL,
  PRIMARY KEY (`TransactionID`),
  KEY `FromAccountID` (`FromAccountID`),
  KEY `ToAccountID` (`ToAccountID`),
  CONSTRAINT `FromAccount` FOREIGN KEY (`FromAccountID`) REFERENCES `Account` (`ACCOUNTID`),
  CONSTRAINT `ToAccount` FOREIGN KEY (`ToAccountID`) REFERENCES `Account` (`ACCOUNTID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Transfer`
--

LOCK TABLES `Transfer` WRITE;
/*!40000 ALTER TABLE `Transfer` DISABLE KEYS */;
INSERT INTO `Transfer` VALUES (1,7,6,1.00,'2024-02-24 00:00:00');
/*!40000 ALTER TABLE `Transfer` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-02-17 21:22:50
