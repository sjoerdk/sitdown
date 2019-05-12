from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, QSortFilterProxyModel
from PyQt5.QtWidgets import QApplication, QTextEdit, QMainWindow, QAction, QTreeView, QVBoxLayout, QWidget, QLineEdit, \
    QLabel


class MainAnotatorWindow(QMainWindow):
    def __init__(self):
        super(MainAnotatorWindow, self).__init__()

        self.filterPatternLineEdit = QLineEdit()
        self.filterPatternLabel = QLabel("&Filter pattern:")
        self.filterPatternLabel.setBuddy(self.filterPatternLineEdit)

        self.mutationsListView = QTreeView()
        self.mutationsListView.setSortingEnabled(True)

        self.centralWidget = QWidget()
        self.centralLayout = QVBoxLayout()
        self.centralLayout.addWidget(self.filterPatternLineEdit)
        self.centralLayout.addWidget(self.mutationsListView)
        self.centralWidget.setLayout(self.centralLayout)
        self.setCentralWidget(self.centralWidget)

        self.testAction = QAction("Test", self, shortcut="Ctrl+T", triggered=self.test)

        self.createMenus()

        self.statusBar().showMessage("Ready")

    def test(self):
        print("Test!")

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.testAction)


class MutationsTableModel(QAbstractTableModel):
    """Shows a list of mutations """

    column_names = {
        0: "amount",
        1: "description",
        2: "balance_after",
        3: "date",
        4: "category",
        5: "opposite_account",
    }
    column_numbers = {y: x for x, y in column_names.items()}

    def __init__(self, mutations, parent=None):
        """

        Parameters
        ----------
        mutations: Set[Mutations]
        parent: Q
        """
        super(MutationsTableModel, self).__init__(parent)
        self.mutations = list(mutations)

    def rowCount(self, parent=QModelIndex()):
        return len(self.mutations)

    def columnCount(self, parent=QModelIndex()):
        return len(self.column_names)

    def data(self, index, role):
        if not index.isValid() or role != Qt.DisplayRole:
            return None

        row = index.row()
        column_name = self.column_names[index.column()]
        attr_name = column_name
        return QVariant(str(getattr(self.mutations[row], attr_name)))

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.column_names[section]
