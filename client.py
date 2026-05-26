import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

API_URL = "http://127.0.0.1:8000/convert"

class MiniConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Конвертер валют")
        self.setFixedSize(320, 320)  
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 15, 20, 15)


        title = QLabel("Конвертер")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        


        layout.addWidget(QLabel("Из валюты:"))
        self.combo_from = QComboBox()
        self.combo_from.addItems(["USD", "EUR", "RUB", "GBP", "JPY", "CNY"])
        layout.addWidget(self.combo_from)
        


        self.input_sum = QLineEdit()
        self.input_sum.setPlaceholderText("Введите сумму")
        self.input_sum.setFixedHeight(35)
        layout.addWidget(self.input_sum)
        


        layout.addWidget(QLabel("В валюту:"))
        self.combo_to = QComboBox()
        self.combo_to.addItems(["USD", "EUR", "RUB", "GBP", "JPY", "CNY"])
        self.combo_to.setCurrentText("RUB")
        layout.addWidget(self.combo_to)
        
 
 
        self.btn = QPushButton(" Конвертировать")
        self.btn.clicked.connect(self.do_convert)
        self.btn.setFixedHeight(50)
        self.btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.btn.setStyleSheet("""
background-color: #4CAF50; 
color: white; 
border-radius: 8px;
font-weight: bold;
        """)
        layout.addWidget(self.btn)
        


        spacer = QLabel("")          
        spacer.setFixedHeight(15)    
        layout.addWidget(spacer)

        
        self.res_label = QLabel("Результат: ---")
        self.res_label.setAlignment(Qt.AlignCenter)
        self.res_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.res_label.setStyleSheet("color: black;")  
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
            "from_curr": self.combo_from.currentText(),
            "to_curr": self.combo_to.currentText()
        }

        try:
            resp = requests.post(API_URL, json=data, timeout=5)
            if resp.status_code == 200:
                res_data = resp.json()
                val = res_data['result']
                curr = self.combo_to.currentText()
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
    app = QApplication(sys.argv)
    window = MiniConverter()
    window.show()
    sys.exit(app.exec_())
