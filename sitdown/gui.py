"""Graphical user interface for exploring and checking mutations and classifiers"""


from PyQt5.QtCore import (QDate, QDateTime, QRegExp, QSortFilterProxyModel, Qt,
        QTime)
from PyQt5.QtGui import QStandardItemModel, QKeySequence, QIcon
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
                             QGroupBox, QHBoxLayout, QLabel, QLineEdit, QTreeView, QVBoxLayout,
                             QWidget, QPushButton, QMenuBar, QAction, QStatusBar)


SUBJECT, SENDER, DATE = range(3)

# Work around the fact that QSortFilterProxyModel always filters datetime
# values in QtCore.Qt.ISODate format, but the tree views display using
# QtCore.Qt.DefaultLocaleShortDate format.
class SortFilterProxyModel(QSortFilterProxyModel):
    def filterAcceptsRow(self, sourceRow, sourceParent):
        # Do we filter for the date column?
        if self.filterKeyColumn() == DATE:
            # Fetch datetime value.
            index = self.sourceModel().index(sourceRow, DATE, sourceParent)
            data = self.sourceModel().data(index)

            # Return, if regExp match in displayed format.
            return (self.filterRegExp().indexIn(data.toString(Qt.DefaultLocaleShortDate)) >= 0)

        # Not our business.
        return super(SortFilterProxyModel, self).filterAcceptsRow(sourceRow, sourceParent)


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.proxyModel = SortFilterProxyModel()
        self.proxyModel.setDynamicSortFilter(True)


        self.proxyGroupBox = QGroupBox("")

        self.sourceView = QTreeView()
        self.sourceView.setRootIsDecorated(False)
        self.sourceView.setAlternatingRowColors(True)

        self.proxyView = QTreeView()
        self.proxyView.setRootIsDecorated(False)
        self.proxyView.setAlternatingRowColors(True)
        self.proxyView.setModel(self.proxyModel)
        self.proxyView.setSortingEnabled(True)

        self.sortCaseSensitivityCheckBox = QCheckBox("Case sensitive sorting")
        self.filterCaseSensitivityCheckBox = QCheckBox("Case sensitive filter")

        self.filterPatternLineEdit = QLineEdit()
        self.filterPatternLabel = QLabel("&Filter pattern:")
        self.filterPatternLabel.setBuddy(self.filterPatternLineEdit)

        self.filterSyntaxComboBox = QComboBox()
        self.filterSyntaxComboBox.addItem("Regular expression", QRegExp.RegExp)
        self.filterSyntaxComboBox.addItem("Wildcard", QRegExp.Wildcard)
        self.filterSyntaxComboBox.addItem("Fixed string", QRegExp.FixedString)
        self.filterSyntaxLabel = QLabel("Filter &syntax:")
        self.filterSyntaxLabel.setBuddy(self.filterSyntaxComboBox)

        self.filterColumnComboBox = QComboBox()
        self.filterColumnComboBox.addItem("Subject")
        self.filterColumnComboBox.addItem("Sender")
        self.filterColumnComboBox.addItem("Date")
        self.filterColumnLabel = QLabel("Filter &column:")
        self.filterColumnLabel.setBuddy(self.filterColumnComboBox)

        self.filterPatternLineEdit.textChanged.connect(self.filterRegExpChanged)
        self.filterSyntaxComboBox.currentIndexChanged.connect(self.filterRegExpChanged)
        self.filterColumnComboBox.currentIndexChanged.connect(self.filterColumnChanged)
        self.filterCaseSensitivityCheckBox.toggled.connect(self.filterRegExpChanged)
        self.sortCaseSensitivityCheckBox.toggled.connect(self.sortChanged)



        proxyLayout = QGridLayout()

        #proxyLayout.addWidget(self.filterPatternLabel, 1, 2)
        proxyLayout.addWidget(self.filterPatternLineEdit, 1, 2)
        proxyLayout.addWidget(self.proxyView, 2, 2)
        #proxyLayout.addWidget(self.filterSyntaxLabel, 2, 0)
        #proxyLayout.addWidget(self.filterSyntaxComboBox, 2, 1, 1, 2)
        #proxyLayout.addWidget(self.filterColumnLabel, 3, 0)
        #proxyLayout.addWidget(self.filterColumnComboBox, 3, 1, 1, 2)
        #proxyLayout.addWidget(self.filterCaseSensitivityCheckBox, 4, 0, 1, 2)
        #proxyLayout.addWidget(self.sortCaseSensitivityCheckBox, 4, 2)
        self.proxyGroupBox.setLayout(proxyLayout)


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
        mainLayout.addWidget(self.proxyGroupBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Basic Sort/Filter Model")
        self.resize(500, 450)

        self.proxyView.sortByColumn(SENDER, Qt.AscendingOrder)
        self.filterColumnComboBox.setCurrentIndex(SENDER)

        self.filterPatternLineEdit.setText("Andy|Grace")
        self.filterCaseSensitivityCheckBox.setChecked(True)
        self.sortCaseSensitivityCheckBox.setChecked(True)

    def open_mutation_set(self):
        print("Opening a thing!")

    def save_mutation_set(self):
        print("Saving a thing!")

    def setSourceModel(self, model):
        self.proxyModel.setSourceModel(model)
        self.sourceView.setModel(model)

    def filterRegExpChanged(self):
        syntax_nr = self.filterSyntaxComboBox.itemData(self.filterSyntaxComboBox.currentIndex())
        syntax = QRegExp.PatternSyntax(syntax_nr)

        if self.filterCaseSensitivityCheckBox.isChecked():
            caseSensitivity = Qt.CaseSensitive
        else:
            caseSensitivity = Qt.CaseInsensitive

        regExp = QRegExp(self.filterPatternLineEdit.text(),
                caseSensitivity, syntax)
        self.proxyModel.setFilterRegExp(regExp)

    def filterColumnChanged(self):
        self.proxyModel.setFilterKeyColumn(self.filterColumnComboBox.currentIndex())

    def sortChanged(self):
        if self.sortCaseSensitivityCheckBox.isChecked():
            caseSensitivity = Qt.CaseSensitive
        else:
            caseSensitivity = Qt.CaseInsensitive

        self.proxyModel.setSortCaseSensitivity(caseSensitivity)


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
