import sys
from PyQt5.QtWidgets import * #QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QPushButton, QAction, QLabel, QGridLayout
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import *
from PyQt5 import QtCore


class Part:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def getName(self):
        return self.name

    def getType(self):
        return self.type

    def setName(self, name):
        self.name = name

    def setType(self, type):
        self.type = type



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.width = 800
        self.height = 500

        self.setWindowTitle('OT2 GUI')
        self.setGeometry(0, 0, self.width, self.height)

        self.table_widget = TableWidget(self)
        self.table_widget.resize(self.width, self.height)
        self.setCentralWidget(self.table_widget)

        self.show()

    # def resizeEvent(self, event):
    #     print(self.geometry())
    #     QMainWindow.resizeEvent(self, event)



class TableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initializing Tabs
        self.tabs = QTabWidget()
        self.homeTab = QWidget()
        self.registryTab = QWidget()
        self.combinationTab = QWidget()
        self.finalTab = QWidget()

        # self.homeTab.resize(parent.geometry().width() - 22, parent.geometry().height() - 48)

        # Adding tabs
        self.tabs.addTab(self.homeTab, 'Home')
        self.tabs.addTab(self.registryTab, 'Registry')
        self.tabs.addTab(self.combinationTab, 'Combinations')
        self.tabs.addTab(self.finalTab, 'Final')

        # Creating widgets for Home tab
        self.homeTitle = QLabel('OT2 GUI Bullshit')
        self.registryButton = QPushButton('Go to Parts Registry')
        self.combosButton = QPushButton('Create Combination')

        # Connecting buttons
        self.registryButton.clicked.connect(self.on_registry_click)
        self.combosButton.clicked.connect(self.on_combos_click)


        # Creating Home Tab
        self.homeTab.layout = QVBoxLayout(self)
        self.homeTab.layout.addWidget(self.homeTitle)
        self.homeTab.layout.addWidget(self.registryButton)
        self.homeTab.layout.addWidget(self.combosButton)

        font = QFont()
        font.setPixelSize(50)
        font.setPointSize(50)
        font.setBold(True)

        self.homeTitle.setFont(font)
        self.homeTitle.setAlignment(QtCore.Qt.AlignCenter)

        self.homeTab.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.homeTab.setLayout(self.homeTab.layout)


        listofstuff = ['Protein', 'CDS', 'Promoter', 'Terminator', 'RBS']

        # Registry Tab

        self.registryTab.layout = QHBoxLayout(self)
        self.registryTab.leftWidget = QWidget()
        self.registryTab.rightWidget = QTreeWidget()

        self.registryTab.leftWidget.layout = QFormLayout()
        self.registryTab.leftWidget.partBox = QLineEdit()
        self.registryTab.leftWidget.layout.addRow(QLabel('Part Name'), self.registryTab.leftWidget.partBox)
        self.registryTab.leftWidget.dropdown = QComboBox()
        self.registryTab.leftWidget.dropdown.addItems(listofstuff)
        self.registryTab.leftWidget.layout.addRow(QLabel('Type'), self.registryTab.leftWidget.dropdown)

        self.registryTab.leftWidget.addButton = QPushButton('Add')
        self.registryTab.leftWidget.addButton.clicked.connect(self.on_add_click)
        self.registryTab.leftWidget.layout.addRow(self.registryTab.leftWidget.addButton)
        # self.registryTab.leftWidget.addButton.setAlignment(QtCore.Qt.AlignRight)

        self.registryTab.leftWidget.setLayout(self.registryTab.leftWidget.layout)

        labels = ['Part Name', 'Part Type']
        self.registryTab.rightWidget.setColumnCount(2)
        self.registryTab.rightWidget.setHeaderLabels(labels)

        columnWidth = self.registryTab.rightWidget.geometry().width() / 4
        self.registryTab.rightWidget.setColumnWidth(0, columnWidth)
        self.registryTab.rightWidget.setColumnWidth(1, columnWidth)



        self.registryTab.layout.addWidget(self.registryTab.leftWidget)
        self.registryTab.layout.addWidget(self.registryTab.rightWidget)
        self.registryTab.setLayout(self.registryTab.layout)






        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


    @pyqtSlot()
    def on_registry_click(self):
        self.tabs.setCurrentIndex(1)

    @pyqtSlot()
    def on_combos_click(self):
        self.tabs.setCurrentIndex(2)

    @pyqtSlot()
    def on_add_click(self):
        formText = self.registryTab.leftWidget.partBox.text()
        comboText = self.registryTab.leftWidget.dropdown.currentText()

        treeItem = QTreeWidgetItem()
        treeItem.setText(0, formText)
        treeItem.setText(1, comboText)
        self.registryTab.rightWidget.addTopLevelItem(treeItem)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    app.setStyle('Fusion')
    app.exec_()





