from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor
import constants

class DataTableModel(QAbstractTableModel):
    def __init__(self, rows, columns, parent=None):
        super().__init__(parent)
        self.rows = rows or []
        self.columns = columns
        self.highlighted_row = None
        
        self.highlight_color = QColor(constants.primary_accent)
        self.highlight_color.setAlpha(140)
    
    def set_highlight(self, row):
        self.highlighted_row = row
        if self.rows:
            self.dataChanged.emit(
                self.index(0, 0),
                self.index(self.rowCount() - 1, self.columnCount() - 1),
                [Qt.ItemDataRole.BackgroundRole]
            )

    def rowCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self.rows)

    def columnCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self.columns)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.BackgroundRole:
            if index.row() == self.highlighted_row:
                return self.highlight_color
            return None
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        value = self.rows[index.row()].get(self.columns[index.column()][1])
        return "" if value is None else str(value)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.columns[section][0]
        return None