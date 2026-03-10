from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton)

class AddWordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('新增单词')
        self.setGeometry(200, 200, 400, 150)
        
        layout = QVBoxLayout()
        
        english_layout = QHBoxLayout()
        english_layout.addWidget(QLabel('英文:'))
        self.english_input = QLineEdit()
        english_layout.addWidget(self.english_input)
        layout.addLayout(english_layout)
        
        chinese_layout = QHBoxLayout()
        chinese_layout.addWidget(QLabel('中文:'))
        self.chinese_input = QLineEdit()
        chinese_layout.addWidget(self.chinese_input)
        layout.addLayout(chinese_layout)
        
        button_layout = QHBoxLayout()
        ok_btn = QPushButton('确定')
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton('取消')
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_data(self):
        return self.english_input.text(), self.chinese_input.text()