# import sys
# from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout
# from PyQt5.QtGui import QIcon
# from PyQt5.QtCore import pyqtSlot
#
# class App(QMainWindow):
#
#     def __init__(self):
#         super().__init__()
#         self.title = 'PyQt5 tabs - pythonspot.com'
#         self.left = 0
#         self.top = 0
#         self.width = 300
#         self.height = 200
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)
#
#         self.table_widget = MyTableWidget(self)
#         self.setCentralWidget(self.table_widget)
#
#         self.show()
#
# class MyTableWidget(QWidget):
#
#     def __init__(self, parent):
#         super(QWidget, self).__init__(parent)
#         self.layout = QVBoxLayout(self)
#
#         # Initialize tab screen
#         self.tabs = QTabWidget()
#         self.tab1 = QWidget()
#         self.tab2 = QWidget()
#         self.tabs.resize(300,200)
#
#         # Add tabs
#         self.tabs.addTab(self.tab1,"Tab 1")
#         self.tabs.addTab(self.tab2,"Tab 2")
#
#         # Create first tab
#         self.tab1.layout = QVBoxLayout(self)
#         self.pushButton1 = QPushButton("PyQt5 button")
#         self.tab1.layout.addWidget(self.pushButton1)
#         self.tab1.setLayout(self.tab1.layout)
#
#         # Add tabs to widget
#         self.layout.addWidget(self.tabs)
#         self.setLayout(self.layout)
#
#     @pyqtSlot()
#     def on_click(self):
#         print("\n")
#         for currentQTableWidgetItem in self.tableWidget.selectedItems():
#             print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     app.setStyle('Fusion')
#     ex = App()
#     sys.exit(app.exec_())



# self.homeTitle = QLabel(self.homeTab)
# self.homeTitle.setText('OT2 GUI Bullshit')
#
# xCoord = self.homeTab.geometry().center().x() - (self.homeTitle.frameGeometry().width() / 2)
# yCoord = self.homeTab.geometry().center().y() - (self.homeTitle.frameGeometry().height() / 2)
#
# self.homeTitle.move(xCoord, yCoord)
#
#
# self.registryButton = QPushButton(self.homeTab)
# self.registryButton.setText('Go to Parts Registry')
# self.combosButton = QPushButton(self.homeTab)
# self.combosButton.setText('Create Combination')
#
# xCoordButton = self.homeTab.geometry().center().x() - (self.registryButton.geometry().width() / 2)
# yCoordButton = self.homeTab.geometry().center().y() - (self.registryButton.geometry().height() / 2)
#
# self.registryButton.move(xCoordButton, yCoordButton + 40)
# self.combosButton.move(xCoordButton, yCoordButton + 80)




#
# self.registryButton.setMinimumWidth(10)
# self.combosButton.setMinimumWidth(10)
#
#
#
# self.homeTab.layout.addWidget(self.homeTitle, 0, 0)
# self.homeTab.layout.addWidget(self.registryButton, 1, 2)
# self.homeTab.layout.addWidget(self.combosButton, 6, 5)

# print(self.geometry())

# self.homeTab.setLayout(self.homeTab.layout)


# def resizeEvent(self, event):
#     print(self.homeTab.frameGeometry())
#     xCoord = self.homeTab.geometry().center().x() - (self.homeTitle.frameGeometry().width() / 2)
#     yCoord = self.homeTab.geometry().center().y() - (self.homeTitle.frameGeometry().height() / 2)
#     self.homeTitle.move(xCoord, yCoord)
#     print(xCoord)
#     print(yCoord)
#
#     xCoordButton = self.homeTab.geometry().center().x() - (self.registryButton.geometry().width() / 2)
#     yCoordButton = self.homeTab.geometry().center().y() - (self.registryButton.geometry().height() / 2)
#
#     self.registryButton.move(xCoordButton, yCoordButton + 40)
#     self.combosButton.move(xCoordButton, yCoordButton + 80)
#
#     # self.homeTitle.move(self.frameGeometry().center().x() - ((self.homeTitle.frameGeometry().width()) / 2), self.frameGeometry().center().y() - (float(self.homeTitle.frameGeometry().height()) / 2) - 20)
#     QWidget.resizeEvent(self, event)
