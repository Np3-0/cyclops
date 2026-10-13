from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget 
import constants

class MenuButton(QWidget):
    clicked = Signal()
    def __init__(self, text, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.layoutA = QHBoxLayout(self)
        self.layoutA.setContentsMargins(15, 20, 15, 25)

        self.numberIcon = QLabel(text[0], self)
        self.numberIcon.setObjectName("numberIcon")
        self.numberIcon.setFixedSize(30, 30)
        self.numberIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layoutA.addWidget(self.numberIcon)

        self.label = QLabel(text[1], self)
        self.layoutA.addWidget(self.label, 1)

        self.setStyleSheet(f"""
            MenuButton {{
                background-color: {constants.primary_bg};
                border: 2px solid {constants.primary_accent};
                border-radius: 10px;
                max-height: 100px;
            }}

            QLabel#numberIcon {{
                margin: 0px;
                padding: 0px;
                border-radius: 15px;
                border: 2px solid {constants.primary_accent};
                color: {constants.primary_accent};
                font-weight: bold;
                background: transparent;
            }}
        """)

        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pass
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(event.position().toPoint()):
            self.clicked.emit()
        super().mouseReleaseEvent(event)