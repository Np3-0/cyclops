from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex

class DataTableModel(QAbstractTableModel):
    def __init__(self, rows, columns, parent=None):
        super().__init__(parent)
        self._rows = rows or []
        self._columns = columns

    def rowCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self._rows)

    def columnCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self._columns)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        value = self._rows[index.row()].get(self._columns[index.column()][1])
        return "" if value is None else str(value)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self._columns[section][0]
        return None