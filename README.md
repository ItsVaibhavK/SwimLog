# SWIM LOG

## IDEA BEHIND SWIM LOG
As a person who swims fairly regularly for exercise, I wanted to track my basic swimming data, like:
- Distance swam in a session
- Pool length
- Duration of a session

And to be able to analyze the data, with parameters such as:
- Total distance swam
- Total time spent swimming
- Average distance swam per session
- Average duration of a session

Before I decided to turn this idea into my final project for [CS50P](https://cs50.harvard.edu/python/2022/), I was trying out various swim-tracking apps on my phone,<br>but they were all invariably too cluttered for my taste. More often than not, it was about pushing the user to sign up for swimming lessons,<br>or to connect a smart watch that would share your swimming session data to the app for you.

Most of the apps had the option to manually update your swimming session data, but it was almost always without fail locked behind a paywall.<br>This is what ultimately led me to utilize what I have been learning through [CS50P](https://cs50.harvard.edu/python/2022/) and [CS50X](https://cs50.harvard.edu/x/2023/) and create a Python program<br>to allow me to
log/track the data from my swimming sessions.

## HOW SWIM LOG WORKS
### Libraries used:
- **cs50** - Using `from cs50 import SQL` enables the program to talk to the SQLite3 database, so that SQL queries can be executed within Python code.

- **pyfiglet** and **random** - I wanted the title of the program to appear in a _fun different_ font each time it was executed.<br>I utilized `from pyfiglet import Figlet` and `import random` to render the title in different fonts on each iteration.

- **tabulate** - For the option(s) that involved viewing existing data, I needed a way to print the data in a readable format.<br>`from tabulate import tabulate` was used to meet this goal.

- **time** - The output was flying by a little too fast for my taste, so I added `time.sleep(1)` at various points in the code to allow time to read,<br>or at least grasp the fact that the output was on the screen.

- **sys** - `sys.exit()` is what is run when the user decides to end the program.

### Schema for data table:
This was the **SQL command** run to create the data table:

CREATE TABLE swim_data (<br>session INTEGER PRIMARY KEY AUTOINCREMENT,<br>date DATETIME DEFAULT CURRENT_TIMESTAMP,<br>distance INTEGER NOT NULL,<br>pool INTEGER NOT NULL,<br>duration INTEGER NOT NULL<br>);

### Flow (menus, and the loops and conditionals behind them):
There are three menus that the user can navigate:
1. **Menu 1 (Main menu)** - Add new data, view/analyze existing data, modify existing data, or end the program.

2. **Menu 2** - Multiple options to view existing data, or to go back to **Menu 1**.

3. **Menu 3** - Choose what aspect of existing data is to be modified, or to go back to **Menu 1**.

All the menus are infinite-looped, allowing the user to accomplish multiple tasks at a time without having to navigate through the program from the beginning each time.<br>When the program is run, the user is presented with **Menu 1**.

#### MENU 1 (MAIN MENU)
---
**Menu 1** presents the user with the following options:
1. Enter new data.
2. View existing data.
3. Modify existing data.
4. End program.

The user is asked to input the option number corresponding to the task they wish to accomplish.<br>User input is validated using a `try-except` block, and `if-elif-else` conditionals.

If the user chooses to "Enter new data", `new_swim_data()` is called and the user is asked to input the various parameters of their swimming session.<br>User input is further validated using `valid(n)`, and if the data checks out, the database is updated by the function `db_update(distance, pool, duration)`.

If the user chooses to "View existing data", or "Modify existing data", since both the options require that there should _be_ existing data,<br>`db_check()` is called first to prevent errors that would arise from an empty database.<br>If the database is not empty, the user is presented with further options. If the database is _empty_, the user is asked to add data first, and they are redirected back to **Menu 1**.

If the user chooses to "End program", `sys.exit()` is used to terminate the program.

#### MENU 2
---
If the user chooses to "View existing data", the program proceeds to present **Menu 2**:
1. View data table.
2. Total distance swam.
3. Total time spent swimming.
4. Average distance swam per session.
5. Average time spent swimming per session.
6. Go back to main menu.

The user is asked to input the option number corresponding to the task they wish to accomplish.<br>User input is validated using a `try-except` block, and `if-elif-else` conditionals. Here is how each option works:
1. View data table - `db_read()` is called to execute a SQL query, and existing data is outputted as a table using the `tabulate` library.

2. Total distance swam - `total_distance()` is called, the corresponding SQL query is executed to acquire the required data.<br>If the total distance is less than 1 kilometer, the output is displayed in meters. If the total distance is greater than or equal to 1 kilometer, the output is displayed in kilometers.

3. Total time spent swimming - `total_time()` is called, the corresponding SQL query is executed to acquire the required data.<br>If the total time is less than 1 hour, the output is displayed in minutes. If the total time is greater than or equal to 1 hour, the output is displayed in hours and minutes.

4. Average distance swam per session - `average_distance()` is called, the corresponding SQL query is executed to acquire the required data.<br>If the average distance is less than 1 kilometer, the output is displayed in meters.<br>If the average distance is greater than or equal to 1 kilometer, the output is displayed in kilometers.

5. Average time spent swimming per session - `average_time()` is called, the corresponding SQL query is executed to acquire the required data.<br>If the average time is less than 1 hour, the output is displayed in minutes. If the average time is greater than or equal to 1 hour, the output is displayed in hours and minutes.

(_Note:_ For the average distance/time options, the **session** column from the table **swim_data** is used to calculate the number of entries made,<br>where each entry corresponds to one session. The **session** "number" or "ID" itself is not looked at to calculate the averages.)

6. Go back to main menu - `break` is used to end the **Menu 2** loop and take the user back to **Menu 1**.

#### MENU 3
---
If the user chooses to "Modify existing data", first, `modify_data()` is called and the existing data is displayed to the user by utilizing the `db_read()` function.<br>The user is then asked to enter the **session number** of the session whose data they wish to change. This particular input from the user is validated by<br>retrieving session numbers/IDs from the **session** column of the **swim_data** table and storing them in a list. Using an `if-else` condition,<br>the user's input is checked against the same list. If user input is valid, the program proceeds further. If user input is not found in the list of **session** IDs,<br>an error message appears and the user is prompted (infinitely) to enter a valid session number.

Once the user inputs a valid **session** number, they are presented with **Menu 3**, where they are asked to input the option number corresponding to the _data_ they wish to _modify_.<br>User input is validated using a `try-except` block, and `if-elif-else` conditionals:
1. Distance.
2. Pool length.
3. Duration.
4. Go back to main menu.

Depending on the option that is selected, user input (the new data to replace the old/incorrect data) is first validated by calling `valid(n)`,<br>following which that particular aspect of the selected **session** is updated in the database using a SQL query.

If option "4. Go back to main menu" is selected, `break` is used to end the **Menu 3** loop and take the user back to **Menu 1**.

## DESIGN THOUGHTS AND FUTURE IDEAS:
1. Each menu is infinite-looped so that the user can go through multiple options on a single execution of the program.

2. Error messages due to invalid inputs also loop infintely, reprompting the user to cooperate until they provide a valid input.

3. Using `random` and `pyfiglet` to render the title in a different font on each execution of the program was for personal amusement.

4. Distance covered in a session, pool length, and the duration of a session are the current parameters that are the focus of Swim Log<br>since these are the main parameters I care about for my personal data. I would, however, like to also consider adding parameters<br>such as number of laps and swim pace in a future version.

5. The program currently only stores/calculates distance data under the metric system. An idea for a future version of Swim Log could be<br>to provide the option of selecting what system of measurement the user would like to implement.

6. Currently, the date/timestamp data is not used in any way apart from a form of record-keeping.<br>Utilizing the date/timestamp data to see milestones like start date, year, etc. can also be considered.

## CREDITS, CONCLUSION:
I cannot express my gratitude and admiration of the staff and team at CS50 enough for sharing their knowledge with students like me,<br>and for their time, effort and dedication behind the plethora of courses offered by Harvard's CS50 on [edX.](https://www.edx.org/) I went from not knowing anything about programming at all<br>to writing my own programs and web apps in these last few months.<br>Thank you from the bottom of my heart for instilling in me the love of all things programming!

_To quote [Professor Malan](https://cs.harvard.edu/malan/):_
> This was CS50!
