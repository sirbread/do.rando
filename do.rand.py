import sys
import random
import requests
from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui

highest_score = None
lowest_score = None
cooldown_time = 3
username = None
title = "Dö.rand"

def roll_number():
    return round(random.uniform(0.00000000001, 9.99999999999), 11)

def log_score(score_type, score_value):
    current_time = datetime.now()
    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
    with open("score_log.txt", "a") as log_file:
        log_file.write(f"New {score_type} achieved at {timestamp}: {score_value}\n")
    print(f"New {score_type} achieved at {timestamp}: {score_value}")

def send_score(score, username):
    try:
        response = requests.post("http://127.0.0.1:5000/submit_score", json={"score": score, "username": username})
        print(f"Score submission response: {response.json()}")
    except Exception as e:
        print(f"Failed to send score: {e}")

class UsernameWindow(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 300, 200)
        self.setStyleSheet("background-color: #34495e; color: #ffffff;") 
        self.setWindowIcon(QtGui.QIcon("smolico.png"))
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        layout.addSpacerItem(QtWidgets.QSpacerItem(20, 15))  

        self.splash_image = QtWidgets.QLabel(self)
        self.splash_image.setPixmap(QtGui.QPixmap("Splash.png").scaled(250, 150, QtCore.Qt.KeepAspectRatio))
        self.splash_image.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.splash_image)

        layout.addSpacerItem(QtWidgets.QSpacerItem(20, 15)) 

        self.username_label = QtWidgets.QLabel("Create your username:")
        self.username_label.setFont(QtGui.QFont("SansSerif", 16, QtGui.QFont.Bold))
        layout.addWidget(self.username_label)

        h_layout = QtWidgets.QHBoxLayout()

        self.username_entry = QtWidgets.QLineEdit()
        self.username_entry.setFont(QtGui.QFont("SansSerif", 14))  
        self.username_entry.setStyleSheet("border: 2px solid #2980b9; padding: 5px; border-radius: 5px;")
        self.username_entry.setFixedHeight(40) 
        h_layout.addWidget(self.username_entry)

        self.submit_button = QtWidgets.QPushButton()
        self.submit_button.setIcon(QtGui.QIcon("arrow_icon.png")) 
        self.submit_button.setIconSize(QtCore.QSize(20, 20)) 
        self.submit_button.setFixedHeight(40)  
        self.submit_button.setFixedWidth(40) 
        self.submit_button.setStyleSheet(""" 
            QPushButton {
                background-color: #2980b9; 
                color: white; 
                border-radius: 5px; 
                padding: 0;  
            }
            QPushButton:hover {
                background-color: #1f6a99;  
            }
        """)
        self.submit_button.clicked.connect(self.submit_username)
        h_layout.addWidget(self.submit_button)

        layout.addLayout(h_layout) 

        self.error_label = QtWidgets.QLabel("")
        self.error_label.setFont(QtGui.QFont("SansSerif", 12))  
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)

        self.how_to_play_button = QtWidgets.QPushButton("How to Play")
        self.how_to_play_button.setFont(QtGui.QFont("SansSerif", 14))  
        self.how_to_play_button.setStyleSheet(""" 
            QPushButton {
                background-color: #2980b9; 
                color: white; 
                border-radius: 5px; 
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1f6a99; 
            }
        """)

        self.how_to_play_button.clicked.connect(self.show_how_to_play)
        layout.addWidget(self.how_to_play_button)

        self.setLayout(layout)


    def show_how_to_play(self):
        dialog = HowToPlayDialog()
        dialog.exec_()

    def submit_username(self):
        global username
        username = self.username_entry.text().strip()
        
        if not username or len(username) < 3 or len(username) > 15 or not username.isalnum():
            self.error_label.setText("Username must be 3-15 characters \nlong and alphanumeric.")
            return
        
        self.error_label.setText("")
        self.check_username_availability()

    def check_username_availability(self):
        response = requests.post("http://127.0.0.1:5000/submit_username", json={"username": username})

        if response.status_code == 200:
            self.close()
            self.start_game()
        else:
            self.error_label.setText("Username taken. Try another.")

    def start_game(self):
        self.game_window = GameWindow()
        self.game_window.show()

