from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication, QPushButton)
from PyQt5.QtGui import QTextCursor
import sys


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.find_match = QPushButton('Make a Match!')
        self.find_match.clicked.connect(self.find_match_handler)

        self.table_info = QLabel('Table Log: ')
        self.table_info_edit = QTextEdit()
        self.table_info_edit.textChanged.connect(self.table_info_edit_changed)
        self.hand_info = QLabel('Your Hand: ')
        self.hand_info_edit = QTextEdit()
        self.hand_info_edit.setStyleSheet('QTextEdit {height: 200px}')

        self.suit = QLabel('Select a Suit')
        self.suit_edit = QLineEdit()
        self.number = QLabel('Select a Number')
        self.number_edit = QLineEdit()

        self.play_button = QPushButton('Play!')
        self.play_button.setStyleSheet('QPushButton {height: 40px}')
        self.play_button.clicked.connect(self.play_card_handler)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(self.find_match, 0, 0)

        self.grid.addWidget(self.table_info, 0, 1)
        self.grid.addWidget(self.table_info_edit, 0, 2, 1, 2)
        self.grid.addWidget(self.hand_info, 1, 1)
        self. grid.addWidget(self.hand_info_edit, 1, 2, 1, 2)

        self.grid.addWidget(self.suit, 2, 1)
        self.grid.addWidget(self.suit_edit, 2, 2)

        self.grid.addWidget(self.play_button, 2, 3, 2, 1)

        self.grid.addWidget(self.number, 3, 1)
        self. grid.addWidget(self.number_edit, 3, 2)

        self.setLayout(self.grid)

        self.setGeometry(300, 300, 800, 300)
        self.setWindowTitle('Spade')
        self.show()

    def find_match_handler(self):
        self.clear_all_fields()
        self.push_message_to_table("Finding a Match")
        self.push_message_to_table("A match is found!!!")

    def play_card_handler(self):
        suit = self.suit_edit.text()
        number = self.number_edit.text()
        self.push_message_to_table('You just played: '+suit+' '+number)
        self.update_hand('your hand is updated')

    def push_message_to_table(self, message):
        self.table_info_edit.setPlainText(self.table_info_edit.toPlainText()+message+'\n')

    def update_hand(self, message):
        self.hand_info_edit.setText(message)

    def clear_table_info_edit(self):
        self.table_info_edit.clear()

    def clear_hand_info_edit(self):
        self.hand_info_edit.clear()

    def clear_suit_edit(self):
        self.suit_edit.clear()

    def clear_number_edit(self):
        self.number_edit.clear()

    def clear_all_fields(self):
        self.clear_hand_info_edit()
        self.clear_table_info_edit()
        self.clear_suit_edit()
        self.clear_number_edit()

    def table_info_edit_changed(self):
        self.table_info_edit.moveCursor(QTextCursor.End)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    # ex.push_message_to_table('a test')
    app.exec_()
    sys.exit()
