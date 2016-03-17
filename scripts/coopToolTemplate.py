from PySide import QtCore, QtGui
import userPrefs as prefs
import maya.cmds as cmds
import coopLib as lib
import coopQt as qt

''' MAIN
Template for a tool with UI in Pyside using studio.coop libraries '''
class yourTool():
    def __init__(self):
        window, existed = qt.createMayaWindow("Your awesome Tool", False, brand=prefs.companyName, tooltip='Information about your tool/brand')
        if not existed:
            print "UI does not exist"
            createLayout(window)
            createSignals(window)
            refresh(window)
            showUI()

def showUI():
    #this function shows your GUI
    cmds.showWindow("Your awesome Tool")

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