class HowToPlayDialog(QtWidgets.QDialog):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("How to Play")
        self.setGeometry(200, 200, 300, 250)
        self.setStyleSheet("background-color: #34495e; color: #ffffff;")
        self.setWindowIcon(QtGui.QIcon("smolico.png"))

        layout = QtWidgets.QVBoxLayout()

        instructions = QtWidgets.QLabel("Instructions:\n\n"
                                         "1. Enter a unique username.\n"
                                         "2. Click 'Roll Number' to generate a random number,\n"
                                         "    and wait until the cooldown is finished.\n"
                                         "3. The highest and lowest rolls that you made\n"
                                         "    will be tracked and recorded.\n"
                                         "4. You can view the leaderboard at localhost:5000.")
        instructions.setFont(QtGui.QFont("SansSerif", 12))
        layout.addWidget(instructions)

        close_button = QtWidgets.QPushButton("Close")
        close_button.setFont(QtGui.QFont("SansSerif", 14))
        close_button.setStyleSheet(""" 
            QPushButton {
                background-color: #2980b9; 
                color: white; 
                border-radius: 5px; 
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1f6a99; 
            }
        """)
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)

class ConfirmationDialog(QtWidgets.QDialog):

    def __init__(self, username, highest_score, lowest_score):
        super().__init__()
        self.setWindowTitle("Confirm Exit")
        self.setGeometry(200, 200, 300, 300) 
        self.setStyleSheet("background-color: #34495e; color: #ffffff;")
        self.setWindowIcon(QtGui.QIcon("smolico.png"))

        layout = QtWidgets.QVBoxLayout()

        info_background = QtWidgets.QWidget()
        info_background.setStyleSheet("""
            background-color: #151c24; 
            border-radius: 10px; 
            padding: 10px;
        """)
        info_layout = QtWidgets.QVBoxLayout(info_background)

        username_label = QtWidgets.QLabel(f"Username: {username}")
        username_label.setFont(QtGui.QFont("SansSerif", 14))  
        info_layout.addWidget(username_label)

        highest_label = QtWidgets.QLabel(f"Highest Roll: {highest_score}")
        highest_label.setFont(QtGui.QFont("SansSerif", 14)) 
        info_layout.addWidget(highest_label)

        lowest_label = QtWidgets.QLabel(f"Lowest Roll: {lowest_score}")
        lowest_label.setFont(QtGui.QFont("SansSerif", 14))  
        info_layout.addWidget(lowest_label)

        layout.addWidget(info_background)

        confirmation_background = QtWidgets.QWidget()
        confirmation_background.setStyleSheet("""
            background-color: #151c24; 
            border-radius: 10px; 
            padding: 10px;
        """)
        confirmation_layout = QtWidgets.QVBoxLayout(confirmation_background)

        confirmation_label = QtWidgets.QLabel("Are you sure you want to quit?")
        confirmation_label.setFont(QtGui.QFont("SansSerif", 14, QtGui.QFont.Bold))
        confirmation_label.setAlignment(QtCore.Qt.AlignLeft) 
        confirmation_layout.addWidget(confirmation_label)

        layout.addWidget(confirmation_background)

        button_layout = QtWidgets.QHBoxLayout()

        yes_button = QtWidgets.QPushButton("Yes")
        yes_button.setFont(QtGui.QFont("SansSerif", 14))
        yes_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white; 
                border-radius: 5px; 
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        yes_button.clicked.connect(self.accept)

        no_button = QtWidgets.QPushButton("No")
        no_button.setFont(QtGui.QFont("SansSerif", 14))
        no_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db; 
                color: white; 
                border-radius: 5px; 
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9; 
            }
        """)
        no_button.clicked.connect(self.reject)

        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)


class GameWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 300, 400)
        self.setStyleSheet("background-color: #34495e; color: #ffffff;")
        self.setWindowIcon(QtGui.QIcon("smolico.png"))

        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        self.current_username_label = QtWidgets.QLabel(f"Username: {username}")
        self.current_username_label.setFont(QtGui.QFont("SansSerif", 14))
        self.current_username_label.setStyleSheet("""
            background-color: #151c24;
            color: white;
            padding: 10px;
            border-radius: 10px;
        """)
        layout.addWidget(self.current_username_label)

        title_label = QtWidgets.QLabel("Roll a number")
        title_label.setFont(QtGui.QFont("SansSerif", 16, QtGui.QFont.Bold))
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)

        self.current_roll_label = QtWidgets.QLabel("Latest roll: ")
        self.current_roll_label.setFont(QtGui.QFont("SansSerif", 14))
        self.current_roll_label.setStyleSheet("""
            background-color: #151c24;
            color: white;
            padding: 10px;
            border-radius: 10px;
        """)
        layout.addWidget(self.current_roll_label)

        self.highest_score_label = QtWidgets.QLabel("Highest: ")
        self.highest_score_label.setFont(QtGui.QFont("SansSerif", 14))
        self.highest_score_label.setStyleSheet("""
            background-color: #151c24;
            color: white;
            padding: 10px;
            border-radius: 10px;
        """)
        layout.addWidget(self.highest_score_label)

        self.lowest_score_label = QtWidgets.QLabel("Lowest: ")
        self.lowest_score_label.setFont(QtGui.QFont("SansSerif", 14))
        self.lowest_score_label.setStyleSheet("""
            background-color: #151c24;
            color: white;
            padding: 10px;
            border-radius: 10px;
        """)
        layout.addWidget(self.lowest_score_label)

        self.roll_button = QtWidgets.QPushButton("Roll Number")
        self.roll_button.setFont(QtGui.QFont("SansSerif", 14))
        self.roll_button.setStyleSheet("""
            QPushButton {
                background-color: #2980b9; 
                color: white; 
                border-radius: 5px; 
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1f6a99; 
            }
        """)

        self.roll_button.clicked.connect(self.play_game)
        layout.addWidget(self.roll_button)

        self.cooldown_label = QtWidgets.QLabel("")
        self.cooldown_label.setFont(QtGui.QFont("SansSerif", 14))
        layout.addWidget(self.cooldown_label)

        self.setLayout(layout)

    def play_game(self):
        global highest_score, lowest_score, cooldown_time

        self.roll_button.setDisabled(True)
        cooldown_time = 3

        current_roll = roll_number()
        self.animate_roll(self.current_roll_label, current_roll)

        if highest_score is None or current_roll > highest_score:
            highest_score = current_roll
            self.animate_roll(self.highest_score_label, highest_score) 
            self.highest_score_label.setText(f"Highest: {highest_score}")
            log_score("highest", highest_score)

        if lowest_score is None or current_roll < lowest_score:
            lowest_score = current_roll
            self.animate_roll(self.lowest_score_label, lowest_score) 
            self.lowest_score_label.setText(f"Lowest: {lowest_score}")
            log_score("lowest", lowest_score)

        send_score(current_roll, username)
        self.roll_button.setDisabled(True)
        self.update_cooldown_label()

    def animate_roll(self, label, target_value):
        label.setText(f"{label.text().split(':')[0]}: ")
        self.random_roll_animation(label, target_value, 0)

    def random_roll_animation(self, label, target_value, index):
        if index < 21: 
            random_symbols = self.generate_random_symbols(12) 
            label.setText(f"{label.text().split(':')[0]}: {random_symbols}")
            QtCore.QTimer.singleShot(30, lambda: self.random_roll_animation(label, target_value, index + 1))  
        else:
            label.setText(f"{label.text().split(':')[0]}: {target_value}")

    def generate_random_symbols(self, length):
        symbols = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        return ''.join(random.choices(symbols, k=length))

    def update_cooldown_label(self):
        global cooldown_time
        if cooldown_time > 0:
            self.cooldown_label.setText(f"Next roll in: {cooldown_time} seconds")

            cooldown_time -= 1
            QtCore.QTimer.singleShot(1000, self.update_cooldown_label)
        else:
            self.cooldown_label.setText("")
            self.roll_button.setDisabled(False) 

    def closeEvent(self, event):
        dialog = ConfirmationDialog(username, highest_score, lowest_score)
        self.hide()  
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            event.accept() 
        else:
            self.show()  
            event.ignore()  

def main():
    app = QtWidgets.QApplication(sys.argv)
    username_window = UsernameWindow()
    username_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
