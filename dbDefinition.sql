CREATE TABLE `opi`.`EventLog` (
  `eventTime` DATETIME NOT NULL,
  `eventType` VARCHAR(64) NOT NULL,
  `eventAnalogValue` DECIMAL(10,2) NULL,
  `eventDigitalValue` BOOL NULL,
  PRIMARY KEY (`eventTime`, `eventType`))
COMMENT = 'Table to log events';


CREATE TABLE `opi`.`StatusNotificationLog` (
  `notificationTime` DATETIME NOT NULL,
  `statusType` VARCHAR(64) NOT NULL,
  `emailSent` BOOL NULL,
  `smsSent` BOOL NULL,
  PRIMARY KEY (`notificationTime`, `statusType`))
COMMENT = 'Table to log status notifications';


CREATE TABLE `opi`.`AppConfig` (
  `property` VARCHAR(128) NOT NULL,
  `value` VARCHAR(128),
  `modificationTime` DATETIME,
  PRIMARY KEY (`property`))
COMMENT = 'Table to store AppConfig';