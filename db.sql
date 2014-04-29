-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.1.30-community - MySQL Community Server (GPL)
-- Server OS:                    Win32
-- HeidiSQL Version:             8.2.0.4675
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping database structure for spiderbot
DROP DATABASE IF EXISTS `spiderbot`;
CREATE DATABASE IF NOT EXISTS `spiderbot` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `spiderbot`;


-- Dumping structure for table spiderbot.cat_last_state
DROP TABLE IF EXISTS `cat_last_state`;
CREATE TABLE IF NOT EXISTS `cat_last_state` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login_cred_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.


-- Dumping structure for table spiderbot.current_state
DROP TABLE IF EXISTS `current_state`;
CREATE TABLE IF NOT EXISTS `current_state` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cat_id` int(11) DEFAULT NULL,
  `page_index` int(11) DEFAULT NULL,
  `total_page` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `login_cred_id` int(11) DEFAULT NULL,
  `link1` varchar(500) DEFAULT NULL,
  `link2` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.


-- Dumping structure for table spiderbot.info_details
DROP TABLE IF EXISTS `info_details`;
CREATE TABLE IF NOT EXISTS `info_details` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login_cred_id` int(11) DEFAULT NULL,
  `tb_category_id` int(11) DEFAULT NULL,
  `business_name` varchar(255) DEFAULT NULL,
  `rating` varchar(50) DEFAULT NULL,
  `number_of_reviews` varchar(50) DEFAULT NULL,
  `coupon` varchar(50) DEFAULT NULL,
  `buy_itnow` varchar(50) DEFAULT NULL,
  `address1` varchar(255) DEFAULT NULL,
  `address2` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `zip` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `website` varchar(255) DEFAULT NULL,
  `page_count` int(11) DEFAULT NULL,
  `link` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.


-- Dumping structure for table spiderbot.login_cred
DROP TABLE IF EXISTS `login_cred`;
CREATE TABLE IF NOT EXISTS `login_cred` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `blocked` int(11) unsigned zerofill DEFAULT '00000000000',
  `done` int(11) unsigned zerofill DEFAULT '00000000000',
  `category_crawled` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.


-- Dumping structure for table spiderbot.tbl_category
DROP TABLE IF EXISTS `tbl_category`;
CREATE TABLE IF NOT EXISTS `tbl_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login_cred_id` int(11) DEFAULT NULL,
  `zip_code` varchar(50) DEFAULT NULL,
  `cat_name` varchar(512) DEFAULT NULL,
  `cat_link` varchar(512) DEFAULT NULL,
  `visited` int(11) unsigned zerofill DEFAULT '00000000000',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
