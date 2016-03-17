from PySide import QtCore, QtGui
import userPrefs as prefs
import maya.cmds as cmds
import coopLib as lib
import coopQt as qt

class attrUtils():
    def __init__(self):
        window, existed = qt.createMayaWindow("Attr. Utils", False, prefs.companyName, 'Attribute utilities')
        if not existed:
            print "UI does not exist"
            createLayout(window)
            refresh(window)
            showUI()

''' SLOTS '''
def showAll(w):
    if w.showAll.isChecked():
        print "showAll is checked"
    else:
        print "unchecked"

def refresh(w):
    attributes = cmds.listAttr(k=True)
    attributes.extend(cmds.listAttr(cb=True))
    print attributes
    for attribute in attributes:
        w.attributeList.insertItem(0, attribute)

def utilsChanged(w):
    option = w.utilBox.currentText()
    if option=="SET ATTRS":
        print option
    elif option=="COPY":
        print option
    elif option=="CLONE CBOX":
        print option

def utilsRun(w):
    option = w.utilBox.currentText()
    attributes = w.attributeList.selectedItems()
    if option=="SET ATTRS":
        #cmds.attributeQuery
        #cmds.addAttr
        value = w.inputField.text()
        print option
    elif option=="COPY":
        print option
    elif option=="CLONE CBOX":
        print option


'''GUI'''
def showUI():
    cmds.showWindow("Attr. Utils")

def createLayout(w):
    w.setGeometry(800, 400, 250, 300)

    '''Util Menu'''
    w.utilBox = QtGui.QComboBox()
    w.utilBox.addItems(['SET ATTRS', 'COPY', 'RE-ARRANGE', 'CLONE CBOX', 'LOCK/HIDE'])

    '''Attribute Box'''
    w.attributeBox = QtGui.QGroupBox("Change Attributes")
    w.attributeLayout = QtGui.QVBoxLayout()
    w.attributeBox.setLayout(w.attributeLayout)

    w.attributeDisplayWidget = QtGui.QWidget()
    w.attributeDisplayLayout = QtGui.QHBoxLayout()
    w.attributeDisplayWidget.setLayout(w.attributeDisplayLayout)
    w.showAll = QtGui.QCheckBox("show all")
    w.reload = qt.iconButton("refresh.png", "Reload Attributes", [50,50])
    w.attributeDisplayLayout.addWidget(w.showAll)
    w.attributeDisplayLayout.addWidget(w.reload)
    w.attributeList = QtGui.QListWidget()

    w.attributeLayout.addWidget(w.attributeDisplayWidget)
    w.attributeLayout.addWidget(w.attributeList)

    '''Options Box'''
    w.optionsWidget = QtGui.QWidget()
    w.optionsLayout = QtGui.QHBoxLayout()
    w.optionsWidget.setLayout(w.optionsLayout)

    w.inputField = QtGui.QLineEdit('')
    w.runButton = QtGui.QPushButton("Set Attr")
    w.optionsLayout.addWidget(w.inputField)
    w.optionsLayout.addWidget(w.runButton)

    # Create main layout
    ''' Create the main layouts and add widgets '''
    w.mainLayout = QtGui.QVBoxLayout()
    w.setLayout(w.mainLayout)
    w.mainLayout.setContentsMargins(2, 2, 2, 2)
    w.mainLayout.addWidget(w.header)
    w.mainLayout.addWidget(w.utilBox)
    w.mainLayout.addWidget(w.attributeBox)
    w.mainLayout.addWidget(w.optionsWidget)
    w.mainLayout.addWidget(w.help)

    # Create Connections
    ''' SIGNALS '''
    w.showAll.stateChanged.connect(lambda: showAll(w))
    w.reload.clicked.connect(lambda: refresh(w))
    w.runButton.clicked.connect(lambda: utilsRun(w))
    w.utilBox.currentIndexChanged.connect(lambda: utilsChanged(w))
