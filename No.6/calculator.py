# Codyssey No.6 - 문제3 계산기의 제작
# 계산기 만들기

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLineEdit


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('iPhone Style Calculator')
        self.setFixedSize(300, 400)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setFixedHeight(60)
        self.display.setStyleSheet('font-size: 24px')
        main_layout.addWidget(self.display)

        grid = QGridLayout()

        buttons = [
            ['C', '+/-', '%', '/'],
            ['7', '8', '9', 'x'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '0', '.', '=']
        ]

        for row in range(5):
            for col in range(4):
                label = buttons[row][col]

                if row == 4 and col == 1:
                    continue  # skip second '0' for iPhone-style wide button

                button = QPushButton(label)
                button.setFixedSize(60, 60)
                button.setStyleSheet('font-size: 18px')
                button.clicked.connect(lambda checked, val=label: self.button_clicked(val))

                if row == 4 and col == 0:
                    grid.addWidget(button, row, col, 1, 2)  # wide '0' button
                elif row == 4 and col > 1:
                    grid.addWidget(button, row, col)
                else:
                    grid.addWidget(button, row, col)

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    def button_clicked(self, value):
        current_text = self.display.text()

        if value == 'C':
            self.display.clear()
        else:
            self.display.setText(current_text + value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())