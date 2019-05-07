from PyQt5.QtWidgets import QApplication
from sitdown.gui.mainwindow import MainAnotatorWindow, MutationsTableModel
from sitdown.readers import ABNAMROReader
from tests import RESOURCE_PATH
from tests.conftest import generate_mutation_sequence
import sys


def run_gui():

    # Get some mutations
    #mutations = generate_mutation_sequence(50)

    reader = ABNAMROReader()
    path = r"C:\Users\z428172\Documents\financien\2019\transacties\TXT190210094911.TAB"
    mutations = reader.read(path)

    app = QApplication(sys.argv)
    window = MainAnotatorWindow()

    model = MutationsTableModel(mutations)

    window.treeView.setModel(model)
    window.show()
    sys.exit(app.exec_())


run_gui()

