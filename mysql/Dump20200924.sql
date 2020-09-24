-- MySQL dump 10.13  Distrib 8.0.20, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: websmosim
-- ------------------------------------------------------
-- Server version	8.0.20

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `smo_fieldequip`
--

DROP TABLE IF EXISTS `smo_fieldequip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `smo_fieldequip` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `eq_name` varchar(30) NOT NULL,
  `eq_desc` varchar(100) DEFAULT NULL,
  `eq_signal` varchar(10) DEFAULT NULL,
  `eq_type` varchar(30) DEFAULT NULL,
  `eq_val` varchar(30) DEFAULT NULL,
  `eq_val_date` datetime NOT NULL,
  `eq_param` varchar(30) DEFAULT NULL,
  `eq_room` varchar(50) DEFAULT NULL,
  `eq_indoor` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smo_fieldequip`
--

LOCK TABLES `smo_fieldequip` WRITE;
/*!40000 ALTER TABLE `smo_fieldequip` DISABLE KEYS */;
INSERT INTO `smo_fieldequip` VALUES (7,'PIR_01','Movement Transmitter','input','PIR','0','2020-09-21 04:00:00','-','-',0),(8,'TT_01','Temperature Transmitter (analog) #1 ','input','TT','23.85','2020-09-21 04:00:00','celcius','-',0),(9,'TT_02','Temperature Transmitter (i2c) #2 [isolated]','input','TT','24.25','2020-09-21 04:00:01','celcius','-',0),(10,'TT_03','Temperature Transmitter (i2c) #3 [wired]','input','TT','24.75','2020-09-21 04:03:24','celcius','-',0),(11,'TT_04','Temperature Transmitter (i2c) #4','input','TT','23.06','2020-09-21 04:00:03','celcius','-',0),(12,'TT_05','Temperature Transmitter (spi) #5 (TPT, bmp180)','input','TPT','23.06','2020-09-21 04:00:04','celcius','-',0),(13,'POT_01','Potentiometer #1','input','potentiometer','54.3','2020-09-21 04:00:04','percentage','-',0),(14,'POT_02','Potentiometer #2','input','potentiometer','24.5','2020-09-21 04:00:04','percentage','-',0),(15,'LS_01','Light Sensor','input','light sensor','14.14','2020-09-21 04:03:24','percentage','-',0),(16,'DS_01','Door Switch #1','input','door switch','0','2020-09-21 04:00:04','-','-',0),(17,'DS_02','Door Switch #2','input','door switch','0','2020-09-21 04:00:04','-','-',0),(19,'SW_01','On/Off Switch with lamp','input','switch','0','2020-09-21 04:00:04','-','-',0),(20,'PT_01',' Pressure Transmitter (spi) (TPT, bmp180)','input','TPT','1011.05','2020-09-21 04:00:06','pascals','-',0),(21,'FAN_01','Main Fan','output','fan','OFF','2020-09-21 04:03:24','-','-',0),(22,'FAN_02','Small Fan','output','fan','OFF','2020-09-21 04:00:06','-','-',0),(23,'BIP_01','Signalisation buzzer','output','buzzer','OFF','2020-09-21 04:00:06','-','-',0),(24,'BIP_02','Alarm buzzer','output','buzzer','OFF','2020-09-21 04:00:06','-','-',0),(25,'LED_Y','Yellow LED','output','led','YELLOW','2020-09-21 04:03:24','-','-',0),(26,'LED_RG','Red and Green LED','output','led','OFF','2020-09-21 04:00:06','-','-',0),(27,'LED_RGB','Red, Green and Blue LED','output','led','OFF','2020-09-21 04:00:06','-','-',0),(29,'DC_MOT','DC Motor','output','motor','OFF','2020-09-21 04:00:06','-','-',0),(31,'HF_01','Heating Floor','output','heater','OFF','2020-09-21 04:00:06','-','-',0);
/*!40000 ALTER TABLE `smo_fieldequip` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smo_measurement`
--

DROP TABLE IF EXISTS `smo_measurement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `smo_measurement` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `instrument_name` varchar(30) NOT NULL,
  `measurement_value` varchar(100) DEFAULT NULL,
  `measurement_date` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14651 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smo_measurement`
--

LOCK TABLES `smo_measurement` WRITE;
/*!40000 ALTER TABLE `smo_measurement` DISABLE KEYS */;
INSERT INTO `smo_measurement` VALUES (1,'PIR_01','0','2020-09-09 15:21:52'),(2,'TT_01','24.81','2020-09-09 15:21:52'),(3,'TT_02','33.0','2020-09-09 15:21:53'),(4,'TT_03','29.19','2020-09-09 15:21:54'),(5,'TT_04','25.0','2020-09-09 15:21:55'),(6,'TT_05','25.48','2020-09-09 15:21:56'),(7,'POT_01','60.6','2020-09-09 15:21:56'),(8,'POT_02','18.6','2020-09-09 15:21:56'),(9,'LS_01','77.43','2020-09-09 15:21:56'),(10,'DS_01','1','2020-09-09 15:21:56');
/*!40000 ALTER TABLE `smo_measurement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smo_rules`
--

DROP TABLE IF EXISTS `smo_rules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `smo_rules` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `instrument_name` varchar(40) NOT NULL,
  `upper_limit` varchar(20) DEFAULT NULL,
  `lower_limit` varchar(20) DEFAULT NULL,
  `regulator_name` varchar(20) DEFAULT NULL,
  `upper_rule` varchar(20) DEFAULT NULL,
  `lower_rule` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smo_rules`
--

LOCK TABLES `smo_rules` WRITE;
/*!40000 ALTER TABLE `smo_rules` DISABLE KEYS */;
INSERT INTO `smo_rules` VALUES (1,'LS_01','50','30','LED_Y','0','1'),(2,'TT_03','28','26','FAN_01','1','0');
/*!40000 ALTER TABLE `smo_rules` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-09-24  6:54:24
