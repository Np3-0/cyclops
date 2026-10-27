from PySide6.QtWidgets import QStackedWidget, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QTableView
from PySide6.QtCore import Qt
import constants
from gui_elements.DataTableModel import DataTableModel

COLUMNS = [
    ("Marker", "marker"),
    ("Dye", "dye"),
    ("Box", "box"),
    ("Address", "address"),
    ("Volume (µL)", "volume_ul"),
]

class CarouselWidget(QWidget):
    def __init__(self, data: dict):
        super().__init__()
        self.step = data
        self.setObjectName("carouselWidget")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.widget_layout = QVBoxLayout(self)
        self.step_name = QLabel(self.step['name'])
        self.widget_layout.addWidget(self.step_name, alignment=Qt.AlignmentFlag.AlignTop)

        self.view = QTableView(self)
        self.model = DataTableModel(data['reagents'], COLUMNS, self.view)
        self.view.setModel(self.model)
        self.widget_layout.addWidget(self.view)
        
        self.setStyleSheet(f"""
            QLabel {{
                font-weight: bold;
                font-size: 24px;
            }}
            
            QWidget#carouselWidget {{
                background: {constants.secondary_bg};
                border-radius: 10px;
            }}
        """)

class DataCarousel(QWidget):
    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self.data = data
        self.cur_index = 0
        
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.main_layout = QVBoxLayout(self)
        
        self.carousel_stack = QStackedWidget()
        for item in data['steps']:
            self.carousel_stack.addWidget(CarouselWidget(item))
        self.main_layout.addWidget(self.carousel_stack)
        
        self.nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton("Previous")
        self.next_btn = QPushButton("Next")
        
        self.prev_btn.clicked.connect(self.prev_ind)
        self.next_btn.clicked.connect(self.next_ind)
        
        self.nav_layout.addWidget(self.prev_btn)
        self.nav_layout.addWidget(self.next_btn)
        self.main_layout.addLayout(self.nav_layout)
        
        self.setStyleSheet(f"""
                QPushButton {{
                border: 2px solid {constants.primary_accent};
                border-radius: 10px;
                max-height: 75px;
                background: {constants.secondary_bg};
                font-size: 18px;
                font-weight: bold;
            }}   
        """)
        
    def next_ind(self):
        self.cur_index = (self.cur_index + 1) % len(self.data['steps'])
        self.carousel_stack.setCurrentIndex(self.cur_index)
        
    def prev_ind(self):
        self.cur_index = (self.cur_index - 1) % len(self.data['steps'])
        self.carousel_stack.setCurrentIndex(self.cur_index)
    
        # todo: 1. create carousel layout
        # 2. create method to generate carousel from data
        # 3. make it look good