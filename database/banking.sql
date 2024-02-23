-- MySQL dump 10.13  Distrib 8.0.23, for Linux (x86_64)
--
-- Host: localhost    Database: banking
-- ------------------------------------------------------
-- Server version	8.0.23

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
-- Table structure for table `Account`
--

DROP TABLE IF EXISTS `Account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Account` (
  `ACCOUNTID` int NOT NULL AUTO_INCREMENT,
  `CUSTOMERID` int DEFAULT NULL,
  `ACCOUNTTYPEID` int DEFAULT NULL,
  `ACCOUNTTYPENAME` VARCHAR(25),
  `BALANCE` decimal(15,2) DEFAULT 0,
  `STARTDATE` datetime DEFAULT NULL,
  `ENDDATE` datetime DEFAULT NULL,
  `ENTITYID` int DEFAULT 1,
  `OFFICEID` int DEFAULT 1,
  `CDID` VARCHAR(25),
  `ANID` VARCHAR(25),
  `INTERESRATE` decimal(15,2) DEFAULT 0,
  PRIMARY KEY (`ACCOUNTID`),
  KEY `CUSTOMERID` (`CUSTOMERID`),
  KEY `Account_fk2` (`AccountType`),
  CONSTRAINT `AccountTypeFK` FOREIGN KEY (`ACCOUNTTYPEID`) REFERENCES `AccountType` (`AcctID`),
  CONSTRAINT `CustomerHasAccountFK` FOREIGN KEY (`CUSTOMERID`) REFERENCES `Customer` (`CUSTOMERID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Account`
--

LOCK TABLES `Account` WRITE;
/*!40000 ALTER TABLE `Account` DISABLE KEYS */;
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
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AccountType`
--

LOCK TABLES `AccountType` WRITE;
/*!40000 ALTER TABLE `AccountType` DISABLE KEYS */;
-- INSERT INTO `AccountType` ('AcctID','Name') VALUES (1,'Checking'),(2, 'Loan'),(3,'Savings');
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
  PRIMARY KEY (`BRANCHID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Branch`
--

LOCK TABLES `Branch` WRITE;
/*!40000 ALTER TABLE `Branch` DISABLE KEYS */;
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
  `STARTDATE` date DEFAULT CURRENT_DATE,
  `BRANCHID` int DEFAULT 1,
  PRIMARY KEY (`CUSTOMERID`),
  KEY `fk_Customer_Branch` (`BRANCHID`),
  CONSTRAINT `CustomerInBranchFK` FOREIGN KEY (`BRANCHID`) REFERENCES `Branch` (`BRANCHID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Customer`
--

LOCK TABLES `Customer` WRITE;
/*!40000 ALTER TABLE `Customer` DISABLE KEYS */;
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
  `EMPLOYEETYPEID` int DEFAULT 1,
  `EMPLOYEESURNAME` varchar(15) NOT NULL,
  `EMPLOYEENAME` varchar(15) NOT NULL,
  `OFFICEID` int DEFAULT '1',
  `EMPLOYEEADDRESS` VARCHAR(100) DEFAULT NULL,
  `EMPLOYEESTARTDATE` datetime DEFAULT CURRENT_DATE,
  `EMPLOYEEPHOTOTO` BLOB DEFAULT NULL,
  `NAME` varchar(100) DEFAULT NULL,
  `EMPLOYEEPHONE` VARCHAR(50) DEFAULT NULL,
  PRIMARY KEY (`EMPLOYEEID`),
  KEY `fk_Employee_Branch` (`Branch`),
  CONSTRAINT `EmployeeWorksInBranch` FOREIGN KEY (`OFFICEID`) REFERENCES `Branch` (`BRANCHID`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Employees`
--

LOCK TABLES `Employees` WRITE;
/*!40000 ALTER TABLE `Employees` DISABLE KEYS */;
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
  `TotalAmount` decimal(15,2) DEFAULT 0,
  `Deposit` decimal(15,2) DEFAULT 0,
  `Withdrawl` decimal(15,2) DEFAULT 0,
  `ItemImage` text,
  `TransactionDate` datetime DEFAULT NULL,
  PRIMARY KEY (`TransactionID`),
  KEY `AccountID` (`AccountID`),
  CONSTRAINT `Transaction_ibfk_1` FOREIGN KEY (`AccountID`) REFERENCES `Account` (`AccountID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Transaction`
--

LOCK TABLES `Transaction` WRITE;
/*!40000 ALTER TABLE `Transaction` DISABLE KEYS */;
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
  `Amount` decimal(15,2) DEFAULT 0,
  `TransactionDate` datetime DEFAULT NULL,
  PRIMARY KEY (`TransactionID`),
  KEY `FromAccountID` (`FromAccountID`),
  KEY `ToAccountID` (`ToAccountID`),
  CONSTRAINT `FromAccount` FOREIGN KEY (`FromAccountID`) REFERENCES `Account` (`AccountID`),
  CONSTRAINT `ToAccount` FOREIGN KEY (`ToAccountID`) REFERENCES `Account` (`AccountID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Transfer`
--

LOCK TABLES `Transfer` WRITE;
/*!40000 ALTER TABLE `Transfer` DISABLE KEYS */;
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
