#!/usr/bin/python

from dbConfig import *
import MySQLdb
import traceback
import logging
import time
from EventNames import *

def getDBConnection():
    try:
        return MySQLdb.connect(dbHost, dbUser, dbPass, dbSchema)

    except Exception as e:
        logging.error( "Failed to connect to database")
        logging.error(traceback.format_exc())
        logging.error(e.__doc__)
        logging.error(e.message)
        raise e


def closeDBConnection(dbConnection):
    try:
        if (dbConnection != None):
            dbConnection.close()

    except Exception as e:
        logging.error("Failed to close database connection")
        logging.error(traceback.format_exc())
        logging.error(e.__doc__)
        logging.error(e.message)
        raise e


def createEvent(eventType, eventAnalogValue, eventDigitalValue, eventTime):
    if eventType is None or (eventAnalogValue is None and eventDigitalValue is None):
        logging.warn("No enough data to log event")
    else:
        dbConnection = None

        rationalisedAnalogValue = getRationalisedAnalogValue(eventType, eventAnalogValue)
        #rationalisedAnalogValue = eventAnalogValue

        sql = "INSERT INTO EventLog(eventTime, eventType, eventAnalogValue, eventDigitalValue) VALUES (%s, %s, %s, %s)"

        try:
            dbConnection = getDBConnection()

            try:
                # Execute the SQL command
                dbConnection.cursor().execute(sql, (
                    eventTime.strftime('%Y-%m-%d %H:%M:%S'), eventType, rationalisedAnalogValue, bool(eventDigitalValue)))
                # Commit your changes in the database
                dbConnection.commit()

            except Exception as e:
                logging.error("Failed to create event.")
                logging.error(traceback.format_exc())
                logging.error(e.__doc__)
                logging.error(e.message)
                # Rollback in case there is any error
                dbConnection.rollback()

        except Exception as e:
            logging.error("Failed to create event.")
            logging.error(traceback.format_exc())
            logging.error(e.__doc__)
            logging.error(e.message)

        finally:
            if dbConnection is not None:
                closeDBConnection(dbConnection)


def getLatestEventEmailNotification():
    dbConnection = None

    sql = "SELECT statusType FROM StatusNotificationLog WHERE emailSent = TRUE ORDER BY notificationTime DESC LIMIT 1"

    try:
        dbConnection = getDBConnection()

        try:
            # Execute the SQL command
            cursor = dbConnection.cursor()
            cursor.execute(sql)

            if cursor.rowcount > 0:
                row = cursor.fetchone()
                return row[0]

            else:
                return None

        except Exception as e:
            logging.error("Failed to fetch event notification information")
            logging.error(traceback.format_exc())
            logging.error(e.__doc__)
            logging.error(e.message)

    except Exception as e:
        logging.error("Failed to fetch event notification information")
        logging.error(traceback.format_exc())
        logging.error(e.__doc__)
        logging.error(e.message)

    finally:
        if dbConnection is not None:
            closeDBConnection(dbConnection)


def getLatestEventSMSNotification():
    dbConnection = None

    sql = "SELECT statusType FROM StatusNotificationLog WHERE smsSent = TRUE ORDER BY notificationTime DESC LIMIT 1"

    try:
        dbConnection = getDBConnection()

        try:
            # Execute the SQL command
            cursor = dbConnection.cursor()
            cursor.execute(sql)

            if cursor.rowcount > 0:
                row = cursor.fetchone()
                return row[0]

            else:
                return None

        except Exception as e:
            logging.error("Failed to fetch event notification information")
            logging.error(traceback.format_exc())
            logging.error(e.__doc__)
            logging.error(e.message)

    except Exception as e:
        logging.error("Failed to fetch event notification information")
        logging.error(traceback.format_exc())
        logging.error(e.__doc__)
        logging.error(e.message)

    finally:
        if dbConnection is not None:
            closeDBConnection(dbConnection)


def createEventNotification(statusType, emailSent, smsSent):
    if statusType is None:
        logging.warn("No enough data to log event notification")
    else:
        dbConnection = None

        sql = "INSERT INTO StatusNotificationLog(notificationTime, statusType, emailSent, smsSent) VALUES (%s, %s, %s, %s)"

        try:
            dbConnection = getDBConnection()

            if emailSent is None:
                emailSent = False
            if smsSent is None:
                smsSent = False

            try:
                # Execute the SQL command
                dbConnection.cursor().execute(sql, (
                    time.strftime('%Y-%m-%d %H:%M:%S'), statusType, emailSent, smsSent))
                # Commit your changes in the database
                dbConnection.commit()

            except Exception as e:
                logging.error("Failed to create event notification.")
                logging.error(traceback.format_exc())
                logging.error(e.__doc__)
                logging.error(e.message)
                # Rollback in case there is any error
                dbConnection.rollback()

        except Exception as e:
            logging.error("Failed to create event notification.")
            logging.error(traceback.format_exc())
            logging.error(e.__doc__)
            logging.error(e.message)

        finally:
            if dbConnection is not None:
                closeDBConnection(dbConnection)


