import sys
import csv
from PyQt5.QtWidgets import * #QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QPushButton, QTreeWidget  QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QPushButton, QAction, QLabel, QGridLayout
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import *
from PyQt5 import QtCore
import partstore

import os

CURRENTDIR = os.path.dirname(os.path.abspath(__file__))
IMAGESDIR = os.path.join(CURRENTDIR, 'images')
sys.path.insert(0, IMAGESDIR)

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
        self.homePicture = QLabel()
        image = QImage(os.path.join(IMAGESDIR, 'cowboyhat.png'))
        self.homePicture.setPixmap(QPixmap.fromImage(image))

        self.homeTitle = QLabel('LASSO')
        self.registryButton = QPushButton('Go to Parts Registry')
        self.combosButton = QPushButton('Create Combination')

        # Connecting buttons
        self.registryButton.clicked.connect(self.on_registry_click)
        self.combosButton.clicked.connect(self.on_combos_click)

        # Creating Home Tab
        self.homeTab.layout = QVBoxLayout(self)
        self.homeTab.layout.addWidget(self.homePicture)
        self.homeTab.layout.addWidget(self.homeTitle)
        self.homeTab.layout.addWidget(self.registryButton)
        self.homeTab.layout.addWidget(self.combosButton)

        font = QFont()
        font.setPixelSize(50)
        font.setPointSize(50)
        font.setBold(True)

        self.homePicture.setAlignment(QtCore.Qt.AlignCenter)

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
            self.partNameArray.append(partName + ' (' + currpart.getType() + ')')
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

        self.registryTab.rightWidget.setSortingEnabled(True)
        self.registryTab.rightWidget.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.registryTab.rightWidget.sortByColumn(1, QtCore.Qt.AscendingOrder)


        self.registryTab.layout.addWidget(self.registryTab.leftWidget)
        self.registryTab.layout.addWidget(self.registryTab.rightWidget)
        self.registryTab.setLayout(self.registryTab.layout)


        """
        Combination Tab
        """
        self.wellNumber = 1
        self.combosDictionary = {}
        self.imageDictionary = {}

        self.combinationTab.topLayout = QVBoxLayout(self.combinationTab)
        self.combinationTab.topWidget = QWidget()

        self.combinationTab.layout = QHBoxLayout(self.combinationTab.topWidget)
        self.combinationTab.leftWidget = QWidget()
        self.combinationTab.rightWidget = QWidget()

        self.combinationTab.pictureWidget = QLabel()
        self.sbolLine = QImage(os.path.join(IMAGESDIR, 'bigblackline.png'))
        self.combinationTab.pictureWidget.setPixmap(QPixmap.fromImage(self.sbolLine))
        self.combinationTab.pictureWidget.resize(self.sbolLine.width(),self.sbolLine.height())

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

        """
        Final Tab
        """
        self.finalTab.widget = QWidget()
        self.finalTab.layout = QHBoxLayout()

        self.finalTab.leftWidget = QWidget()
        self.finalTab.leftWidget.layout = QVBoxLayout()
        self.finalTab.leftWidget.label = QLabel('Input Plate')
        self.finalTab.leftWidget.label.setAlignment(QtCore.Qt.AlignCenter)
        self.finalTab.leftWidget.table = QTableWidget(12, 8, self.finalTab.leftWidget)

        # leftHeader = self.finalTab.leftWidget.table.horizontalHeader()
        #leftHeader.setSectionResizeMode(0,QHeaderView.ResizeToContents)

        self.finalTab.leftWidget.layout.addWidget(self.finalTab.leftWidget.label)
        self.finalTab.leftWidget.layout.addWidget(self.finalTab.leftWidget.table)
        self.finalTab.leftWidget.setLayout(self.finalTab.leftWidget.layout)


        self.finalTab.rightWidget = QWidget()
        self.finalTab.rightWidget.layout = QVBoxLayout()
        self.finalTab.rightWidget.label = QLabel('Output Plate')
        self.finalTab.rightWidget.label.setAlignment(QtCore.Qt.AlignCenter)
        self.finalTab.rightWidget.table = QTableWidget(12, 8, self.finalTab.rightWidget)

        self.finalTab.rightWidget.layout.addWidget(self.finalTab.rightWidget.label)
        self.finalTab.rightWidget.layout.addWidget(self.finalTab.rightWidget.table)
        self.finalTab.rightWidget.setLayout(self.finalTab.rightWidget.layout)

        self.finalTab.layout.addWidget(self.finalTab.leftWidget)
        self.finalTab.layout.addWidget(self.finalTab.rightWidget)
        self.finalTab.setLayout(self.finalTab.layout)










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
        if formText == '':
            return
        if ps.findPart(formText) is not None:
            return
        comboText = self.registryTab.leftWidget.dropdown.currentText()
        volumeText = self.registryTab.leftWidget.volumeBox.text()
        if volumeText.isnumeric() is False or volumeText == '':
            return

        treeItem = QTreeWidgetItem()
        treeItem.setText(0, formText)
        treeItem.setText(1, comboText)
        treeItem.setText(2, volumeText)
        self.registryTab.rightWidget.addTopLevelItem(treeItem)

        ps.addPart(formText, comboText, volumeText)
        ps.saveJSON('registry.json')

        self.partNameArray = ps.generatePartList()
        self.combinationTab.leftWidget.dropdown.clear()
        self.combinationTab.leftWidget.dropdown.addItems(self.partNameArray)

        self.registryTab.rightWidget.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.registryTab.rightWidget.sortByColumn(1, QtCore.Qt.AscendingOrder)

    @pyqtSlot()
    def on_add_part_click(self):
        if self.wellNumber not in self.combosDictionary:
            self.combosDictionary[self.wellNumber] = []
            self.imageDictionary[self.wellNumber] = []


        if len(self.combosDictionary[self.wellNumber]) == 10 or len(self.partNameArray) == 0:
            return

        nextPart =  self.combinationTab.leftWidget.dropdown.currentText().split('(')[0].strip()
        part = ps.findPart(nextPart)

        comboPartList = self.combosDictionary[self.wellNumber]
        comboPartList.append(nextPart)

        self.combinationTab.rightWidget.listWidget.addItem(str(len(comboPartList)) + '. '
                                                + nextPart + ' (' + part.getType() + ')')

        #creating the images
        typeImage = part.getType()
        imageName = typeImage.lower() + '.png'
        numParts = len(self.combosDictionary[self.wellNumber])
        distanceLeft = 100 + 60*(numParts - 1)
        sbolImage = QImage(imageName)
        self.imageDrawer(imageName, distanceLeft, sbolImage)
        self.combinationTab.pictureWidget.setPixmap(QPixmap.fromImage(self.sbolLine))

        self.imageDictionary[self.wellNumber].append(imageName)

    @pyqtSlot()
    def on_next_click(self):
        if self.wellNumber == 96:
            return
        if self.wellNumber not in self.combosDictionary or len(self.combosDictionary[self.wellNumber]) == 0:
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

        self.sbolLine = QImage('bigblackline.png')
        self.combinationTab.pictureWidget.setPixmap(QPixmap.fromImage(self.sbolLine))
        if self.wellNumber in self.combosDictionary:
            imagesList = self.imageDictionary[self.wellNumber]
            partNumber = 0
            for imageName in imagesList:
                distanceLeft = 100 + 60*(partNumber)
                sbolImage = QImage(imageName)
                self.imageDrawer(imageName, distanceLeft, sbolImage)
                partNumber += 1
                self.combinationTab.pictureWidget.setPixmap(QPixmap.fromImage(self.sbolLine))




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

        self.sbolLine = QImage('bigblackline.png')
        self.combinationTab.pictureWidget.setPixmap(QPixmap.fromImage(self.sbolLine))
        if self.wellNumber in self.combosDictionary:
            imagesList = self.imageDictionary[self.wellNumber]
            partNumber = 0
            for imageName in imagesList:
                distanceLeft = 100 + 60*(partNumber)
                sbolImage = QImage(imageName)
                self.imageDrawer(imageName, distanceLeft, sbolImage)
                partNumber += 1
                self.combinationTab.pictureWidget.setPixmap(QPixmap.fromImage(self.sbolLine))



    @pyqtSlot()
    def on_final_click(self):
        self.tabs.setCurrentIndex(3)

        #creating CSV files

        with open('combinations.csv', 'w', newline = '') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for key in range(1, len(self.combosDictionary) + 1):
                partArray = self.combosDictionary[key].copy()
                partArray.insert(0, 'Combination_' + str(key))
                writer.writerow(partArray)

        with open('input_plate_map.csv', 'w', newline = '') as csv_file:
            partArray = []
            for key in range(1, len(self.combosDictionary) + 1):
                partNameArray = self.combosDictionary[key].copy()
                for partName in partNameArray:
                    partArray.append(ps.findPart(partName))
            partArray.sort()
            writer = csv.writer(csv_file, delimiter=',')
            inputList = []
            counter = 1
            for index, input in enumerate(partArray):
                if input.getName() not in inputList:
                    inputList.append(input.getName())
                    counter += 1

                if counter == 13 or index == len(partArray) - 1:
                    writer.writerow(inputList)
                    inputList = []
                    counter = 1

        with open('output_plate_map.csv', 'w', newline = '') as csv_file:
            numCombosArray = []
            writer = csv.writer(csv_file, delimiter=',')
            numCombos = len(self.combosDictionary)
            counter = 1
            inputList = []
            for i in range(1,numCombos+1):
                numCombosArray.append('Combination_' + str(i))
            for index, input in enumerate(numCombosArray):
                counter += 1
                inputList.append(input)
                if counter == 13 or index == len(numCombosArray) - 1:
                    writer.writerow(inputList)
                    inputList = []
                    counter = 1

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Backspace:
            if self.tabs.currentIndex() == 1 and self.registryTab.rightWidget.topLevelItemCount() != 0:
                treeParent = self.registryTab.rightWidget.invisibleRootItem()
                for item in self.registryTab.rightWidget.selectedItems():
                    treeParent.removeChild(item)
                    name = item.text(0)
                    Type = item.text(1)
                    volume = item.text(2)
                    ps.removePart(name,Type,volume)
                    ps.saveJSON('registry.json')
                    self.partNameArray.remove(name + ' (' + Type + ')')
                    self.combinationTab.leftWidget.dropdown.clear()
                    self.combinationTab.leftWidget.dropdown.addItems(self.partNameArray)
            elif self.tabs.currentIndex() == 2 and self.combinationTab.rightWidget.listWidget.count() != 0:
                comboPartList = self.combosDictionary[self.wellNumber]
                imagesList = self.imageDictionary[self.wellNumber]
                row = self.combinationTab.rightWidget.listWidget.currentRow()
                item = self.combinationTab.rightWidget.listWidget.takeItem(row)
                del comboPartList[row]
                del imagesList[row]

                for index, item in enumerate(comboPartList):
                    listWidgetItem = self.combinationTab.rightWidget.listWidget.item(index)
                    listWidgetItemText = listWidgetItem.text().split('.')[1]
                    listWidgetItem.setText(str(index + 1) + '.' + listWidgetItemText)

                self.sbolLine = QImage('bigblackline.png')
                self.combinationTab.pictureWidget.setPixmap(QPixmap.fromImage(self.sbolLine))
                # painter = QPainter()
                partNumber = 0
                for imageName in imagesList:
                    distanceLeft = 100 + 60*(partNumber)
                    sbolImage = QImage(imageName)
                    self.imageDrawer(imageName, distanceLeft, sbolImage)
                    partNumber += 1
                    self.combinationTab.pictureWidget.setPixmap(QPixmap.fromImage(self.sbolLine))

    def imageDrawer(self, imageName, distanceLeft, sbolImage):
        painter = QPainter()
        painter.begin(self.sbolLine)
        if imageName == 'cds.png':
            painter.drawImage(self.combinationTab.pictureWidget.rect().left() + distanceLeft, self.combinationTab.pictureWidget.rect().center().y() - 18, sbolImage)
        elif imageName == 'insulator.png':
            painter.drawImage(self.combinationTab.pictureWidget.rect().left() + distanceLeft, self.combinationTab.pictureWidget.rect().center().y() - 45, sbolImage)
        elif imageName == 'promoter.png':
            painter.drawImage(self.combinationTab.pictureWidget.rect().left() + distanceLeft, self.combinationTab.pictureWidget.rect().center().y() - 55, sbolImage)
        elif imageName == 'terminator.png':
             painter.drawImage(self.combinationTab.pictureWidget.rect().left() + distanceLeft, self.combinationTab.pictureWidget.rect().center().y() - 48, sbolImage)
        painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    app.setStyle('Fusion')
    app.exec_()
