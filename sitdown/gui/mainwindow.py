from PyQt5.QtWidgets import QApplication, QTextEdit, QMainWindow, QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        self.testAction = QAction("Test", self, shortcut="Ctrl+T", triggered=self.test)

        self.createMenus()

        self.statusBar().showMessage("Ready")

    def test(self):
        print('Test!')

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.testAction)



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

