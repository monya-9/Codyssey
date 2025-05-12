# Codyssey No.7 - 문제4 계산기의 핵심 코어 제작
# 계산기 만들기

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout,
    QPushButton, QLineEdit, QMessageBox
)
from PyQt5.QtGui import QFont


class Calculator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current = '0'
        self.operator = None
        self.operand = None
        self.result_shown = False

    def input_digit(self, digit):
        if self.result_shown:
            self.current = digit
            self.result_shown = False
        elif self.current == '0':
            self.current = digit
        else:
            self.current += digit

    def input_dot(self):
        if '.' not in self.current:
            self.current += '.'

    def set_operator(self, op):
        if self.operator and not self.result_shown:
            self.equal()
        self.operator = op
        self.operand = float(self.current)
        self.result_shown = True

    def add(self):
        self.set_operator('+')

    def subtract(self):
        self.set_operator('-')

    def multiply(self):
        self.set_operator('*')

    def divide(self):
        self.set_operator('/')

    def negative_positive(self):
        if self.current.startswith('-'):
            self.current = self.current[1:]
        else:
            self.current = '-' + self.current

    def percent(self):
        try:
            value = float(self.current) / 100
            self.current = str(value)
        except Exception:
            self.current = 'Error'

    def equal(self):
        if not self.operator:
            return

        try:
            second = float(self.current)
            if self.operator == '+':
                result = self.operand + second
            elif self.operator == '-':
                result = self.operand - second
            elif self.operator == '*':
                result = self.operand * second
            elif self.operator == '/':
                if second == 0:
                    self.current = 'Error'
                    return
                result = self.operand / second
            else:
                result = second

            if abs(result) > 1e100:
                self.current = 'Overflow'
            else:
                result = round(result, 6)
                self.current = str(result).rstrip('0').rstrip('.') if '.' in str(result) else str(result)

        except Exception:
            self.current = 'Error'
        finally:
            self.operator = None
            self.result_shown = True


class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.calculator = Calculator()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Calculator')
        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont('Arial', 24))

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.display)

        grid = QGridLayout()
        buttons = [
            ('C', self.reset), ('+/-', self.negative_positive), ('%', self.percent), ('/', self.divide),
            ('7', lambda: self.input_digit('7')), ('8', lambda: self.input_digit('8')), ('9', lambda: self.input_digit('9')), ('*', self.multiply),
            ('4', lambda: self.input_digit('4')), ('5', lambda: self.input_digit('5')), ('6', lambda: self.input_digit('6')), ('-', self.subtract),
            ('1', lambda: self.input_digit('1')), ('2', lambda: self.input_digit('2')), ('3', lambda: self.input_digit('3')), ('+', self.add),
            ('0', lambda: self.input_digit('0')), ('.', self.input_dot), ('=', self.equal)
        ]

        positions = [(i, j) for i in range(5) for j in range(4)]

        for position, (text, handler) in zip(positions, buttons):
            if text == '':
                continue
            button = QPushButton(text)
            button.setFont(QFont('Arial', 18))
            button.clicked.connect(handler)
            grid.addWidget(button, *position)

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    def update_display(self):
        text = self.calculator.current
        length = len(text)
        font_size = max(18, 36 - length)
        self.display.setFont(QFont('Arial', font_size))
        self.display.setText(text)

    def input_digit(self, digit):
        self.calculator.input_digit(digit)
        self.update_display()

    def input_dot(self):
        self.calculator.input_dot()
        self.update_display()

    def reset(self):
        self.calculator.reset()
        self.update_display()

    def negative_positive(self):
        self.calculator.negative_positive()
        self.update_display()

    def percent(self):
        self.calculator.percent()
        self.update_display()

    def add(self):
        self.calculator.add()
        self.update_display()

    def subtract(self):
        self.calculator.subtract()
        self.update_display()

    def multiply(self):
        self.calculator.multiply()
        self.update_display()

    def divide(self):
        self.calculator.divide()
        self.update_display()

    def equal(self):
        self.calculator.equal()
        self.update_display()


if __name__ == '__main__':
    from PyQt5.QtCore import Qt

    app = QApplication(sys.argv)
    calc = CalculatorUI()
    calc.show()
    sys.exit(app.exec_())
