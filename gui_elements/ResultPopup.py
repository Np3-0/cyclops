from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt
import constants

class ResultPopup(QDialog):
    
    def __init__(self, dye_info: dict, parent=None):
        super().__init__(parent)
        self.dye_info = dye_info
        self.setWindowTitle("Dye Info")
        self.resize(480, 540)
        self.layout = QVBoxLayout(self)
        
        self.title_widget = QWidget()
        self.title_widget.setObjectName("titleWidget")
        self.title_widget_layout = QVBoxLayout(self.title_widget)
        self.title_widget.setAttribute(Qt.WA_StyledBackground, True)

        self.title_widget_layout.setSpacing(15)
        self.title_widget_layout.setContentsMargins(25, 25, 25, 25)
        
        self.dye_name = QLabel(self.dye_info['name'], alignment=Qt.AlignTop | Qt.AlignHCenter)
        self.dye_name.setObjectName("dyeName")
        self.title_widget_layout.addWidget(self.dye_name)
        
        self.dye_id = QLabel(f"ID: {self.dye_info['id']}")
        self.dye_id.setObjectName("dyeID")
        self.title_widget_layout.addWidget(self.dye_id, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
        self.expire_layout = QHBoxLayout()
        self.date_received = QLabel(f"Date Received: {self.dye_info['date_received']}")
        self.expire_date = QLabel(f"Expiration Date: {self.dye_info['expiration_date']}")
        self.expire_layout.addWidget(self.date_received)
        self.expire_layout.addWidget(self.expire_date)
        self.title_widget_layout.addLayout(self.expire_layout)
        
        self.layout.addWidget(self.title_widget)

        self.info_widget = QWidget()
        self.info_widget.setObjectName("infoWidget")
        self.info_widget_layout = QVBoxLayout(self.info_widget)
        self.info_widget.setAttribute(Qt.WA_StyledBackground, True)
        self.info_widget_layout.setSpacing(15)
        self.info_widget_layout.setContentsMargins(25, 25, 25, 25)

        self.description = QLabel(f"Description: {dye_info['description']}", alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter)
        self.info_widget_layout.addWidget(self.description)
        self.antigen_layout = QHBoxLayout()
        self.antigen = QLabel(f"Antigen: {dye_info['antigen']}")
        self.conjugation = QLabel(f"Conjugation: {dye_info['conjugation']}")
        self.antigen_layout.addWidget(self.antigen)
        self.antigen_layout.addWidget(self.conjugation)
        self.info_widget_layout.addLayout(self.antigen_layout)

        self.clone_layout = QHBoxLayout()
        self.clone = QLabel(f"Clone: {dye_info['clone']}")
        self.clonality = QLabel(f"Clonality: {dye_info['clonality']}")
        self.clone_layout.addWidget(self.clone)
        self.clone_layout.addWidget(self.clonality)
        self.info_widget_layout.addLayout(self.clone_layout)

        self.layout.addWidget(self.info_widget)
        
        shown = {"name", "id", "date_received", "expiration_date", "antigen", "conjugation", "clonality", "clone"}
        for key, value in dye_info.items():
            if key not in shown:
                self.layout.addWidget(QLabel(f"{key}: {value}"))
            
        self.confirm_button = QPushButton("Confirm and Close", self)
        self.confirm_button.setObjectName("confirmButton")
        self.confirm_button.clicked.connect(self.accept) 
        self.layout.addWidget(self.confirm_button)
            
        self.setStyleSheet(f"""
            QWidget#titleWidget, QWidget#infoWidget{{
                background: {constants.secondary_bg};
                border: 2px solid {constants.primary_accent};
                border-radius: 10px;
            }}
            
            QWidget#titleWidget QLabel#dyeName {{
                font-weight: bold;
                font-size: 32px;
            }}
            
            QWidget#titleWidget QLabel#dyeID {{
                font-weight: 600;
                font-size: 24px;
            }}
            
            QPushButton#confirmButton {{
                background: {constants.primary_accent};
                border-radius: 10px;
                font-size: 24px;
                font-weight: bold;
            }}
        """)