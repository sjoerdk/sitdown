"""Graphical user interface for exploring and checking mutations and classifiers"""


from PyQt5.QtCore import (QDate, QDateTime, QRegExp, QSortFilterProxyModel, Qt,
        QTime)
from PyQt5.QtGui import QStandardItemModel, QKeySequence, QIcon
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
                             QGroupBox, QHBoxLayout, QLabel, QLineEdit, QTreeView, QVBoxLayout,
                             QWidget, QPushButton, QMenuBar, QAction, QStatusBar, QTreeView)

SUBJECT, SENDER, DATE = range(3)


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.mutationsModel = QSortFilterProxyModel()
        self.mutationsModel.setDynamicSortFilter(True)

        self.mutationsGroupBox = QGroupBox("")

        self.mutationsView = QTreeView()
        self.mutationsView.setRootIsDecorated(False)
        self.mutationsView.setAlternatingRowColors(True)
        self.mutationsView.setModel(self.mutationsModel)
        self.mutationsView.setSortingEnabled(True)

        self.filterPatternLineEdit = QLineEdit()
        self.filterPatternLabel = QLabel("&Filter pattern:")
        self.filterPatternLabel.setBuddy(self.filterPatternLineEdit)

        self.filterPatternLineEdit.textChanged.connect(self.filterRegExpChanged)

        self.labelView = QTreeView()
        self.labelView.setModel()

        proxyLayout = QGridLayout()
        proxyLayout.addWidget(self.filterPatternLineEdit, 1, 2)
        proxyLayout.addWidget(self.mutationsView, 2, 2)
        proxyLayout.addWidget(self.labelView, 0, 0, 3, 1)
        self.mutationsGroupBox.setLayout(proxyLayout)

        self.mutationsModel.setFilterKeyColumn(SUBJECT)

        self.statusBar = QStatusBar()
        self.menuBar = QMenuBar()
        from sitdown import GUI_RESOURCE_PATH

        self.openAct = QAction(QIcon(str(GUI_RESOURCE_PATH / "open.png")), "&Open...",
                               self, shortcut=QKeySequence.Open,
                               statusTip="Open mutations", triggered=self.open_mutation_set)
        self.saveAct = QAction(QIcon(str(GUI_RESOURCE_PATH / "save.png")), "&Save...",
                               self, shortcut=QKeySequence.Save,
                               statusTip="Save mutations", triggered=self.save_mutation_set)
        self.fileMenu = self.menuBar.addMenu("&File")
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)

        self.menuItemLayout = QGroupBox("Horizontal layout")
        self.openFileNameButton = QPushButton("QFileDialog.get&OpenFileName()")
        layout = QHBoxLayout(self.openFileNameButton)
        self.menuItemLayout.setLayout(layout)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.menuBar)
        mainLayout.addWidget(self.mutationsGroupBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Basic Sort/Filter Model")
        self.resize(500, 450)

        self.mutationsView.sortByColumn(SENDER, Qt.AscendingOrder)

        self.filterPatternLineEdit.setText("")

    def open_mutation_set(self):
        print("Opening a thing!")

    def save_mutation_set(self):
        print("Saving a thing!")

    def setSourceModel(self, model):
        self.mutationsModel.setSourceModel(model)

    def filterRegExpChanged(self):
        regExp = QRegExp(self.filterPatternLineEdit.text(),
                Qt.CaseInsensitive, QRegExp.RegExp)
        self.mutationsModel.setFilterRegExp(regExp)

    def sortChanged(self):
        if self.sortCaseSensitivityCheckBox.isChecked():
            caseSensitivity = Qt.CaseSensitive
        else:
            caseSensitivity = Qt.CaseInsensitive

        self.mutationsModel.setSortCaseSensitivity(caseSensitivity)


def addMail(model, subject, sender, date):
    model.insertRow(0)
    model.setData(model.index(0, SUBJECT), subject)
    model.setData(model.index(0, SENDER), sender)
    model.setData(model.index(0, DATE), date)


def createMailModel(parent):
    model = QStandardItemModel(0, 3, parent)

    model.setHeaderData(SUBJECT, Qt.Horizontal, "Subject")
    model.setHeaderData(SENDER, Qt.Horizontal, "Sender")
    model.setHeaderData(DATE, Qt.Horizontal, "Date")

    addMail(model, "Happy New Year!", "Grace K. <grace@software-inc.com>",
            QDateTime(QDate(2006, 12, 31), QTime(17, 3)))
    addMail(model, "Radically new concept", "Grace K. <grace@software-inc.com>",
            QDateTime(QDate(2006, 12, 22), QTime(9, 44)))
    addMail(model, "Accounts", "pascale@nospam.com",
            QDateTime(QDate(2006, 12, 31), QTime(12, 50)))
    addMail(model, "Expenses", "Joe Bloggs <joe@bloggs.com>",
            QDateTime(QDate(2006, 12, 25), QTime(11, 39)))
    addMail(model, "Re: Expenses", "Andy <andy@nospam.com>",
            QDateTime(QDate(2007, 1, 2), QTime(16, 5)))
    addMail(model, "Re: Accounts", "Joe Bloggs <joe@bloggs.com>",
            QDateTime(QDate(2007, 1, 3), QTime(14, 18)))
    addMail(model, "Re: Accounts", "Andy <andy@nospam.com>",
            QDateTime(QDate(2007, 1, 3), QTime(14, 26)))
    addMail(model, "Sports", "Linda Smith <linda.smith@nospam.com>",
            QDateTime(QDate(2007, 1, 5), QTime(11, 33)))
    addMail(model, "AW: Sports", "Rolf Newschweinstein <rolfn@nospam.com>",
            QDateTime(QDate(2007, 1, 5), QTime(12, 0)))
    addMail(model, "RE: Sports", "Petra Schmidt <petras@nospam.com>",
            QDateTime(QDate(2007, 1, 5), QTime(12, 1)))

    return model
