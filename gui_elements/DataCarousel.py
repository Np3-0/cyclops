from PySide6.QtWidgets import QStackedWidget, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QTableView, QHeaderView
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
    def __init__(self, data: dict, size: int):
        super().__init__()
        self.step = data
        self.size = size
        self.setObjectName("carouselWidget")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.widget_layout = QVBoxLayout(self)
        self.step_name = QLabel(f"{self.step['name']} - {self.step['step']}/{self.size}")
        self.widget_layout.addWidget(self.step_name)

        self.view = QTableView(self)
        self.model = DataTableModel(data['reagents'], COLUMNS, self.view)
        self.view.setModel(self.model)
        self.header = self.view.horizontalHeader()
        self.header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.widget_layout.addWidget(self.view)
        
        self.setStyleSheet(f"""
            QLabel {{
                font-weight: bold;
                font-size: 24px;
                margin-bottom: 12px;
            }}
            
            QWidget#carouselWidget {{
                background: {constants.secondary_bg};
                border-radius: 10px;
            }}
            
            QTableView {{
                gridline-color: {constants.primary_accent};
                background-color: {constants.primary_bg};
                font-weight: semibold;
                font-size: 14px;
            }}
            
            QHeaderView::section {{
                background-color: {constants.primary_bg};
                border: 1px solid {constants.primary_accent};
                font-weight: bold;
                font-size: 16px;
            }}
            
            QTableView QScrollBar:vertical {{
                background: {constants.primary_accent};
                border-radius: 6px;
                margin: 0px;
                width: 12px;
            }}
            
             QTableView QScrollBar::handle:vertical {{
                background: {constants.secondary_bg};
                min-height: 24px;
                border-radius: 6px;
            }}

            QTableView QScrollBar::handle:vertical:hover {{
                background: {constants.secondary_bg};
            }}

            QTableView QScrollBar::add-line:vertical,
            QTableView QScrollBar::sub-line:vertical {{
                height: 0px;
            }}

            QTableView QScrollBar::add-page:vertical,
            QTableView QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """)

    def set_highlight(self, row):
        self.model.set_highlight(row)
        if row is not None:
            self.view.scrollTo(self.model.index(row, 0))
            
class DataCarousel(QWidget):
    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self.data = data
        self.cur_index = 0
        
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.main_layout = QVBoxLayout(self)
        
        self.carousel_stack = QStackedWidget()
        for item in data['steps']:
            self.carousel_stack.addWidget(CarouselWidget(item, len(data['steps'])))
        self.main_layout.addWidget(self.carousel_stack)
        
        self.nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton("Previous")
        self.next_btn = QPushButton("Next")
        
        self.prev_btn.clicked.connect(self.prev_ind)
        self.prev_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_btn.clicked.connect(self.next_ind)
        self.next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.nav_layout.addWidget(self.prev_btn)
        self.nav_layout.addWidget(self.next_btn)
        self.main_layout.addLayout(self.nav_layout)
        
        self.setStyleSheet(f"""
                QPushButton {{
                border: 2px solid {constants.primary_accent};
                border-radius: 10px;
                min-height: 50px;
                background: {constants.primary_bg};
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
    
    def set_pos(self, page, row):
        steps = self.data['steps']
        if not 0 <= page < len(steps): return
        
        self.cur_index = page
        self.carousel_stack.setCurrentIndex(page)
        
        for i in range(self.carousel_stack.count()):
            widget = self.carousel_stack.widget(i)
            widget.set_highlight(row if i == page else None)