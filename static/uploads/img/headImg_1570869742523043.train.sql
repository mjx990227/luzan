# Host: localhost  (Version: 5.5.53)
# Date: 2019-06-26 10:04:42
# Generator: MySQL-Front 5.3  (Build 4.234)

/*!40101 SET NAMES utf8 */;

#
# Structure for table "book"
#

DROP TABLE IF EXISTS `book`;
CREATE TABLE `book` (
  `订单票号` varchar(15) NOT NULL DEFAULT '',
  `订票时间` date NOT NULL DEFAULT '0000-00-00',
  `订票数量` int(11) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`订单票号`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='订票单';

#
# Data for table "book"
#

/*!40000 ALTER TABLE `book` DISABLE KEYS */;
/*!40000 ALTER TABLE `book` ENABLE KEYS */;

#
# Structure for table "client"
#

DROP TABLE IF EXISTS `client`;
CREATE TABLE `client` (
  `客户编号` char(18) NOT NULL DEFAULT '' COMMENT '客户编号',
  `客户姓名` varchar(15) NOT NULL DEFAULT '',
  `证件类型` varchar(15) NOT NULL DEFAULT '',
  `客户类型` varchar(15) NOT NULL DEFAULT '',
  `联系电话` char(11) NOT NULL DEFAULT '',
  `支付方式` varchar(15) NOT NULL DEFAULT '微信',
  PRIMARY KEY (`客户编号`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='客户表';

#
# Data for table "client"
#

/*!40000 ALTER TABLE `client` DISABLE KEYS */;
/*!40000 ALTER TABLE `client` ENABLE KEYS */;

#
# Structure for table "refund"
#

DROP TABLE IF EXISTS `refund`;
CREATE TABLE `refund` (
  `订票单号` varchar(15) NOT NULL DEFAULT '',
  `订票时间` varchar(15) NOT NULL DEFAULT '',
  `订票数量` int(2) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`订票单号`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='退票单';

#
# Data for table "refund"
#

/*!40000 ALTER TABLE `refund` DISABLE KEYS */;
/*!40000 ALTER TABLE `refund` ENABLE KEYS */;

#
# Structure for table "save"
#

DROP TABLE IF EXISTS `save`;
CREATE TABLE `save` (
  `票存系统编号` varchar(15) NOT NULL DEFAULT '',
  `票存系统地址` varchar(15) NOT NULL DEFAULT '',
  `出入帐金额` char(6) NOT NULL DEFAULT '',
  `出入帐类型` char(10) NOT NULL DEFAULT '',
  `记录时间` date NOT NULL DEFAULT '0000-00-00',
  PRIMARY KEY (`票存系统编号`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='存票表';

#
# Data for table "save"
#

/*!40000 ALTER TABLE `save` DISABLE KEYS */;
/*!40000 ALTER TABLE `save` ENABLE KEYS */;

#
# Structure for table "traincode"
#

DROP TABLE IF EXISTS `traincode`;
CREATE TABLE `traincode` (
  `车票编号` varchar(10) NOT NULL DEFAULT '',
  `车次` varchar(10) NOT NULL DEFAULT '',
  `出发站` varchar(10) NOT NULL DEFAULT '',
  `终点站` varchar(10) NOT NULL DEFAULT '',
  `票价` varchar(10) NOT NULL DEFAULT '',
  `出发时间` date NOT NULL DEFAULT '0000-00-00',
  `到站时间` date NOT NULL DEFAULT '0000-00-00',
  `座位信息` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`车票编号`) COMMENT '车票表'
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='车票表';

#
# Data for table "traincode"
#

/*!40000 ALTER TABLE `traincode` DISABLE KEYS */;
/*!40000 ALTER TABLE `traincode` ENABLE KEYS */;
