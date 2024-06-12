/*
SQLyog Ultimate v12.4.1 (64 bit)
MySQL - 10.4.24-MariaDB : Database - furniture_db
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`furniture_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `furniture_db`;

/*Table structure for table `access_right` */

DROP TABLE IF EXISTS `access_right`;

CREATE TABLE `access_right` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `access_code` varchar(30) NOT NULL,
  `access_name` varchar(300) NOT NULL,
  `access_desc` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `access_code` (`access_code`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

/*Data for the table `access_right` */

insert  into `access_right`(`id`,`access_code`,`access_name`,`access_desc`) values 
(1,'ALL_CREATOR','User can access all records made by other users.','User can access all records made by other users although the logged user is not an admin.'),
(2,'ONLY_CREATOR','User can access only the records made by logged user.','User can access the records made by logged user although logged user is an admin.');

/*Table structure for table `alembic_version` */

DROP TABLE IF EXISTS `alembic_version`;

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `alembic_version` */

insert  into `alembic_version`(`version_num`) values 
('d0a2f53cb61e');

/*Table structure for table `material_list` */

DROP TABLE IF EXISTS `material_list`;

CREATE TABLE `material_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `barcode` varchar(30) NOT NULL,
  `name` varchar(300) NOT NULL,
  `qty` float DEFAULT NULL,
  `uom` varchar(200) NOT NULL,
  `consumable` tinyint(1) DEFAULT NULL,
  `storage_location` varchar(200) NOT NULL,
  `image` varchar(300) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `date_modified` datetime DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `modified_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `barcode` (`barcode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `material_list` */

/*Table structure for table `product_list` */

DROP TABLE IF EXISTS `product_list`;

CREATE TABLE `product_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model_no` varchar(30) NOT NULL,
  `name` varchar(300) NOT NULL,
  `qty` float DEFAULT NULL,
  `qty_uom` varchar(200) NOT NULL,
  `weight` float DEFAULT NULL,
  `weight_uom` varchar(200) NOT NULL,
  `currency` varchar(30) NOT NULL,
  `price` int(11) NOT NULL,
  `storage_location` varchar(200) NOT NULL,
  `image` varchar(300) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `date_modified` datetime DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `modified_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `model_no` (`model_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `product_list` */

/*Table structure for table `product_material` */

DROP TABLE IF EXISTS `product_material`;

CREATE TABLE `product_material` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) DEFAULT NULL,
  `material_id` int(11) DEFAULT NULL,
  `used_material_qty` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  KEY `material_id` (`material_id`),
  CONSTRAINT `product_material_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product_list` (`id`),
  CONSTRAINT `product_material_ibfk_2` FOREIGN KEY (`material_id`) REFERENCES `material_list` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `product_material` */

/*Table structure for table `storage_location` */

DROP TABLE IF EXISTS `storage_location`;

CREATE TABLE `storage_location` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `storage_location_code` varchar(30) NOT NULL,
  `storage_location_name` varchar(300) NOT NULL,
  `date_created` datetime DEFAULT NULL,
  `date_modified` datetime DEFAULT NULL,
  `usable` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `storage_location_code` (`storage_location_code`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4;

/*Data for the table `storage_location` */

insert  into `storage_location`(`id`,`storage_location_code`,`storage_location_name`,`date_created`,`date_modified`,`usable`) values 
(1,'PR-BED','Product-Bed','2024-06-12 19:21:37','2024-06-12 19:21:37',1),
(2,'PR-CAB','Product-Cabinet','2024-06-12 19:44:18','2024-06-12 19:44:18',1),
(7,'PR-CHAIR','Product-Chair','2024-06-12 21:09:31','2024-06-12 21:11:04',0),
(8,'PR-MAT','Product-Mat','2024-06-12 21:10:44','2024-06-12 21:11:17',1),
(9,'PR-DESK','Product-Desk','2024-06-12 21:11:54','2024-06-12 21:11:54',0);

/*Table structure for table `users` */

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `birth_date` date NOT NULL,
  `phone_num` int(11) NOT NULL,
  `address` varchar(300) NOT NULL,
  `username` varchar(128) NOT NULL,
  `password` varchar(128) NOT NULL,
  `image` varchar(300) DEFAULT NULL,
  `admin` tinyint(1) DEFAULT NULL,
  `access_right` varchar(30) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `date_modified` datetime DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `modified_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

/*Data for the table `users` */

insert  into `users`(`id`,`name`,`birth_date`,`phone_num`,`address`,`username`,`password`,`image`,`admin`,`access_right`,`date_created`,`date_modified`,`created_by`,`modified_by`) values 
(1,'Admin1','2024-06-01',12345,'Surya Sumantri Street','admin1','admin1','N/A',1,'ONLY_CREATOR','2024-06-12 16:30:15','2024-06-12 21:05:50',0,1),
(2,'Basic User 1','1999-01-01',123456,'Surya sumantri','basic1','basic1','N/A',0,'ONLY_CREATOR','2024-06-12 16:58:43','2024-06-12 21:08:15',1,1),
(3,'admin2','2003-02-02',12345,'Address','Admin2','Admin2','N/A',0,'ALL_CREATOR','2024-06-12 19:42:36','2024-06-12 21:00:12',1,1),
(4,'Basic2','1999-01-01',12345,'Address','basic2','basic2','N/A',0,'ALL_CREATOR','2024-06-12 19:43:14','2024-06-12 19:43:14',1,1);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
