import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget, QApplication
import constants
from gui_elements import MenuButton

class Background(QWidget):
    def __init__(self):
        super().__init__()
        self.title_text = QLabel("Inventory Management System", alignment=Qt.AlignTop | Qt.AlignHCenter)
        self.title_text.setObjectName("titleText")
        self.main_layout = QVBoxLayout(self)
        
        self.left_menu_panel = QWidget()
        self.left_menu_panel.setObjectName("leftMenuPanel")
        self.left_panel_layout = QVBoxLayout(self.left_menu_panel)
        self.left_panel_layout.setSpacing(15)
        self.left_panel_layout.setContentsMargins(25, 25, 25, 25)

        self.left_menu_dyes_button = MenuButton(["1.", "Input Dyes"])
        self.left_menu_dyes_button.clicked.connect(self.testButton)
        self.left_menu_camera_button = MenuButton(["2.", "Open Scanner"])
        self.left_menu_camera_button.clicked.connect(self.testButton)
        self.left_menu_results_button = MenuButton(["3.", "View Results"])
        self.left_menu_results_button.clicked.connect(self.testButton)

        self.left_panel_layout.addWidget(self.left_menu_dyes_button)
        self.left_panel_layout.addWidget(self.left_menu_camera_button)
        self.left_panel_layout.addWidget(self.left_menu_results_button)

        self.right_menu_panel = QWidget()
        self.right_menu_panel.setObjectName("rightMenuPanel")
        self.right_panel_layout = QVBoxLayout(self.right_menu_panel)
        
        self.right_menu_text = QLabel("Info", alignment=Qt.AlignTop | Qt.AlignHCenter)
        self.right_panel_layout.addWidget(self.right_menu_text)
        
        self.menu_layout = QHBoxLayout()
        
        self.menu_layout.addWidget(self.left_menu_panel, 1)
        self.menu_layout.addWidget(self.right_menu_panel, 3)        

        self.main_layout.addWidget(self.title_text, 0)
        self.main_layout.addLayout(self.menu_layout, 1)

    def testButton(self):
        print("TEST")
        
if __name__ == "__main__":
    app = QApplication([])

    widget = Background()
    widget.setWindowTitle("Inventory Management System")
    widget.resize(1080, 720)
    widget.setStyleSheet(f"""  
        QWidget {{
            background-color: {constants.primary_bg};
            color: #ffffff;
        }}
        QPushButton {{
            background-color: {constants.primary_accent};
            color: #ffffff;
        }}
        
        QLabel#titleText {{
            margin-top: 20px;
            font-size: 24px;
            font-weight: bold;
        }}
        
        QWidget#leftMenuPanel, QWidget#rightMenuPanel {{
            background-color: {constants.secondary_bg};
            border-radius: 10px;
        }}
        
        QWidget#leftMenuPanel QLabel, QWidget#rightMenuPanel QLabel {{
            font-size: 18px;
            font-weight: bold;
            margin-top: 10px;
        }}
        
        QLabel {{
            background: transparent;
        }}
        """)
    
    widget.show()
    

    sys.exit(app.exec())