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
        
        self.dye_name = QLabel(f"{self.fmt(self.dye_info['marker'])} - {self.fmt(self.dye_info['dye'])}", alignment=Qt.AlignTop | Qt.AlignHCenter)
        self.dye_name.setObjectName("dyeName")
        self.title_widget_layout.addWidget(self.dye_name)
        
        self.dye_id = QLabel(f"ID: {self.fmt(self.dye_info['itemId'])}", alignment=Qt.AlignTop | Qt.AlignHCenter)
        self.dye_id.setObjectName("dyeID")
        self.title_widget_layout.addWidget(self.dye_id)
        
        self.expire_layout = QHBoxLayout()
        self.date_received = QLabel(f"Date Received: {self.fmt(self.dye_info['dateReceived'], date=True)}")
        self.expire_date = QLabel(f"Expiration Date: {self.fmt(self.dye_info['expirationDate'], date=True)}")
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

        self.address_layout = QHBoxLayout()
        self.box = QLabel(f"Box: {self.fmt(dye_info['box'])}")
        self.address = QLabel(f"Address: {self.fmt(dye_info['address'])}")
        self.address_layout.addWidget(self.box)
        self.address_layout.addWidget(self.address)
        self.info_widget_layout.addLayout(self.address_layout)

        self.other_layout = QHBoxLayout()
        self.price = QLabel(f"Price: ${self.fmt(dye_info['price'])}")
        self.volume = QLabel(f"Volume (μl): {self.fmt(dye_info['volumeUl'])}")
        self.other_layout.addWidget(self.price)
        self.other_layout.addWidget(self.volume)
        self.info_widget_layout.addLayout(self.other_layout)

        self.clone_layout = QHBoxLayout()
        self.clone = QLabel(f"Clone: {self.fmt(dye_info['clone'])}")
        self.clonality = QLabel(f"Clonality: {self.fmt(dye_info['clonality'])}")
        self.clone_layout.addWidget(self.clone)
        self.clone_layout.addWidget(self.clonality)
        self.info_widget_layout.addLayout(self.clone_layout)
        
        self.raised_info = QHBoxLayout()
        self.raised = QLabel(f"Raised In: {self.fmt(dye_info['raisedIn'])}")
        self.recognizes = QLabel(f"Recognizes: {self.fmt(dye_info['recognizes'])}")
        self.raised_info.addWidget(self.raised)
        self.raised_info.addWidget(self.recognizes)
        self.info_widget_layout.addLayout(self.raised_info)
        
        self.stainMethod = QLabel(f"Stain Method: {self.fmt(dye_info['stainingMethod'])}", alignment=Qt.AlignmentFlag.AlignHCenter)
        self.info_widget_layout.addWidget(self.stainMethod)

        self.layout.addWidget(self.info_widget)
            
        self.confirm_button = QPushButton("Confirm and Close", self)
        self.confirm_button.setObjectName("confirmButton")
        self.confirm_button.clicked.connect(self.accept) 
        self.layout.addWidget(self.confirm_button)
            
        self.setStyleSheet(f"""
            QWidget#titleWidget, QWidget#infoWidget{{
                background: {constants.secondary_bg};
                border: 2px solid {constants.primary_accent};
                border-radius: 10px;
                margin-bottom: 20px;
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
                margin-top: 25px;
            }}
        """)
    def fmt(self, value, date=False):
        if value is None or value == "":
            return "N/A"
        return str(value)[:10] if date else str(value)