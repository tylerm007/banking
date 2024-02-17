CREATE DATABASE `banking` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

-- banking.AccountType definition

CREATE TABLE `AccountType` (
  `Name` varchar(25) NOT NULL,
  PRIMARY KEY (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- banking.Branch definition

CREATE TABLE `Branch` (
  `BranchID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) DEFAULT NULL,
  `Office` varchar(15) DEFAULT NULL,
  `Address` varchar(100) DEFAULT NULL,
  `OpenDate` datetime DEFAULT NULL,
  PRIMARY KEY (`BranchID`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- banking.Customer definition

CREATE TABLE `Customer` (
  `CustomerID` int NOT NULL,
  `FirstName` varchar(50) DEFAULT NULL,
  `LastName` varchar(50) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `PhoneNumber` varchar(20) DEFAULT NULL,
  `Address` varchar(200) DEFAULT NULL,
  `BirthDate` date DEFAULT NULL,
  `RegistrationDate` datetime DEFAULT NULL,
  `UserName` varchar(64) NOT NULL,
  `Password` varchar(64) NOT NULL,
  `BranchID` int DEFAULT NULL,
  PRIMARY KEY (`CustomerID`),
  KEY `fk_Customer_Branch` (`BranchID`),
  CONSTRAINT `fk_Customer_Branch` FOREIGN KEY (`BranchID`) REFERENCES `Branch` (`BranchID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- banking.Employees definition

CREATE TABLE `Employees` (
  `EmployeeID` int NOT NULL AUTO_INCREMENT,
  `LastName` varchar(15) NOT NULL,
  `FirstName` varchar(15) NOT NULL,
  `Branch` int DEFAULT '1',
  `BirthDate` datetime DEFAULT NULL,
  `Photo` varchar(25) DEFAULT NULL,
  `Notes` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`EmployeeID`),
  KEY `fk_Employee_Branch` (`Branch`),
  CONSTRAINT `fk_Employee_Branch` FOREIGN KEY (`Branch`) REFERENCES `Branch` (`BranchID`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- banking.Account definition

CREATE TABLE `Account` (
  `AccountID` int NOT NULL,
  `CustomerID` int DEFAULT NULL,
  `AccountType` enum('Savings','Checking','Loan') DEFAULT NULL,
  `AcctBalance` decimal(15,2) DEFAULT NULL,
  `OpenDate` datetime DEFAULT NULL,
  PRIMARY KEY (`AccountID`),
  KEY `CustomerID` (`CustomerID`),
  CONSTRAINT `Account_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `Customer` (`CustomerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- banking.`Transaction` definition

CREATE TABLE `Transaction` (
  `TransactionID` int NOT NULL,
  `AccountID` int DEFAULT NULL,
  `TransactionType` enum('Deposit','Withdrawal','Transfer') DEFAULT NULL,
  `TotalAmount` decimal(15,2) DEFAULT NULL,
  `Deposit` decimal(15,2) DEFAULT NULL,
  `Withdrawl` decimal(15,2) DEFAULT NULL,
  `ItemImage` text,
  `TransactionDate` datetime DEFAULT NULL,
  PRIMARY KEY (`TransactionID`),
  KEY `AccountID` (`AccountID`),
  CONSTRAINT `Transaction_ibfk_1` FOREIGN KEY (`AccountID`) REFERENCES `Account` (`AccountID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- banking.Transfer definition

CREATE TABLE `Transfer` (
  `TransactionID` int NOT NULL,
  `FromAccountID` int DEFAULT NULL,
  `ToAccountID` int DEFAULT NULL,
  `Amount` decimal(15,2) DEFAULT NULL,
  `TransactionDate` datetime DEFAULT NULL,
  PRIMARY KEY (`TransactionID`),
  KEY `FromAccountID` (`FromAccountID`),
  KEY `ToAccountID` (`ToAccountID`),
  CONSTRAINT `Transfer_ibfk_1` FOREIGN KEY (`FromAccountID`) REFERENCES `Account` (`AccountID`),
  CONSTRAINT `Transfer_ibfk_2` FOREIGN KEY (`ToAccountID`) REFERENCES `Account` (`AccountID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;