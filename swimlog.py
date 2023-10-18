from cs50 import SQL
from pyfiglet import Figlet
from tabulate import tabulate
import random, sys, time

# initiate figlet
figlet = Figlet()
# connect to database
db = SQL("sqlite:///SwimLog.db")


def main():
    # Use pyfiglet and random to assign the program title a random font
    # each time it is run (this is just for fun)
    figlet.setFont(font=random.choice(figlet.getFonts()))
    print(figlet.renderText("SWIM LOG"))

    # Main menu (Menu 1)
    """
    Menu is infinite-looped until the user wishes to quit the program
    or the program proceeds further, but it always brings the user back
    to the main menu to quit the program.
    """
    while True:
        time.sleep(1)
        print(
            "\nSelect desired action:\n1 - Enter new data.\n2 - View existing data.\n3 - Modify existing data.\n4 - End program.\n"
        )
        # Get user input, use try-except and conditionals to validate
        first_choice = input("Option: ")
        try:
            first_choice = int(first_choice)
            if first_choice == 1:
                # Get back list of new data to be added, convert to int and split into individual variables
                data = new_swim_data()
                distance = int(data[0])
                pool = int(data[1])
                duration = int(data[2])
                # Add new data to database using custom function
                db_update(distance, pool, duration)
            elif first_choice == 2:
                # If there is no existing data, user cannot access this option
                if db_check():
                    existing_swim_data()
            elif first_choice == 3:
                # If there is no existing data, user cannot access this option
                if db_check():
                    modify_data()
            elif first_choice == 4:
                sys.exit()
            else:
                print("\nEnter a valid option number.\n")

        except ValueError:
            print("\nEnter a valid option number.\n")


# Get new data from user
def new_swim_data():
    # User input sequence is an infinite loop if the input is invalid
    while True:
        distance = input("\nDistance swam in meters: ")
        pool = input("Pool length in meters: ")
        duration = input("Duration of session in minutes: ")
        # If all inputs are valid, return input values as a list
        if valid(distance) and valid(pool) and valid(duration):
            return [distance, pool, duration]
        else:
            print("\nEnter valid data.")


# Validate user input
def valid(n):
    try:
        n = int(n)
        if n > 0:
            return True
        else:
            return False
    except ValueError:
        return False


# Add new data to database
def db_update(distance, pool, duration):
    db.execute(
        "INSERT INTO swim_data(distance, pool, duration) VALUES(?, ?, ?)",
        distance,
        pool,
        duration,
    )


# Menu 2 - to view and analyze existing data
"""
Menu is looped, allowing the user to access all options
until they decide to break out of this loop by going back to Menu 1/Main menu.
"""


def existing_swim_data():
    while True:
        time.sleep(1)
        print(
            "\n1 - View data table.\n2 - Total distance swam.\n3 - Total time spent swimming.\n4 - Average distance swam per session.\n5 - Average time spent swimming per session.\n6 - Go back to main menu.\n"
        )
        # Get user input, use try-except and conditionals to validate
        second_choice = input("Option: ")
        try:
            second_choice = int(second_choice)
            if second_choice == 1:
                db_read()
            elif second_choice == 2:
                total_distance()
            elif second_choice == 3:
                total_time()
            elif second_choice == 4:
                average_distance()
            elif second_choice == 5:
                average_time()
            elif second_choice == 6:
                break
            else:
                print("\nEnter a valid option number.\n")

        except ValueError:
            print("\nEnter a valid option number.\n")


# Check if data exists or if the database is empty
def db_check():
    data = db.execute("SELECT * FROM swim_data")
    if not data:
        print("\nThere is no existing data. Please add data to the database first.")
        return False
    else:
        return True


# Print out existing data as a table using tabulate module
def db_read():
    print()
    data = db.execute("SELECT * FROM swim_data")
    print(tabulate(data, headers="keys", tablefmt="grid"))


# Display total distance swam
def total_distance():
    total_distance_list = db.execute("SELECT SUM(distance) AS n FROM swim_data")
    total_distance = total_distance_list[0]["n"]
    # Total distance in meters if < 1 kilometer
    if total_distance < 1000:
        print(f"\nTotal distance swam: {total_distance} meters")
    # Total distance in kilometers if >= 1 kilometer
    else:
        print(f"\nTotal distance swam: {total_distance/1000} kilometers")


