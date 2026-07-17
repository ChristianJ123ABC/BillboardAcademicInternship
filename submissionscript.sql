-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: junction.proxy.rlwy.net    Database: railway
-- ------------------------------------------------------
-- Server version	9.4.0

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
-- Table structure for table `advertisements`
--

DROP TABLE IF EXISTS `advertisements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `advertisements` (
  `advert_id` int NOT NULL AUTO_INCREMENT,
  `file` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `caption` text COLLATE utf8mb4_unicode_ci,
  `user_id` int DEFAULT NULL,
  `views` int DEFAULT NULL,
  PRIMARY KEY (`advert_id`),
  KEY `fk_user` (`user_id`),
  CONSTRAINT `fk_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10068 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `advertisements`
--

LOCK TABLES `advertisements` WRITE;
/*!40000 ALTER TABLE `advertisements` DISABLE KEYS */;
INSERT INTO `advertisements` VALUES (4,'uploads\\HHKwsK-XAAAViHM.png','gmail perc',5,54),(27,'uploads/Background.jpg','',3,12),(28,'uploads/airport.jpg','',3,15),(29,'uploads/city_center.jpg','',3,34),(30,'uploads/shopping_center.jpg','',3,67),(31,'uploads/train_station.jpg','',3,82),(33,'uploads\\SPOILER_POSTER_Map_V2.png','maptest',5,38),(34,'uploads\\image.png','Smoking Advert Test',5,41),(9999,'tests/resources/gp.mp4','hi',1,33),(10048,'C:\\Users\\flips\\Documents\\GitHub\\BillboardAcademicInternship\\tests\\resources\\city_center.jpg',NULL,4,33),(10049,'myfilenow','dontdelete',5,333),(10067,'uploads/....jpg','',1,33);
/*!40000 ALTER TABLE `advertisements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schedules`
--

DROP TABLE IF EXISTS `schedules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schedules` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `advert_id` int NOT NULL,
  `location` text NOT NULL,
  `time` text NOT NULL,
  `date_start` date NOT NULL,
  `date_end` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedules`
--

LOCK TABLES `schedules` WRITE;
/*!40000 ALTER TABLE `schedules` DISABLE KEYS */;
INSERT INTO `schedules` VALUES (17,4,'Dublin City Center','08:00 AM - 10:00 AM','2028-05-02','2029-03-03'),(18,33,'O\'Connell Street','08:00 AM - 10:00 AM','2040-02-05','2041-05-02'),(19,34,'Swords Pavilions Shopping Centre','12:00 PM - 02:00 PM','2026-07-10','2026-08-17');
/*!40000 ALTER TABLE `schedules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) DEFAULT NULL,
  `hashed_password` varchar(255) DEFAULT NULL,
  `firstName` varchar(255) DEFAULT NULL,
  `lastName` varchar(255) DEFAULT NULL,
  `businessName` varchar(255) DEFAULT NULL,
  `2fa_enabled` tinyint(1) DEFAULT NULL,
  `2fa_secret` varchar(255) DEFAULT NULL,
  `subscription_plan` varchar(255) DEFAULT 'basic',
  `uploads_used` int DEFAULT '0',
  `subscription_start` datetime DEFAULT NULL,
  `subscription_expiry` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `userID` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'fake123@gmail.com','scrypt:32768:8:1$YX0xJnkULeCaHd3N$23fd16a292b50ff1cb3fb3fd0a62a193c128d3db65afc5ee9e0d86908c93e049c3a6c330f7ba43458d1b3ddfeaf83f032597f402b9e6e14eb549d0337354a84a','Chris','Joe','Christian\'s Business',0,'gAAAAABqWnSr0xsZsQSi-81at7KJxJx81P2vYK3cHrwtRHsM4vvEnMwnizmsL03HTyxc6O-L98zUGXFSeTRqOYST88hzHEIX-_CDCVNVngArxuCAcUyHPBsIeneJWAJXVVPUufsOpjP2','Premium',0,NULL,'2026-08-16 19:09:17'),(2,'fakebusiness@gmail.com','scrypt:32768:8:1$KomCRJIpEBb6hmGI$1d86948086925f6153c691bd07a8d3d746360508e79a58ad556466e93e46347a8d8c82b45845d99b05d90d185e343ea364328f2306415372181f4547a60e8977','Fake','Business','FakeBusiness456',0,NULL,'Basic',0,NULL,NULL),(3,'1234@gmail.com','scrypt:32768:8:1$OlCa0gvkyv6fkC2z$42b73ed47ef11310f0b3d33fd36343dba05c37429b9b77c0eebd8fd59f329c06bd804c75c25b85df5eacf1ab4272e446a485797a469cc7bf10824f73dfc7c522','NCI','college','PrakashBusiness',0,'gAAAAABqRSCeWUrh7LRLKrq9p-EO-am4rQZlSWqvQvxjnkZqaptx4vVTO-GiVmOGVNbMVEE8anQI24KHSEr9-6-Xzx06IlrbbFNR3RpK3sWOZ0AbW7S3s5iNimb9m83jxswJg-bhTnXq','Premium',0,'2026-06-25 12:35:14','2026-07-30 22:17:27'),(4,'2345@gmail.com','scrypt:32768:8:1$uZULxhu9Mn8xV5YI$0b786317690cb7f8d09839f2be46278c7dc0dc9ccd1f5e7d0381f758af596315cb2af39b6ec491f5749ffd8d12c55cc86228fdc030c93f7bd7f53d77b0a4b43e','Nci','College','PrakashBusiness',0,NULL,'Basic',0,NULL,NULL),(5,'3456@gmail.com','scrypt:32768:8:1$7eWqirCbDxY8Q0NJ$e8f30a317d792c6524fddd86bc7a315c0d5fc26066cff86c8d469e1193cde07bea0c2601c12e28180b3afb337428eab770d1dd954b16d61fd14341019da6d46c','3456','3456','3456',0,NULL,'Standard',0,NULL,NULL),(14,'2FAenabled@gmail.com','scrypt:32768:8:1$laVfcofOnIGouDHV$67d13e3dcf5b3fcb934b12b3022caf3467ccc8ff607779a0a403c07a8da100bd30a256f6f5174922757743cd477029033d5feda1a35ea8971593927f243cb72a','2FA','Enabled','2FAEnterprises',1,'gAAAAABqVRvNAC_8ZbFC_GouvHK0pngoSFOAs2GGn2cxGfCz4E2CWxvUK4Gqx9UjljiqQYQ0h1ij5o-MMW5DTZNoiC9Ic9m2kQBg3SnWGofISKNmUWU-KwGiS8yYcRfVyef9dTn-s5L_','Basic',0,NULL,NULL),(18,'noplan@gmail.com','scrypt:32768:8:1$kJwMoepb3Z13y2By$1d96c7ee81fdb5720bd89453fcb72f1813a31aa2910857eafa9f02d8ec47c91951e70a79020a9fd061c7c53c7d58ce412c26e9b720f220f78d8fb63cd8e822bd','No','Business','NoBusiness',0,NULL,'New',0,NULL,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-17 20:17:11
