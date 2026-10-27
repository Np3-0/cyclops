from PyQt6.QtWidgets import QStackedWidget, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout

class DataCarousel(QWidget):
    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self.data = data
        
        self.main_layout = QVBoxLayout(self)
        # todo: 1. create carousel layout
        # 2. create method to generate carousel from data
        # 3. make it look good