def getEventLogOfLastNHours(noOfHours, eventName):
    dbConnection = None

    sql = "SELECT eventTime, eventAnalogValue FROM EventLog WHERE (eventTime > DATE_SUB(NOW(), INTERVAL %s HOUR)) AND eventType = %s ORDER BY eventTime DESC"

    try:
        dbConnection = getDBConnection()

        try:
            # Execute the SQL command
            cursor = dbConnection.cursor()
            cursor.execute(sql, (noOfHours, eventName))

            if cursor.rowcount > 0:
                return cursor.fetchall()
            else:
                return None

        except Exception as e:
            logging.error("Failed to fetch event log information for last {0} hours".format(str(noOfHours)))
            logging.error(traceback.format_exc())
            logging.error(e.__doc__)
            logging.error(e.message)

    except Exception as e:
        logging.error("Failed to fetch event log information for last {0} hours".format(str(noOfHours)))
        logging.error(traceback.format_exc())
        logging.error(e.__doc__)
        logging.error(e.message)

    finally:
        if dbConnection is not None:
            closeDBConnection(dbConnection)


def getLatestEventsData():
    dbConnection = None

    sql = "select el.eventTime, el.eventAnalogValue, el.eventType  from EventLog as el join (select max(Eventtime) as eventTime,eventType from EventLog  group by eventType order by eventTime desc) as t1 on el.eventTime=t1.eventTime and el.eventtype = t1.eventtype;"

    try:
        dbConnection = getDBConnection()

        try:
            # Execute the SQL command
            cursor = dbConnection.cursor()
            cursor.execute(sql)

            if cursor.rowcount > 0:
                return cursor.fetchall()
            else:
                return None

        except Exception as e:
            logging.error("Failed to fetch latest event log information")
            logging.error(traceback.format_exc())
            logging.error(e.__doc__)
            logging.error(e.message)

    except Exception as e:
        logging.error("Failed to fetch latest event log information")
        logging.error(traceback.format_exc())
        logging.error(e.__doc__)
        logging.error(e.message)

    finally:
        if dbConnection is not None:
            closeDBConnection(dbConnection)


def getAvgAnalogValueOfLastNHours(noOfHours, eventName):
    dbConnection = None

    sql = "SELECT AVG(eventAnalogValue) FROM EventLog WHERE (eventTime > DATE_SUB(NOW(), INTERVAL %s HOUR)) AND eventType = %s ORDER BY eventTime DESC"

    try:
        dbConnection = getDBConnection()

        try:
            # Execute the SQL command
            cursor = dbConnection.cursor()
            cursor.execute(sql, (noOfHours, eventName))

            if cursor.rowcount > 0:
                return cursor.fetchone()[0]
            else:
                return None

        except Exception as e:
            logging.error("Failed to fetch event log information for last {0} hours".format(str(noOfHours)))
            logging.error(traceback.format_exc())
            logging.error(e.__doc__)
            logging.error(e.message)

    except Exception as e:
        logging.error("Failed to fetch event log information for last {0} hours".format(str(noOfHours)))
        logging.error(traceback.format_exc())
        logging.error(e.__doc__)
        logging.error(e.message)

    finally:
        if dbConnection is not None:
            closeDBConnection(dbConnection)


def getLatestAnalogValueForEvent(eventName):
    dbConnection = None

    sql = "SELECT eventAnalogValue FROM EventLog WHERE eventType = %s ORDER BY eventTime DESC LIMIT 1"

    try:
        dbConnection = getDBConnection()

        try:
            # Execute the SQL command
            cursor = dbConnection.cursor()
            cursor.execute(sql, (eventName))

            if cursor.rowcount > 0:
                return cursor.fetchone()[0]
            else:
                return None

        except Exception as e:
            logging.error("Failed to fetch Latest AnalogValue For {0}".format(str(eventName)))
            logging.error(traceback.format_exc())
            logging.error(e.__doc__)
            logging.error(e.message)

    except Exception as e:
        logging.error("Failed to fetch Latest AnalogValue For {0}".format(str(eventName)))
        logging.error(traceback.format_exc())
        logging.error(e.__doc__)
        logging.error(e.message)

    finally:
        if dbConnection is not None:
            closeDBConnection(dbConnection)


