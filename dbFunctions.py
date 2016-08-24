#!/usr/bin/python

from dbConfig import *
import MySQLdb
import traceback
import logging
import time
from sqlalchemy import create_engine

engine = create_engine('mysql://{0}:{1}@{2}/{3}'.format(dbUser,dbPass,dbHost,dbSchema))

def getDBConnection():
    try:
        #return MySQLdb.connect(dbHost, dbUser, dbPass, dbSchema)
        return engine.connect()

    except Exception as e:
        print "Failed to connect to database"
        logging.error(traceback.format_exc())
        print e.__doc__
        print e.message
        raise e


def closeDBConnection(dbConnection):
    try:
        if (dbConnection != None):
            dbConnection.close()

    except Exception as e:
        print "Failed to close database connection"
        logging.error(traceback.format_exc())
        print e.__doc__
        print e.message
        raise e


def createEvent(eventType, eventAnalogValue, eventDigitalValue, eventTime):
    if eventType is None or (eventAnalogValue is None and eventDigitalValue is None):
        print "No enough data to log event"
    else:
        dbConnection = None

        sql = "INSERT INTO EventLog(eventTime, eventType, eventAnalogValue, eventDigitalValue) VALUES (%s, %s, %s, %s)"

        try:
            dbConnection = getDBConnection()

            try:
                # Execute the SQL command
                dbConnection.cursor().execute(sql, (
                    eventTime.strftime('%Y-%m-%d %H:%M:%S'), eventType, eventAnalogValue, bool(eventDigitalValue)))
                # Commit your changes in the database
                dbConnection.commit()

            except Exception as e:
                print "Failed to create event."
                logging.error(traceback.format_exc())
                print e.__doc__
                print e.message
                # Rollback in case there is any error
                dbConnection.rollback()

        except Exception as e:
            print "Failed to create event."
            logging.error(traceback.format_exc())
            print e.__doc__
            print e.message

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
            print "Failed to fetch event notification information"
            logging.error(traceback.format_exc())
            print e.__doc__
            print e.message

    except Exception as e:
        print "Failed to fetch event notification information"
        logging.error(traceback.format_exc())
        print e.__doc__
        print e.message

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
            print "Failed to fetch event notification information"
            logging.error(traceback.format_exc())
            print e.__doc__
            print e.message

    except Exception as e:
        print "Failed to fetch event notification information"
        logging.error(traceback.format_exc())
        print e.__doc__
        print e.message

    finally:
        if dbConnection is not None:
            closeDBConnection(dbConnection)


def createEventNotification(statusType, emailSent, smsSent):
    if statusType is None:
        print "No enough data to log event notification"
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
                print "Failed to create event notification."
                logging.error(traceback.format_exc())
                print e.__doc__
                print e.message
                # Rollback in case there is any error
                dbConnection.rollback()

        except Exception as e:
            print "Failed to create event notification."
            logging.error(traceback.format_exc())
            print e.__doc__
            print e.message

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
            print "Failed to fetch event log information for last {0} hours".format(str(noOfHours))
            logging.error(traceback.format_exc())
            print e.__doc__
            print e.message

    except Exception as e:
        print "Failed to fetch event log information for last {0} hours".format(str(noOfHours))
        logging.error(traceback.format_exc())
        print e.__doc__
        print e.message

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
            print "Failed to fetch event log information for last {0} hours".format(str(noOfHours))
            logging.error(traceback.format_exc())
            print e.__doc__
            print e.message

    except Exception as e:
        print "Failed to fetch event log information for last {0} hours".format(str(noOfHours))
        logging.error(traceback.format_exc())
        print e.__doc__
        print e.message

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
            print "Failed to fetch config information for {0} property".format(str(propertyName))
            logging.error(traceback.format_exc())
            print e.__doc__
            print e.message

    except Exception as e:
        print "Failed to fetch config information for {0} property".format(str(propertyName))
        logging.error(traceback.format_exc())
        print e.__doc__
        print e.message

    finally:
        if dbConnection is not None:
            closeDBConnection(dbConnection)

