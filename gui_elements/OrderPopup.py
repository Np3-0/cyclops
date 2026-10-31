from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel
from gui_elements.DataCarousel import DataCarousel
from utils.get_data import get_dye_id_from_info

class OrderPopup(QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent, Qt.WindowType.Window)
        self.data = data
        
        self.indexes = [0, 0]
        self.current_reagent = data['steps'][self.indexes[0]]['reagents'][self.indexes[1]]
        self.setWindowTitle("Order Information")
        self.resize(550, 500)
        self.main_layout = QVBoxLayout(self)
        self.carousel = DataCarousel(data)
        self.main_layout.addWidget(self.carousel)
        self.update_highlight()

        
    def set_indexes(self, page, row):
        self.indexes = [page, row]
        self.current_reagent = self.data['steps'][page]['reagents'][row]
        self.update_highlight()
    
    def update_highlight(self):
        self.carousel.set_pos(*self.indexes)
        
    def check_dye(self, dye_info):
        correct_ids = get_dye_id_from_info(
            self.current_reagent['marker'],
            self.current_reagent['dye'],
            self.current_reagent['box'],
        )
        found_id = dye_info['id']
        print(correct_ids, found_id, found_id in correct_ids)