def getNumberOfXEventsInLastNMinutes(eventName, minutes):
    dbConnection = None

    sql = "SELECT count(*) FROM EventLog WHERE (eventTime > DATE_SUB(NOW(), INTERVAL %s MINUTE )) AND eventType = %s"

    try:
        dbConnection = getDBConnection()

        try:
            # Execute the SQL command
            cursor = dbConnection.cursor()
            cursor.execute(sql, (minutes,eventName))

            if cursor.rowcount > 0:
                return cursor.fetchone()[0]
            else:
                return None

        except Exception as e:
            logging.error("Failed to fetch Latest event counts For {0}".format(str(eventName)))
            logging.error(traceback.format_exc())
            logging.error(e.__doc__)
            logging.error(e.message)

    except Exception as e:
        logging.error("Failed to fetch Latest event counts For {0}".format(str(eventName)))
        logging.error(traceback.format_exc())
        logging.error(e.__doc__)
        logging.error(e.message)

    finally:
        if dbConnection is not None:
            closeDBConnection(dbConnection)




def getConfigValue(propertyName):

    if propertyName is None:
        return None

    dbConnection = None

    sql = "SELECT value FROM AppConfig WHERE property = %s"

    try:
        dbConnection = getDBConnection()

        try:
            # Execute the SQL command
            cursor = dbConnection.cursor()
            cursor.execute(sql, propertyName)

            if cursor.rowcount > 0:
                return cursor.fetchone()[0]
            else:
                return None

        except Exception as e:
            logging.error("Failed to fetch config information for {0} property".format(str(propertyName)))
            logging.error(traceback.format_exc())
            logging.error(e.__doc__)
            logging.error(e.message)

    except Exception as e:
        logging.error("Failed to fetch config information for {0} property".format(str(propertyName)))
        logging.error(traceback.format_exc())
        logging.error(e.__doc__)
        logging.error(e.message)

    finally:
        if dbConnection is not None:
            closeDBConnection(dbConnection)

def updateConfigValue(propertyName, propertyValue, timestamp):

    if propertyName is None:
        return False

    dbConnection = None

    sql = "UPDATE AppConfig set value = %s , modificationTime = %s WHERE property = %s"

    try:
        dbConnection = getDBConnection()

        try:
            # Execute the SQL command
            cursor = dbConnection.cursor()
            cursor.execute(sql, (propertyValue, timestamp, propertyName))
            dbConnection.commit()
            return True

        except Exception as e:
            logging.error("Failed to update config information for {0} property".format(str(propertyName)))
            logging.error(traceback.format_exc())
            logging.error(e.__doc__)
            logging.error(e.message)
            dbConnection.rollback()
            return False

    except Exception as e:
        logging.error("Failed to update config information for {0} property".format(str(propertyName)))
        logging.error(traceback.format_exc())
        logging.error(e.__doc__)
        logging.error(e.message)
        return False

    finally:
        if dbConnection is not None:
            closeDBConnection(dbConnection)


def createUser(username, hashedPassword):
    if username is None or hashedPassword is None:
        logging.warn("No enough data to create user")
    else:
        dbConnection = None

        sql = "INSERT INTO UserRecords(username, password) VALUES (%s, %s)"

        try:
            dbConnection = getDBConnection()
            try:
                # Execute the SQL command
                dbConnection.cursor().execute(sql, (username,hashedPassword))
                # Commit your changes in the database
                dbConnection.commit()

            except Exception as e:
                logging.error("Failed to create user.")
                logging.error(traceback.format_exc())
                logging.error(e.__doc__)
                logging.error(e.message)
                # Rollback in case there is any error
                dbConnection.rollback()

        except Exception as e:
            logging.error("Failed to create user.")
            logging.error(traceback.format_exc())
            logging.error(e.__doc__)
            logging.error(e.message)

        finally:
            if dbConnection is not None:
                closeDBConnection(dbConnection)


def getRationalisedAnalogValue(eventName, currentAnalogValue):

    if eventName == WaterPlantEvent:
        return currentAnalogValue

    lastAnalogValue = float(getLatestAnalogValueForEvent(eventName))

    if eventName in (CheckTemperatureEvent, CheckHumidityEvent):
        deviation = 10

    elif eventName in (CheckMoistureLevelEvent,CheckWaterLevelEvent):
        var_no_of_mins_for_rational_value = getConfigValue('no_of_mins_for_rational_value')
        if var_no_of_mins_for_rational_value is None:
            var_no_of_mins_for_rational_value = 21
        if (getNumberOfXEventsInLastNMinutes(WaterPlantEvent,var_no_of_mins_for_rational_value) == 0):
            deviation = 5
        else:
            deviation = 100

    observed_deviation = ((currentAnalogValue - lastAnalogValue) / lastAnalogValue) * 100

    if observed_deviation < 0:
        observed_deviation *= -1

    if observed_deviation > deviation:
        return lastAnalogValue
    else:
        return currentAnalogValue

