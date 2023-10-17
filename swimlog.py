from cs50 import SQL
from pyfiglet import Figlet
from tabulate import tabulate
import datetime, random, sys, time

figlet = Figlet()
db = SQL("sqlite:///SwimLog.db")


def main():
    figlet.setFont(font=random.choice(figlet.getFonts()))
    print(figlet.renderText("SWIM LOG"))

    while True:
        time.sleep(1)
        print(
            "\nWould you like to:\n1. Enter new swim data.\n2. Go through existing swim data.\n3. Modify existing swim data.\n4. Exit program.\n"
        )
        first_choice = input("Choice: ")
        try:
            first_choice = int(first_choice)
            if first_choice == 1:
                data = new_swim_data()
                distance = int(data[0])
                pool = int(data[1])
                duration = int(data[2])
                db_update(distance, pool, duration)
            elif first_choice == 2:
                existing_swim_data()
            elif first_choice == 3:
                modify_data()
            elif first_choice == 4:
                sys.exit()
            else:
                print("\nEnter a valid option.\n")

        except ValueError:
            print("\nEnter a valid option.\n")


def new_swim_data():
    while True:
        distance = input("\nDistance swam in meters: ")
        pool = input("Pool length in meters: ")
        duration = input("Duration of session in minutes: ")

        if valid(distance) and valid(pool) and valid(duration):
            return [distance, pool, duration]
        else:
            print("\nEnter valid figures.")


def valid(n):
    while True:
        try:
            n = int(n)
            if n > 0:
                return True
            else:
                return False
        except ValueError:
            return False


def db_update(distance, pool, duration):
    db.execute(
        "INSERT INTO swim_data(distance, pool, duration) VALUES(?, ?, ?)",
        distance,
        pool,
        duration,
    )


def existing_swim_data():
    while True:
        time.sleep(1)
        print(
            "\n1. Swim data table.\n2. Total distance swam.\n3. Total time spent swimming.\n4. Average distance swam per session.\n5. Average time spent swimming per session.\n6. Go back to previous menu.\n"
        )
        second_choice = input("Choice: ")
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
                print("\nEnter a valid option.\n")

        except ValueError:
            print("\nEnter a valid option.\n")


def db_read():
    print()
    data = db.execute("SELECT * FROM swim_data")
    print(tabulate(data, headers="keys", tablefmt="grid"))


def total_distance():
    total_distance_list = db.execute("SELECT SUM(distance) AS n FROM swim_data")
    total_distance = total_distance_list[0]["n"]
    if total_distance < 1000:
        print(f"\n{total_distance} meters")
    else:
        print(f"\n{total_distance/1000} kilometers")


def total_time():
    total_time_list = db.execute("SELECT SUM(duration) AS n FROM swim_data")
    total_time = total_time_list[0]["n"]
    if total_time < 60:
        print(f"\n{total_time} minutes")
    else:
        hours = total_time // 60
        minutes = total_time % 60
        print(f"\n{hours} hours, {minutes} minutes")


def average_distance():
    distance_list = db.execute("SELECT SUM(distance) AS m FROM swim_data")
    distance = distance_list[0]["m"]
    sessions_list = db.execute("SELECT COUNT(*) AS n FROM swim_data")
    sessions = sessions_list[0]["n"]
    average = round(distance / sessions, 1)
    if average < 1000:
        print(f"\n{average} meters")
    else:
        print(f"\n{average} kilometers")


def average_time():
    total_time_list = db.execute("SELECT SUM(duration) AS m FROM swim_data")
    duration = total_time_list[0]["m"]
    sessions_list = db.execute("SELECT COUNT(*) AS n FROM swim_data")
    sessions = sessions_list[0]["n"]
    average = round(duration / sessions)
    if average < 60:
        print(f"\n{average} minutes")
    else:
        hours = average // 60
        minutes = average % 60
        print(f"\n{hours} hours, {minutes} minutes")


def modify_data():
    print()
    data = db.execute("SELECT * FROM swim_data")
    print(tabulate(data, headers="keys", tablefmt="grid"))

    while True:
        try:
            time.sleep(1)
            id = int(input("\nSelect the session to be updated: "))
            session_list = db.execute("SELECT session FROM swim_data")
            id_list = []
            for session in session_list:
                if not session["session"] in id_list:
                    id_list.append(session["session"])

            if id in id_list:
                break
            else:
                print("\nEnter a valid session ID.")
        except ValueError:
            print("\nEnter a valid session ID.")

    while True:
        try:
            time.sleep(1)
            print(
                "\nWould you like to modify:\n1. Distance.\n2. Pool length.\n3. Duration.\n4. Go back to previous menu."
            )
            third_choice = int(input("\nChoice: "))

            if third_choice == 1:
                distance = input("\nDistance swam in meters: ")
                if valid(distance):
                    db.execute(
                        "UPDATE swim_data SET distance = ? WHERE session = ?",
                        distance,
                        id,
                    )
                else:
                    print("\nEnter valid figures.")
            elif third_choice == 2:
                pool = input("\nPool length in meters: ")
                if valid(pool):
                    db.execute(
                        "UPDATE swim_data SET pool = ? WHERE session = ?", pool, id
                    )
                else:
                    print("\nEnter valid figures.")
            elif third_choice == 3:
                duration = input("\nDuration of session in minutes: ")
                if valid(duration):
                    db.execute(
                        "UPDATE swim_data SET duration = ? WHERE session = ?",
                        duration,
                        id,
                    )
                else:
                    print("\nEnter valid figures.")
            elif third_choice == 4:
                break
            else:
                print("\nEnter a valid option.")
        except ValueError:
            print("\nEnter a valid option.")


if __name__ == "__main__":
    main()
