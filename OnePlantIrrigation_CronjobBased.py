# ---------------------------------------------------------------------------------------------------------------------
# This is main file which will use all other utilities to detect the moisture and turn on the tap if moisture is less.
# This will also send email notifications about current status of the plant.
# ---------------------------------------------------------------------------------------------------------------------


from MoistureSensorFunctions import *
import sys
from GenerateGraph import plot_graph


# ---------------------------------------------------------------------------------------------------------------------
# Call this python file at scheduled intervals using cron job utility.
# ---------------------------------------------------------------------------------------------------------------------

# Gather our code in a main() function
def main():
    try:
        # Setup GPIO for experiment
        setup_gpio()

        # Just call callback function which checks sensor, and does required actions.
        callback()

        if len(sys.argv) > 1 and bool(sys.argv[1]):
            print "Plat graph flag: " + sys.argv[1]
            plot_graph(False)

    except KeyboardInterrupt:
        print "Program terminated on user interrupt."

    except Exception as e:
        logging.error(traceback.format_exc())
        print e.__doc__
        print e.message

    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    finally:
        cleanupGPIO()


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
