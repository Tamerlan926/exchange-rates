import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QLabel, QComboBox, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

API_URL = "http://127.0.0.1:8000/convert"

class MiniConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Конвертер")
        self.setFixedSize(300, 250) # Маленькое окно
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)


        self.label1 = QLabel("Из валюты:")
        self.combo1 = QComboBox()
        self.combo1.addItems(["USD", "EUR", "RUB", "GBP", "JPY", "CNY"])


        self.input_sum = QLineEdit()
        self.input_sum.setPlaceholderText("Введите сумму")
        

        self.label2 = QLabel("В валюту:")
        self.combo2 = QComboBox()
        self.combo2.addItems(["USD", "EUR", "RUB", "GBP", "JPY", "CNY"])
        self.combo2.setCurrentText("RUB") # По умолчанию рубли
        

        self.btn = QPushButton(" Конвертировать")
        self.btn.clicked.connect(self.do_convert)
        self.btn.setFixedHeight(50)  # Высота кнопки — 50 пикселей (было ~30)
        self.btn.setFont(QFont("Arial", 12, QFont.Bold))  # Жирный шрифт покрупнее
        self.btn.setStyleSheet("""
    background-color: #4CAF50; 
    color: white; 
    padding: 10px; 
    border-radius: 8px;
    font-weight: bold;
""")
        

        
        self.res_label = QLabel("Результат: ---")
        self.res_label.setAlignment(Qt.AlignCenter)
        self.res_label.setFont(QFont("Arial", 12, QFont.Bold))
        

        layout.addWidget(self.label1)
        layout.addWidget(self.combo1)
        layout.addWidget(self.input_sum)
        layout.addWidget(self.label2)
        layout.addWidget(self.combo2)
        layout.addWidget(self.btn)
        layout.addWidget(self.res_label)
        
        self.setLayout(layout)

    def do_convert(self):
        text = self.input_sum.text()
        if not text:
            QMessageBox.warning(self, "Ошибка", "Введите сумму!")
            return
        
        try:
            amount = float(text)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Нужно ввести число!")
            return

        data = {
            "amount": amount,
            "from_curr": self.combo1.currentText(),
            "to_curr": self.combo2.currentText()
        }

        try:
            resp = requests.post(API_URL, json=data, timeout=5)
            if resp.status_code == 200:
                res_data = resp.json()
                val = res_data['result']
                curr = self.combo2.currentText()
                self.res_label.setText(f"{val} {curr}")
            else:
                self.res_label.setText("Ошибка сервера")
        except Exception as e:
            self.res_label.setText("Нет связи с сервером")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MiniConverter()
    window.show()
    sys.exit(app.exec_())
