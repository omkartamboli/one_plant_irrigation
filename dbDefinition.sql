CREATE TABLE `opi`.`EventLog` (
  `eventTime` DATETIME NOT NULL,
  `eventType` VARCHAR(64) NOT NULL,
  `eventAnalogValue` DECIMAL(10,2) NULL,
  `eventDigitalValue` BOOL NULL,
  PRIMARY KEY (`eventTime`, `eventType`))
COMMENT = 'Table to log events';
