from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QApplication

from sitdown.gui.mainwindow import MainWindow, MutationsTableModel


def test_gui(short_mutation_sequence):

    # Get some mutations
    mutations = short_mutation_sequence


    # Load into gui
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()

    model = QStandardItemModel(0, 2)

    model.setHeaderData(0, Qt.Horizontal, "amount")
    model.setHeaderData(1, Qt.Horizontal, "descrtiption")

    for mutation in mutations:
        model.insertRow(0)
        model.setData(model.index(0, 0), str(mutation.amount))
        model.setData(model.index(0, 1), mutation.description)

    model = MutationsTableModel(mutations)

    window.treeView.setModel(model)
    window.show()
    sys.exit(app.exec_())