# Display total time spent swimming
def total_time():
    total_time_list = db.execute("SELECT SUM(duration) AS n FROM swim_data")
    total_time = total_time_list[0]["n"]
    # Total time in minutes if < 1 hour
    if total_time < 60:
        print(f"\nTotal time spent swimming: {total_time} minutes")
    # Total time in hours, minutes if >= 1 hour
    else:
        hours = total_time // 60
        minutes = total_time % 60
        print(f"\nTotal time spent swimming: {hours} hour(s), {minutes} minute(s)")


# Display average distance swam per session
def average_distance():
    distance_list = db.execute("SELECT SUM(distance) AS m FROM swim_data")
    distance = distance_list[0]["m"]
    sessions_list = db.execute("SELECT COUNT(*) AS n FROM swim_data")
    sessions = sessions_list[0]["n"]
    average = round(distance / sessions, 2)
    # Average distance in meters if < 1 kilometer
    if average < 1000:
        print(f"\nAverage distance swam per session: {average} meters")
    # Average distance in kilometers if >= 1 kilometer
    else:
        print(f"\nAverage distance swam per session: {average} kilometers")


# Display average time spent swimming per session
def average_time():
    total_time_list = db.execute("SELECT SUM(duration) AS m FROM swim_data")
    duration = total_time_list[0]["m"]
    sessions_list = db.execute("SELECT COUNT(*) AS n FROM swim_data")
    sessions = sessions_list[0]["n"]
    average = round(duration / sessions)
    # Average time in minutes if < 1 hour
    if average < 60:
        print(f"\nAverage time spent swimming per session: {average} minutes")
    # Average time in hours, minutes if >= 1 hour
    else:
        hours = average // 60
        minutes = average % 60
        print(
            f"\nAverage time spent swimming per session: {hours} hour(s), {minutes} minute(s)"
        )


# Modify existing data
def modify_data():
    # Print out existing data as a table using tabulate module
    print()
    db_read()

    # Menu 3
    """
    Infinite loop, until the user inputs a valid session number.
    """
    while True:
        # Get user input, use try-except and conditionals to validate
        try:
            time.sleep(1)
            id = int(input("\nEnter the session number of the session to be updated: "))
            session_list = db.execute("SELECT session FROM swim_data")
            id_list = []
            for session in session_list:
                if not session["session"] in id_list:
                    id_list.append(session["session"])

            if id in id_list:
                break
            else:
                print("\nEnter a valid session number.")
        except ValueError:
            print("\nEnter a valid session number.")

    """
    Infinite loop to allow the user to modify more than
    just one aspect of a session.
    """
    while True:
        # Get user input, use try-except and conditionals to validate
        try:
            time.sleep(1)
            print(
                "\nSelect desired data to modify:\n1 - Distance.\n2 - Pool length.\n3 - Duration.\n4 - Go back to main menu."
            )
            third_choice = int(input("\nOption: "))

            if third_choice == 1:
                distance = input("\nDistance swam in meters: ")
                if valid(distance):
                    db.execute(
                        "UPDATE swim_data SET distance = ? WHERE session = ?",
                        distance,
                        id,
                    )
                else:
                    print("\nEnter valid data.")
            elif third_choice == 2:
                pool = input("\nPool length in meters: ")
                if valid(pool):
                    db.execute(
                        "UPDATE swim_data SET pool = ? WHERE session = ?", pool, id
                    )
                else:
                    print("\nEnter valid data.")
            elif third_choice == 3:
                duration = input("\nDuration of session in minutes: ")
                if valid(duration):
                    db.execute(
                        "UPDATE swim_data SET duration = ? WHERE session = ?",
                        duration,
                        id,
                    )
                else:
                    print("\nEnter valid data.")
            elif third_choice == 4:
                break
            else:
                print("\nEnter a valid option number.")
        except ValueError:
            print("\nEnter a valid option number.")


if __name__ == "__main__":
    main()
