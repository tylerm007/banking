-- MySQL dump 10.13  Distrib 8.0.33, for Linux (aarch64)
--
-- Host: localhost    Database: authdb
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
-- Current Database: `authdb`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `authdb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `authdb`;

--
-- Table structure for table `Role`
--

DROP TABLE IF EXISTS `Role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Role` (
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Role`
--

LOCK TABLES `Role` WRITE;
/*!40000 ALTER TABLE `Role` DISABLE KEYS */;
INSERT INTO `Role` VALUES ('CS_ADMIN'),('fullaccess'),('tenant');
/*!40000 ALTER TABLE `Role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `UserRole`
--

DROP TABLE IF EXISTS `UserRole`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `UserRole` (
  `user_id` varchar(64) NOT NULL,
  `notes` text,
  `role_name` varchar(32) NOT NULL,
  PRIMARY KEY (`user_id`,`role_name`),
  KEY `in_role` (`role_name`),
  CONSTRAINT `in_client` FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `in_role` FOREIGN KEY (`role_name`) REFERENCES `Role` (`name`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UserRole`
--

LOCK TABLES `UserRole` WRITE;
/*!40000 ALTER TABLE `UserRole` DISABLE KEYS */;
INSERT INTO `UserRole` VALUES ('admin',NULL,'CS_ADMIN'),('admin',NULL,'fullaccess'),('demo','','CS_ADMIN'),('sam','','fullaccess'),('ty',NULL,'CS_ADMIN'),('ty',NULL,'fullaccess');
/*!40000 ALTER TABLE `UserRole` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `name` varchar(128) DEFAULT NULL,
  `notes` text,
  `id` varchar(64) NOT NULL,
  `username` varchar(128) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  `password_hash` varchar(200) DEFAULT NULL,
  `client_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES ('Administrator',NULL,'admin','Admin User','admin@corp.com','password',1003),('','demo','demo','demo@gmail.com','demouser','demouser',0),('sam','','sam','Sam','sbachman@uncommonfarms.com','password',1038),('ty',NULL,'ty','tyler',NULL,'$2b$12$g6Q17yPJUUEaYuD22/joS.MtP4OXEe3OP831Yu1CBOG5qfbLx5Cj2',1038);
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;