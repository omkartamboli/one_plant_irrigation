#!/usr/bin/python

from dbConfig import *
import MySQLdb
import traceback
import logging
import datetime


def getDBConnection():
    try:
        return MySQLdb.connect(dbHost, dbUser, dbPass, dbSchema)

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


def createEvent(timeStamp, eventType, eventAnalogValue, eventDigitalValue):
    if timeStamp is None or eventType is None or (eventAnalogValue is None and eventDigitalValue is None):
        print "No enough data to log event"
    else:
        dbConnection = None
        a = datetime.datetime.strptime(timeStamp, "%b %d %Y %H:%M")
        sql = "INSERT INTO EventLog(eventTime, eventType, eventAnalogValue, eventDigitalValue) VALUES ('%s', '%s', '%d', '%d' )",(
            a.strftime('%Y-%m-%d %H:%M:%S'), eventType, eventAnalogValue, eventDigitalValue)
        try:
            dbConnection = getDBConnection()

            try:
                # Execute the SQL command
                dbConnection.cursor().execute(sql)
                # Commit your changes in the database
                dbConnection.commit()
            except:
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
