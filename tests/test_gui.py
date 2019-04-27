from PyQt5.QtWidgets import QApplication

from sitdown.gui import Window, createMailModel


def test_gui(short_mutation_sequence):

    # Get some mutations
    mutations = short_mutation_sequence


    # Load into gui
    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.setSourceModel(createMailModel(window))
    window.show()
    sys.exit(app.exec_())





