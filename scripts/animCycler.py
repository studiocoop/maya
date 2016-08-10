from PySide import QtCore, QtGui
import userPrefs as prefs
import maya.cmds as cmds
import coopLib as lib
import coopQt as qt

''' MAIN '''
class animCycler():
    def __init__(self):
        window, existed = qt.createMayaWindow("Animation Cycler", False, brand=prefs.companyName, tooltip='Automatically copies and offsets selected animation to the other side of your character')
        if not existed:
            print "UI does not exist"
            createLayout(window)
            createSignals(window)
            refresh(window)
            showUI()

def showUI():
    #this function shows your GUI
    if cmds.window('Animation Cycler', ex=True):
        cmds.showWindow('Animation Cycler')
    else:
        animCycler()

''' SLOTS
Here you can insert all the functions of your tool'''
def refresh(w):
    # You can choose to refresh the GUI with new/custom values here
    print "refresh activated"

'''GUI
Here you create your UI'''
def createLayout(w):
    w.setGeometry(800, 400, 250, 300)

    # Your custom widgets come here
    w.attributeBox = QtGui.QGroupBox("Animation Cycler")
    w.attributeLayout = QtGui.QVBoxLayout()
    w.attributeBox.setLayout(w.attributeLayout)

    w.attributeDisplayWidget = QtGui.QWidget()
    w.attributeDisplayLayout = QtGui.QHBoxLayout()
    w.attributeDisplayWidget.setLayout(w.attributeDisplayLayout)
    w.showAll = QtGui.QCheckBox("Show all")
    w.reload = qt.iconButton("{0}/refreshing.png".format(iconDir), "Reload Attributes", [25,25])
    w.attributeDisplayLayout.addWidget(w.showAll)
    w.attributeDisplayLayout.addWidget(w.reload)
    w.attributeList = QtGui.QListWidget()
    w.attributeList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
    w.attributeList.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)
    w.clearSelection = QtGui.QPushButton("Clear selection")

    w.attributeLayout.addWidget(w.attributeDisplayWidget)
    w.attributeLayout.addWidget(w.attributeList)
    w.attributeLayout.addWidget(w.clearSelection)

    '''Options Box'''
    w.optionsWidget = QtGui.QWidget()
    w.optionsLayout = QtGui.QHBoxLayout()
    w.optionsWidget.setLayout(w.optionsLayout)

    w.inputField = QtGui.QLineEdit('')
    w.runButton = QtGui.QPushButton("Set Attributes")
    w.optionsLayout.addWidget(w.inputField)
    w.optionsLayout.addWidget(w.runButton)

    # Create main layout and add your widgets
    ''' Create the main layouts and add widgets '''
    w.mainLayout = QtGui.QVBoxLayout()
    w.setLayout(w.mainLayout)
    w.mainLayout.setContentsMargins(2, 2, 2, 2)
    w.mainLayout.addWidget(w.header) #w.header is the default studio.coop header
    #w.mainLayout.addWidget(yourWidget)
    w.mainLayout.addWidget(w.help) #w.help is the default studio.coop footer

''' SIGNALS
Here you connect your UI elements to the SLOTS defined earlier'''
def createSignals(w):
    # w.refreshBtn.clicked.connect(lambda: refresh(w))
    # most common Signals
    # button: clicked
    # check box: stateChanged
    # combo box: currentIndexChanged
