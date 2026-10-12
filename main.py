import sys
from PySide6 import QtCore, QtWidgets, QtGui

# color palette: 
primary_bg = "#0b1220"
secondary_bg = "#111a2e"
primary_accent = "#6052d4"

class Background(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.title_text = QtWidgets.QLabel("Inventory Management System", alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.title_text.setObjectName("titleText")
        self.main_layout = QtWidgets.QVBoxLayout(self)
        
        self.left_menu_panel = QtWidgets.QWidget()
        self.left_menu_panel.setObjectName("leftMenuPanel")
        self.left_panel_layout = QtWidgets.QVBoxLayout(self.left_menu_panel)

        self.left_menu_text = QtWidgets.QLabel("Steps", alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.left_panel_layout.addWidget(self.left_menu_text)
        
        self.right_menu_panel = QtWidgets.QWidget()
        self.right_menu_panel.setObjectName("rightMenuPanel")
        self.right_panel_layout = QtWidgets.QVBoxLayout(self.right_menu_panel)
        
        self.right_menu_text = QtWidgets.QLabel("Info", alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.right_panel_layout.addWidget(self.right_menu_text)
        
        self.menu_layout = QtWidgets.QHBoxLayout()
                
        self.menu_layout.addWidget(self.left_menu_panel, 1)
        self.menu_layout.addWidget(self.right_menu_panel, 3)        

        self.main_layout.addWidget(self.title_text, 0)
        self.main_layout.addLayout(self.menu_layout, 1)
        


        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Background()
    widget.setWindowTitle("Inventory Management System")
    widget.resize(1080, 720)
    widget.setStyleSheet(f"""  
        QWidget {{
            background-color: {primary_bg};
            color: #ffffff;
        }}
        QPushButton {{
            background-color: {primary_accent};
            color: #ffffff;
        }}
        
        QLabel#titleText {{
            margin-top: 20px;
            font-size: 24px;
            font-weight: bold;
        }}
        
        QWidget#leftMenuPanel, QWidget#rightMenuPanel {{
            background-color: {secondary_bg};
            margin: 10px;
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