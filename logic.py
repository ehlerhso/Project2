from PyQt6.QtWidgets import *
from menugui import *
from AccountGUI import *
from WorkGUI import *
import sqlite3


class Logic(QMainWindow, Ui_Main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.size())  # Make window size unresizable

        # Setup database
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            userUPT REAL DEFAULT 0,
            userPTO REAL DEFAULT 0,
            userVacation REAL DEFAULT 0,
            userWORKDAY TEXT DEFAULT "Thursday",
            userHOURSWORKED REAL DEFAULT 0
            )"""
        )
        try:
            self.cursor.execute(
                "ALTER TABLE accounts ADD COLUMN userHOURSWORKED REAL DEFAULT 0"
            )
        except sqlite3.OperationalError:
            # Column already exists
            pass
        try:
            self.cursor.execute("ALTER TABLE accounts ADD COLUMN userWORKDAY TEXT DEFAULT 'Thursday'")
        except sqlite3.OperationalError:
            # Column already exists
            pass
        self.__current_user = None
        self.connection.commit()

        # Connect buttons
        self.pushButton.clicked.connect(self.register_user)
        self.pushButton_2.clicked.connect(self.login_user)
        self.pushButton_3.clicked.connect(self.viewAccount)

        # Mask password input
        self.lineEdit_2.setEchoMode(QLineEdit.EchoMode.Password)

    def register_user(self):
        """Creates a new user with the default database values and logs them in."""
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if username and password:
            try:
                # Insert new user into the database
                self.cursor.execute(
                    "INSERT INTO accounts (username, password, userUPT, userPTO, userVacation) VALUES (?, ?, 0.0, 0.0, 0.0)",
                    (username, password),
                )
                self.connection.commit()

                # Automatically log in the newly registered user
                self.cursor.execute("SELECT * FROM accounts WHERE username = ?", (username,))
                self.__current_user = self.cursor.fetchone()

                # Update UI to reflect the logged-in user
                self.label_3.setText(f"Account: {username}")
                print(f"User {username} registered and logged in.")
            except sqlite3.IntegrityError:
                self.label_3.setText("Username already exists.")
                print("Registration failed: Username already exists.")
            finally:
                self.lineEdit.clear()
                self.lineEdit_2.clear()

    def login_user(self):
        """Login user if the user exists."""
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if username and password:
            self.cursor.execute(
                "SELECT * FROM accounts WHERE username = ? AND password = ?", (username, password)
            )
            user = self.cursor.fetchone()
            if user:
                self.__current_user = user

                # Round time-off values to 2 decimal places
                self.cursor.execute(
                    "SELECT userUPT, userPTO, userVacation FROM accounts WHERE username = ?", (username,)
                )
                user_upt, user_pto, user_vacation = self.cursor.fetchone()

                rounded_upt = round(user_upt, 2)
                rounded_pto = round(user_pto, 2)
                rounded_vacation = round(user_vacation, 2)

                # Update the database with rounded values
                self.cursor.execute(
                    """UPDATE accounts
                       SET userUPT = ?, userPTO = ?, userVacation = ?
                       WHERE username = ?""",
                    (rounded_upt, rounded_pto, rounded_vacation, username),
                )
                self.connection.commit()

                # Update UI to reflect the logged-in user
                self.label_3.setText(f"Account: {username}")
                print(f"User {username} successfully logged in with rounded values.")
            else:
                self.label_3.setText("Invalid credentials.")
                print("Invalid credentials provided.")
            self.lineEdit.clear()
            self.lineEdit_2.clear()

    def viewAccount(self):
        """Display the account details in the AccountGUI."""
        if not self.__current_user:
            self.label_3.setText("No user is logged in.")
            return

        # Create and set up AccountGUI window
        self.accountWindow = QMainWindow()
        self.accountUI = Ui_Account()
        self.accountUI.setupUi(self.accountWindow)

        # Fetch user data
        username = self.__current_user[1]
        self.cursor.execute(
            "SELECT userUPT, userPTO, userVacation FROM accounts WHERE username = ?", (username,)
        )
        user_data = self.cursor.fetchone()

        # Update GUI with user data
        if user_data:
            self.accountUI.uptLabel.setText(f"Available UPT: {user_data[0]}")
            self.accountUI.ptoLabel.setText(f"Available PTO: {user_data[1]}")
            self.accountUI.vacationLabel.setText(f"Available Vacation: {user_data[2]}")

        # Connect buttons in AccountGUI
        self.accountUI.GoToShiftButton.clicked.connect(self.openWorkGUI)

        # Show the AccountGUI window
        self.accountWindow.show()

    def work5mins(self):
        """Simulate working for 5 minutes."""
        if not self.__current_user:
            return

        username = self.__current_user[1]
        self.cursor.execute("SELECT userHOURSWORKED FROM accounts WHERE username = ?", (username,))
        hours_worked = self.cursor.fetchone()[0]

        if hours_worked < 12:
            # Add 5 minutes as 0.05 hours
            hours_worked += 0.05

            # Adds an hour when minutes go past 60
            if hours_worked % 1 >= 0.60:
                hours_worked = int(hours_worked) + 1  # Add 1 hour and reset decimal to 0

            # Update the database
            self.cursor.execute(
                "UPDATE accounts SET userHOURSWORKED = ? WHERE username = ?", (hours_worked, username)
            )
            self.connection.commit()

            # Update the label in WorkGUI
            if hasattr(self, "workUI"):  # Check if WorkGUI is open
                self.workUI.AmountWorkedLabel.setText(f"Amount worked today: {hours_worked:.2f}")

    def work1hours(self):
        """Simulate working for 1 hour."""
        if not self.__current_user:
            return

        username = self.__current_user[1]
        self.cursor.execute("SELECT userHOURSWORKED FROM accounts WHERE username = ?", (username,))
        hours_worked = self.cursor.fetchone()[0]

        if hours_worked < 12:
            hours_worked += 1  # Add 1 hour
            self.cursor.execute(
                "UPDATE accounts SET userHOURSWORKED = ? WHERE username = ?", (hours_worked, username)
            )
            self.connection.commit()

            # Update the label in WorkGUI
            if hasattr(self, "workUI"):  # Check if WorkGUI is open
                self.workUI.AmountWorkedLabel.setText(f"Amount worked today: {hours_worked:.2f}")

    def calculateEndShiftToTimeOffGain(self):
        """Calculate time-off increments, reset hours worked, and update user day."""
        if not self.__current_user:
            return

        username = self.__current_user[1]
        self.cursor.execute("SELECT userHOURSWORKED, userWORKDAY FROM accounts WHERE username = ?", (username,))
        hours_worked, current_day = self.cursor.fetchone()
        upt_gain = round(hours_worked * 5 * 0.01, 2)
        pto_gain = round(hours_worked * 3 * 0.01, 2)
        vacation_gain = round(hours_worked * 1 * 0.01, 2)

        # Determine the next day using a dictionary
        day_cycle = {"Thursday": "Friday", "Friday": "Saturday", "Saturday": "Thursday"}
        next_day = day_cycle.get(current_day, "Thursday")  # Fallback to "Thursday" if current_day is invalid

        # Update time-off values and reset hours worked
        self.cursor.execute(
            """UPDATE accounts
               SET userUPT = userUPT + ?, userPTO = userPTO + ?, userVacation = userVacation + ?, 
                   userHOURSWORKED = 0, userWORKDAY = ?
               WHERE username = ?""",
            (upt_gain, pto_gain, vacation_gain, next_day, username),
        )

        # Check if the user time off minutes go above 60
        self.cursor.execute("SELECT userUPT, userPTO, userVacation FROM accounts WHERE username = ?", (username,))
        user_upt, user_pto, user_vacation = self.cursor.fetchone()

        # Extract tenths and hundredths for UPT, PTO, and Vacation
        user_upt_tenths, user_upt_hundredths = int((user_upt * 10) % 10), int((user_upt * 100) % 10)
        user_pto_tenths, user_pto_hundredths = int((user_pto * 10) % 10), int((user_pto * 100) % 10)
        user_vacation_tenths, user_vacation_hundredths = int((user_vacation * 10) % 10), int((user_vacation * 100) % 10)

        # Combine tenths and hundredths into minutes
        combined_upt_minutes = int(f"{user_upt_tenths}{user_upt_hundredths}")
        combined_pto_minutes = int(f"{user_pto_tenths}{user_pto_hundredths}")
        combined_vacation_minutes = int(f"{user_vacation_tenths}{user_vacation_hundredths}")

        # If minutes exceed 59.5 or 60, adjust to add hours
        if combined_upt_minutes >= 59.4:
            excess_hours = combined_upt_minutes // 60
            remaining_minutes = combined_upt_minutes % 60
            new_upt = int(user_upt) + excess_hours + (remaining_minutes / 100)
            self.cursor.execute(
                """UPDATE accounts
                   SET userUPT = ?
                   WHERE username = ?""",
                (new_upt, username),
            )
        if combined_pto_minutes >= 59.1:
            excess_hours = combined_pto_minutes // 60
            remaining_minutes = combined_pto_minutes % 60
            new_pto = int(user_pto) + excess_hours + (remaining_minutes / 100)
            self.cursor.execute(
                """UPDATE accounts
                   SET userPTO = ?
                   WHERE username = ?""",
                (new_pto, username),
            )
        if combined_vacation_minutes >= 59.1:
            excess_hours = combined_vacation_minutes // 60
            remaining_minutes = combined_vacation_minutes % 60
            new_vacation = int(user_vacation) + excess_hours + (remaining_minutes / 100)
            self.cursor.execute(
                """UPDATE accounts
                   SET userVacation = ?
                   WHERE username = ?""",
                (new_vacation, username),
            )

        self.connection.commit()

        # Update AccountGUI labels if open
        if hasattr(self, "accountUI"):
            self.cursor.execute(
                "SELECT userUPT, userPTO, userVacation FROM accounts WHERE username = ?", (username,)
            )
            updated_data = self.cursor.fetchone()
            if updated_data:
                self.accountUI.uptLabel.setText(f"Available UPT: {updated_data[0]:.2f}")
                self.accountUI.ptoLabel.setText(f"Available PTO: {updated_data[1]:.2f}")
                self.accountUI.vacationLabel.setText(f"Available Vacation: {updated_data[2]:.2f}")

        # Update WorkGUI's AmountWorkedLabel and shiftDayLabel if open
        if hasattr(self, "workUI"):
            self.workUI.AmountWorkedLabel.setText("Amount worked today: 0")
            self.workUI.shiftDayLabel.setText(f"Day: {next_day}")

        # Optional debug print
        print(f"Updated day: {next_day}")

    def openWorkGUI(self):
        """Opens the WorkGUI and displays the user hours worked data and the user day data."""
        if not self.__current_user:
            self.label_3.setText("No user is logged in.")
            return

        try:
            # Create and set up WorkGUI window
            self.workWindow = QMainWindow()
            self.workUI = Ui_WorkGUI()
            self.workUI.setupUi(self.workWindow)

            # Get the user data and display it
            username = self.__current_user[1]
            self.cursor.execute(
                "SELECT userHOURSWORKED, userWORKDAY FROM accounts WHERE username = ?", (username,)
            )
            user_data = self.cursor.fetchone()

            if user_data:
                hours_worked, work_day = user_data
                self.workUI.AmountWorkedLabel.setText(f"Amount worked today: {hours_worked}")
                self.workUI.shiftDayLabel.setText(f"Day: {work_day}")

            # Set up the button functions
            self.workUI.workButton.clicked.connect(self.work5mins)
            self.workUI.work1hourButton.clicked.connect(self.work1hours)
            self.workUI.EndShiftButton.clicked.connect(self.calculateEndShiftToTimeOffGain)

            self.workWindow.show()
        except Exception as i:
            print(f"workgui error: {i}")

        # Show WorkGUI
        self.workWindow.show()

