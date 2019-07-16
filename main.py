import sys
from PyQt5.QtWidgets import * #QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QPushButton, QTreeWidget  QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QPushButton, QAction, QLabel, QGridLayout
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import *
from PyQt5 import QtCore
import partstore

ps = partstore.PartStore()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.width = 800
        self.height = 500

        self.setWindowTitle('LASSO')
        self.setGeometry(0, 0, self.width, self.height)

        self.table_widget = TableWidget(self)
        self.table_widget.resize(self.width, self.height)
        self.setCentralWidget(self.table_widget)

        self.show()


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

        # Adding tabs
        self.tabs.addTab(self.homeTab, 'Home')
        self.tabs.addTab(self.registryTab, 'Registry')
        self.tabs.addTab(self.combinationTab, 'Combinations')
        self.tabs.addTab(self.finalTab, 'Final')

        # Creating widgets for Home tab
        self.homeTitle = QLabel('LASSO')
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

        listofstuff = ['CDS', 'Insulator', 'Promoter', 'Terminator']
        # Promoter, Terminator, CDS, Insulator,

        """
        Registry Tab
        """
        self.registryTab.layout = QHBoxLayout(self.registryTab)
        self.registryTab.leftWidget = QWidget()
        self.registryTab.rightWidget = QTreeWidget()

        partsArray = ps.loadJSON('registry.json')
        self.partNameArray = []
        for currpart in partsArray:
            partName = currpart.getName()
            self.partNameArray.append(partName)
            typeName = currpart.getType()
            volumeName = currpart.getVolume()

            treeItem = QTreeWidgetItem()
            treeItem.setText(0, partName)
            treeItem.setText(1, typeName)
            treeItem.setText(2, volumeName)

            self.registryTab.rightWidget.addTopLevelItem(treeItem)

        self.registryTab.leftWidget.layout = QFormLayout()
        self.registryTab.leftWidget.partBox = QLineEdit()
        self.registryTab.leftWidget.layout.addRow(QLabel('Part Name'), self.registryTab.leftWidget.partBox)
        self.registryTab.leftWidget.dropdown = QComboBox()
        self.registryTab.leftWidget.dropdown.addItems(listofstuff)
        self.registryTab.leftWidget.layout.addRow(QLabel('Type'), self.registryTab.leftWidget.dropdown)

        self.registryTab.leftWidget.volumeBox = QLineEdit()
        self.registryTab.leftWidget.layout.addRow(QLabel('Volume (µL)'), self.registryTab.leftWidget.volumeBox)

        self.registryTab.leftWidget.addButton = QPushButton('Add')
        self.registryTab.leftWidget.addButton.clicked.connect(self.on_add_click)
        self.registryTab.leftWidget.layout.addRow(self.registryTab.leftWidget.addButton)
        # self.registryTab.leftWidget.addButton.setAlignment(QtCore.Qt.AlignRight)

        self.registryTab.leftWidget.setLayout(self.registryTab.leftWidget.layout)

        labels = ['Part Name', 'Part Type', 'Volume']
        self.registryTab.rightWidget.setColumnCount(3)
        self.registryTab.rightWidget.setHeaderLabels(labels)

        columnWidth = self.registryTab.rightWidget.geometry().width() / 6
        self.registryTab.rightWidget.setColumnWidth(0, columnWidth)
        self.registryTab.rightWidget.setColumnWidth(1, columnWidth)
        self.registryTab.rightWidget.setColumnWidth(2, columnWidth)



        self.registryTab.layout.addWidget(self.registryTab.leftWidget)
        self.registryTab.layout.addWidget(self.registryTab.rightWidget)
        self.registryTab.setLayout(self.registryTab.layout)


        """
        Combination Tab
        """
        self.wellNumber = 1
        self.combosDictionary = {}

        self.combinationTab.topLayout = QVBoxLayout(self.combinationTab)
        self.combinationTab.topWidget = QWidget()

        self.combinationTab.layout = QHBoxLayout(self.combinationTab.topWidget)
        self.combinationTab.leftWidget = QWidget()
        self.combinationTab.rightWidget = QWidget()

        self.combinationTab.pictureWidget = QLabel()
        sbolImage = QPixmap('testimage.png')
        self.combinationTab.pictureWidget.setPixmap(sbolImage)
        self.combinationTab.pictureWidget.resize(sbolImage.width(),sbolImage.height())

        self.combinationTab.toggleButtons = QWidget()
        self.combinationTab.toggleButtons.layout = QHBoxLayout(self.combinationTab.toggleButtons)
        self.combinationTab.toggleButtons.backButton = QPushButton('Back')
        self.combinationTab.toggleButtons.nextButton = QPushButton('Next')
        self.combinationTab.toggleButtons.finalButton = QPushButton('Final')
        self.combinationTab.toggleButtons.finalButton.setStyleSheet('background-color: #e58f24')

        self.combinationTab.toggleButtons.backButton.clicked.connect(self.on_back_click)
        self.combinationTab.toggleButtons.nextButton.clicked.connect(self.on_next_click)
        self.combinationTab.toggleButtons.finalButton.clicked.connect(self.on_final_click)

        self.combinationTab.toggleButtons.layout.addWidget(self.combinationTab.toggleButtons.backButton)
        self.combinationTab.toggleButtons.layout.addWidget(self.combinationTab.toggleButtons.nextButton)
        self.combinationTab.toggleButtons.layout.addWidget(self.combinationTab.toggleButtons.finalButton)


        self.combinationTab.leftWidget.layout = QFormLayout()
        self.combinationTab.rightWidget.layout = QVBoxLayout()

        sizePolicy = QSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        self.combinationTab.leftWidget.setSizePolicy(sizePolicy)
        self.combinationTab.rightWidget.setSizePolicy(sizePolicy)

        self.combinationTab.leftWidget.partBox = QLineEdit()
        self.combinationTab.leftWidget.wellLabel = QLabel('Well #' + str(self.wellNumber))
        self.combinationTab.leftWidget.layout.addRow(self.combinationTab.leftWidget.wellLabel)
        self.combinationTab.leftWidget.dropdown = QComboBox()

        self.combinationTab.leftWidget.dropdown.addItems(self.partNameArray)

        self.combinationTab.leftWidget.layout.addRow(QLabel('Part Name'), self.combinationTab.leftWidget.dropdown)

        self.combinationTab.leftWidget.addButton = QPushButton('Add Part')
        self.combinationTab.leftWidget.addButton.clicked.connect(self.on_add_part_click)
        self.combinationTab.leftWidget.layout.addRow(self.combinationTab.leftWidget.addButton)

        self.combinationTab.leftWidget.setLayout(self.combinationTab.leftWidget.layout)

        self.combinationTab.rightWidget.label = QLabel('Parts Combination')
        self.combinationTab.rightWidget.listWidget = QListWidget()

        font = QFont()
        font.setPixelSize(14)
        font.setPointSize(14)
        font.setBold(True)

        self.combinationTab.rightWidget.label.setFont(font)
        self.combinationTab.rightWidget.label.setAlignment(QtCore.Qt.AlignCenter)
        self.combinationTab.leftWidget.wellLabel.setFont(font)

        self.combinationTab.rightWidget.layout.addWidget(self.combinationTab.rightWidget.label)
        self.combinationTab.rightWidget.layout.addWidget(self.combinationTab.rightWidget.listWidget)

        self.combinationTab.rightWidget.setLayout(self.combinationTab.rightWidget.layout)

        self.combinationTab.layout.addWidget(self.combinationTab.leftWidget, stretch = 0)
        self.combinationTab.layout.addWidget(self.combinationTab.rightWidget, stretch = 0)


        self.combinationTab.topLayout.addWidget(self.combinationTab.topWidget)
        self.combinationTab.topLayout.addWidget(self.combinationTab.pictureWidget)
        self.combinationTab.topLayout.addWidget(self.combinationTab.toggleButtons)

        self.combinationTab.topWidget.setLayout(self.combinationTab.layout)

        self.combinationTab.setLayout(self.combinationTab.topLayout)

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
        volumeText = self.registryTab.leftWidget.volumeBox.text()

        self.partNameArray.append(formText)
        self.combinationTab.leftWidget.dropdown.addItem(formText)

        treeItem = QTreeWidgetItem()
        treeItem.setText(0, formText)
        treeItem.setText(1, comboText)
        treeItem.setText(2, volumeText)
        self.registryTab.rightWidget.addTopLevelItem(treeItem)

        ps.addPart(formText, comboText, volumeText)
        ps.saveJSON('registry.json')

    @pyqtSlot()
    def on_add_part_click(self):
        if self.wellNumber not in self.combosDictionary:
            self.combosDictionary[self.wellNumber] = []

        if len(self.combosDictionary[self.wellNumber]) == 10:
            return

        nextPart =  self.combinationTab.leftWidget.dropdown.currentText()
        part = ps.findPart(nextPart)

        comboPartList = self.combosDictionary[self.wellNumber]
        comboPartList.append(nextPart)

        self.combinationTab.rightWidget.listWidget.addItem(str(len(comboPartList)) + '. '
                                                + nextPart + ' (' + part.getType() + ')')

    @pyqtSlot()
    def on_next_click(self):
        if self.wellNumber == 96:
            return

        self.wellNumber += 1
        self.combinationTab.rightWidget.listWidget.clear()
        if self.wellNumber in self.combosDictionary:
            comboPartList = self.combosDictionary[self.wellNumber]
            for index, item in enumerate(comboPartList):
                part = ps.findPart(item)
                self.combinationTab.rightWidget.listWidget.addItem(str(index + 1) + '. '
                                                        + item + ' (' + part.getType() + ')')

        font = QFont()
        font.setPixelSize(14)
        font.setPointSize(14)
        font.setBold(True)

        self.combinationTab.leftWidget.wellLabel = QLabel('Well #' + str(self.wellNumber))
        self.combinationTab.leftWidget.wellLabel.setFont(font)
        self.combinationTab.leftWidget.layout.removeRow(0)
        self.combinationTab.leftWidget.layout.insertRow(0, self.combinationTab.leftWidget.wellLabel)
        self.combinationTab.leftWidget.setLayout(self.combinationTab.leftWidget.layout)

    @pyqtSlot()
    def on_back_click(self):
        if self.wellNumber == 1:
            return

        self.wellNumber -= 1
        self.combinationTab.rightWidget.listWidget.clear()
        if self.wellNumber in self.combosDictionary:
            comboPartList = self.combosDictionary[self.wellNumber]
            for index, item in enumerate(comboPartList):
                part = ps.findPart(item)
                self.combinationTab.rightWidget.listWidget.addItem(str(index + 1) + '. '
                                                        + item + ' (' + part.getType() + ')')

        font = QFont()
        font.setPixelSize(14)
        font.setPointSize(14)
        font.setBold(True)

        self.combinationTab.leftWidget.wellLabel = QLabel('Well #' + str(self.wellNumber))
        self.combinationTab.leftWidget.wellLabel.setFont(font)
        self.combinationTab.leftWidget.layout.removeRow(0)
        self.combinationTab.leftWidget.layout.insertRow(0, self.combinationTab.leftWidget.wellLabel)
        self.combinationTab.leftWidget.setLayout(self.combinationTab.leftWidget.layout)

    @pyqtSlot()
    def on_final_click(self):
        self.tabs.setCurrentIndex(3)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Backspace:
            if self.tabs.currentIndex() == 1 and self.registryTab.rightWidget.topLevelItemCount() != 0:
                treeParent = self.registryTab.rightWidget.invisibleRootItem()
                for item in self.registryTab.rightWidget.selectedItems():
                    treeParent.removeChild(item)
                    name = item.text(0)
                    type = item.text(1)
                    volume = item.text(2)
                    ps.removePart(name,type,volume)
                    ps.saveJSON('registry.json')
            elif self.tabs.currentIndex() == 2 and self.combinationTab.rightWidget.listWidget.count() != 0:
                comboPartList = self.combosDictionary[self.wellNumber]
                row = self.combinationTab.rightWidget.listWidget.currentRow()
                item = self.combinationTab.rightWidget.listWidget.takeItem(row)
                del comboPartList[row]

                #self.combinationTab.rightWidget.listWidget.clear()

                for index, item in enumerate(comboPartList):
                    listWidgetItem = self.combinationTab.rightWidget.listWidget.item(index)
                    listWidgetItemText = listWidgetItem.text().split('.')[1]
                    listWidgetItem.setText(str(index + 1) + '.' + listWidgetItemText)
                    #part = ps.findPart(item)
                    #self.combinationTab.rightWidget.listWidget.addItem(str(index + 1) + '. '
                                                            #+ item + ' (' + part.getType() + ')')

                print(self.combosDictionary)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    app.setStyle('Fusion')
    app.exec_()
