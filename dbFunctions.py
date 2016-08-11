#!/usr/bin/python

from dbConfig import *
import MySQLdb
import traceback
import logging
import time


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


def createEvent(eventType, eventAnalogValue, eventDigitalValue):
    if eventType is None or (eventAnalogValue is None and eventDigitalValue is None):
        print "No enough data to log event"
    else:
        dbConnection = None

        sql = "INSERT INTO EventLog(eventTime, eventType, eventAnalogValue, eventDigitalValue) VALUES (%s, %s, %s, %s)"

        try:
            dbConnection = getDBConnection()

            try:
                # Execute the SQL command
                dbConnection.cursor().execute(sql, (time.strftime('%Y-%m-%d %H:%M:%S'), eventType, eventAnalogValue, bool(eventDigitalValue)))
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
