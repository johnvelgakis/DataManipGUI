-- MySQL dump 10.13  Distrib 5.7.24, for osx11.1 (x86_64)
--
-- Host: localhost    Database: hotel_booking
-- ------------------------------------------------------
-- Server version	8.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `basic_statistics`
--

DROP TABLE IF EXISTS `basic_statistics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_statistics` (
  `hotel` text,
  `average_nights` double DEFAULT NULL,
  `cancellation_rate` double DEFAULT NULL,
  `first_arrival` datetime DEFAULT NULL,
  `last_arrival` datetime DEFAULT NULL,
  `total_cancellations` bigint DEFAULT NULL,
  `total_bookings` bigint DEFAULT NULL,
  `cancellation_percentage` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `booking_distribution`
--

DROP TABLE IF EXISTS `booking_distribution`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `booking_distribution` (
  `hotel` text,
  `max_month` text,
  `min_month` text,
  `max_season` text,
  `min_season` text,
  `max_room_type` text,
  `min_room_type` text,
  `max_client_type` text,
  `min_client_type` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bookings`
--

DROP TABLE IF EXISTS `bookings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bookings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `hotel` varchar(255) DEFAULT NULL,
  `is_canceled` int DEFAULT NULL,
  `lead_time` int DEFAULT NULL,
  `arrival_date_year` int DEFAULT NULL,
  `arrival_date_month` varchar(255) DEFAULT NULL,
  `arrival_date_week_number` int DEFAULT NULL,
  `arrival_date_day_of_month` int DEFAULT NULL,
  `stays_in_weekend_nights` int DEFAULT NULL,
  `stays_in_week_nights` int DEFAULT NULL,
  `adults` int DEFAULT NULL,
  `children` float DEFAULT NULL,
  `babies` int DEFAULT NULL,
  `meal` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `market_segment` varchar(255) DEFAULT NULL,
  `distribution_channel` varchar(255) DEFAULT NULL,
  `is_repeated_guest` int DEFAULT NULL,
  `previous_cancellations` int DEFAULT NULL,
  `previous_bookings_not_canceled` int DEFAULT NULL,
  `reserved_room_type` varchar(255) DEFAULT NULL,
  `assigned_room_type` varchar(255) DEFAULT NULL,
  `booking_changes` int DEFAULT NULL,
  `deposit_type` varchar(255) DEFAULT NULL,
  `agent` float DEFAULT NULL,
  `company` float DEFAULT NULL,
  `days_in_waiting_list` int DEFAULT NULL,
  `customer_type` varchar(255) DEFAULT NULL,
  `adr` float DEFAULT NULL,
  `required_car_parking_spaces` int DEFAULT NULL,
  `total_of_special_requests` int DEFAULT NULL,
  `reservation_status` varchar(255) DEFAULT NULL,
  `reservation_status_date` date DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone_number` varchar(255) DEFAULT NULL,
  `credit_card` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=119391 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-13 16:55:50
