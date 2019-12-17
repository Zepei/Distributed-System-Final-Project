from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication, QPushButton)
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt
import sys

example_hand = 'S1 H2 D3 C4 S5 H6 D7 C8 S9 H10 D11 C12 S13'


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.find_match = QPushButton('Make a Match!')
        self.find_match.clicked.connect(self.find_match_handler)

        self.player_front_label = QLabel('Player Front')
        self.player_front_info = QLabel('n/a cards left\n Last played card: n/a')
        self.player_front_label.setAlignment(Qt.AlignHCenter)
        self.player_front_info.setAlignment(Qt.AlignCenter)

        self.player_left_label = QLabel('Player Left')
        self.player_left_info = QLabel('n/a cards left\n Last played card: n/a')

        self.player_right_label = QLabel('Player Right')
        self.player_right_info = QLabel('n/a cards left\n Last played card: n/a')

        self.table_info_edit = QTextEdit()
        self.table_info_edit.textChanged.connect(self.table_info_edit_changed)
        self.my_hand_label = QLabel('My Hand')
        self.my_hand_info = QLabel('Empty')
        self.my_hand_info.setAlignment(Qt.AlignCenter)
        self.my_hand_label.setAlignment(Qt.AlignHCenter)

        self.suit = QLabel('Enter a Suit')
        self.suit_edit = QLineEdit()
        self.number = QLabel('Enter a Number')
        self.number_edit = QLineEdit()

        self.play_button = QPushButton('Play!')
        self.play_button.setStyleSheet('QPushButton {height: 46px}')
        self.play_button.clicked.connect(self.play_card_handler)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(self.find_match, 0, 0)

        self.grid.addWidget(self.player_front_label, 0, 2, 1, 3)
        self.grid.addWidget(self.player_front_info, 1, 2, 1, 3)
        self.grid.addWidget(self.player_left_label, 3, 1)
        self.grid.addWidget(self.player_left_info, 4, 1)
        self.grid.addWidget(self.player_right_label, 3, 5)
        self.grid.addWidget(self.player_right_info, 4, 5)
        self.grid.addWidget(self.table_info_edit, 2, 2, 4, 3)
        self.grid.addWidget(self.my_hand_info, 6, 2, 1, 3)
        self.grid.addWidget(self.my_hand_label, 7, 2, 1, 3)
        self.grid.addWidget(self.suit, 8, 2)
        self.grid.addWidget(self.suit_edit, 8, 3)
        self.grid.addWidget(self.number, 9, 2)
        self.grid.addWidget(self.number_edit, 9, 3)
        self.grid.addWidget(self.suit, 8, 2)
        self.grid.addWidget(self.play_button, 8, 4, 2, 1)

        self.setLayout(self.grid)

        self.setGeometry(150, 150, 1200, 600)
        self.setWindowTitle('Spade')
        self.show()

    def find_match_handler(self):
        self.clear_all_fields()
        self.push_message_to_table("Finding a Match")
        self.push_message_to_table("A match is found!!!")
        self.my_hand_info.setText(example_hand)

    def play_card_handler(self):
        suit = self.suit_edit.text()
        number = self.number_edit.text()
        if suit == '' or number == '':
            self.push_message_to_table("You mush enter valid suit and number!")
            return
        self.push_message_to_table('You just played: '+suit+' '+number)
        self.update_hand('hand updated')

    def push_message_to_table(self, message):
        self.table_info_edit.setPlainText(self.table_info_edit.toPlainText()+message+'\n')

    def update_hand(self, my_hand):
        self.my_hand_info.setText(my_hand)

    def clear_table_info_edit(self):
        self.table_info_edit.clear()

    def clear_suit_edit(self):
        self.suit_edit.clear()

    def clear_number_edit(self):
        self.number_edit.clear()

    def clear_all_fields(self):
        self.player_front_info.setText('n/a cards left\n Last played card: n/a')
        self.player_left_info.setText('n/a cards left\n Last played card: n/a')
        self.player_right_info.setText('n/a cards left\n Last played card: n/a')
        self.my_hand_info.setText('Empty!')
        self.clear_table_info_edit()
        self.clear_suit_edit()
        self.clear_number_edit()

    def table_info_edit_changed(self):
        self.table_info_edit.moveCursor(QTextCursor.End)

    def update_front_info(self, num_of_cards_left, last_played_card):
        self.player_front_info.setText(f'{num_of_cards_left} cards left\n Last played card: {last_played_card}')

    def update_left_info(self, num_of_cards_left, last_played_card):
        self.player_left_info.setText(f'{num_of_cards_left} cards left\n Last played card: {last_played_card}')

    def update_right_info(self, num_of_cards_left, last_played_card):
        self.player_right_info.setText(f'{num_of_cards_left} cards left\n Last played card: {last_played_card}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    # ex.push_message_to_table('a test')
    app.exec_()
    sys.exit()
