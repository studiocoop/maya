from PySide import QtCore, QtGui
import userPrefs as prefs
import maya.cmds as cmds
import coopLib as lib
import coopQt as qt
reload(qt)

#globals
iconDir = qt.getCoopIconPath()

#utilities
def utilChannelBoxAttributes(source):
    attributes = cmds.listAttr(source, k=True)
    #extend non-keyable in channel box
    nonKeyable = cmds.listAttr(source, cb=True)
    if nonKeyable:
        attributes.extend(nonKeyable)
    return attributes

def utilRearrangeChannelBox():
    cmds.deleteAttr( 'mars', at='mr' )
    cmds.addAttr( ln='greenMen', sn='gm', at='double' )


def utilCopyAttributes():
    print "copying attributes"



def utilCloneChannelBox(sourceAttrs=''):
    selection = cmds.ls(sl=True)
    if len(selection)<2:
        cmds.error("Selection not valid. Please select at least 2 objects to clone")
    source = selection[0]
    targets = selection[1:]
    if not sourceAttrs:
        #cmds.select(source, r=True)
        sourceAttrs = utilChannelBoxAttributes(source)
    for target in targets:
        #cmds.select(source, r=True)
        targetAttrs = utilChannelBoxAttributes(source)
        for sourceAttr in sourceAttrs:
            if not cmds.objExists('{0}.{1}'.format(target, sourceAttr)):
                print sourceAttr
                attrLongName = cmds.attributeQuery( sourceAttr, node=source, ln=True)
                attrShortName = cmds.attributeQuery( sourceAttr, node=source, sn=True)
                attrType = cmds.attributeQuery( sourceAttr, node=source, attributeType=True)
                attrDefault = cmds.attributeQuery( sourceAttr, node=source, ld=True)
                if attrDefault:
                    attrDefault = attrDefault[0]
                attrKeyable = cmds.getAttr('{0}.{1}'.format(source,sourceAttr), k=True)
                print attrKeyable
                if attrType == 'double':
                    attrEnableMinValue = cmds.attributeQuery( sourceAttr, node=source, mne=True)
                    attrMinValue = ['']
                    if attrEnableMinValue:
                        attrMinValue = cmds.attributeQuery( sourceAttr, node=source, min=True)
                    attrEnableMaxValue = cmds.attributeQuery( sourceAttr, node=source, mxe=True)
                    attrMaxValue = ['']
                    if attrEnableMaxValue:
                        attrMaxValue = cmds.attributeQuery( sourceAttr, node=source, max=True)
                    # create 'double' attribute
                    if attrEnableMinValue and attrEnableMaxValue:
                        cmds.addAttr(target, ln=attrLongName, sn=attrShortName, at=attrType, k=attrKeyable, min=attrMinValue[0], max=attrMaxValue[0], dv=attrDefault)
                    elif attrMinValue[0]:
                        cmds.addAttr(target, ln=attrLongName, sn=attrShortName, at=attrType, k=attrKeyable, min=attrMinValue[0], dv=attrDefault)
                    else:
                        cmds.addAttr(target, ln=attrLongName, sn=attrShortName, at=attrType, k=attrKeyable, max=attrMaxValue[0], dv=attrDefault)
                    print "Added to {0}".format(target)

                elif attrType == 'enum':
                    attrEnum = cmds.attributeQuery( sourceAttr, node=source, le=True )
                    cmds.error("Enum type not developed yet. Please consider implementing this")
                else:
                    cmds.error("{0} type not developed yet. Please consider implementing this".format(attrType))

                #set visible for non-keyable on channel box
                if not cmds.getAttr('{0}.{1}'.format(target,sourceAttr), k=True):
                    cmds.setAttr('{0}.{1}'.format(target,sourceAttr), channelBox=True, e=True)
        cmds.select(selection, r=True)

'''
#GUI
'''
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
    refresh(w)

def refresh(w):
    selection = cmds.ls(sl=True)
    if not selection:
        cmds.warning("Cannot refresh attributes without a selection")
        return
    source = selection[0]
    cmds.select(source, r=True)
    #check attributes
    attributes = cmds.listAttr()
    if not w.showAll.isChecked():
        attributes = utilChannelBoxAttributes(source)
    if not attributes:
        cmds.error("No attributes found on selection")
    #clear attribute list
    w.attributeList.clear()
    #add attributes to list
    visibility = attributes.pop(0) #visibility
    for attribute in attributes:
        w.attributeList.addItem(attribute)
    w.attributeList.addItem(visibility)
    cmds.select(selection, r=True)
    print "Attributes refreshed",

def clearSel(w):
    w.attributeList.clearSelection()

def utilsChanged(w):
    option = w.utilBox.currentText()
    w.attributeBox.setTitle(option)
    if option=="Set Attributes":
        #update UI
        w.showAll.setEnabled(True)
        w.optionsLayout.insertWidget(0, w.inputField)
        w.runButton.setText("Set Attributes")
        w.attributeList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        w.attributeList.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)
        print option
    elif option=="Copy":
        #update UI
        w.showAll.setEnabled(True)
        w.optionsLayout.removeWidget(w.inputField)
        w.runButton.setText("Copy Attributes")
        w.attributeList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        w.attributeList.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)
        print option
    elif option=="Re-arrange":
        #update UI
        w.showAll.setChecked(False)
        w.showAll.setEnabled(False)
        w.optionsLayout.removeWidget(w.inputField)
        w.runButton.setText("Re-arrange channel box")
        w.attributeList.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        w.attributeList.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        print option
    elif option=="Clone Channel Box":
        #update UI
        w.showAll.setChecked(False)
        w.showAll.setEnabled(False)
        w.optionsLayout.removeWidget(w.inputField)
        w.runButton.setText("Clone attribute channels")
        w.attributeList.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        w.attributeList.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
    else:
        #update UI
        #Lock/Hide toggle
        w.showAll.setEnabled(True)
        w.optionsLayout.removeWidget(w.inputField)
        w.runButton.setText("Lock/Hide toggle")
        w.attributeList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        w.attributeList.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)
        print option

def utilsRun(w):
    option = w.utilBox.currentText()
    attributes = w.attributeList.selectedItems()
    if option=="Set Attributes":
        #cmds.attributeQuery
        #cmds.addAttr
        value = w.inputField.text()
        print option
    elif option=="Copy":
        utilCopyAttributes()
    elif option=="Clone Channel Box":
        utilCloneChannelBox() #TODO make the order relevant
        print "Channel Box Cloned",


'''GUI'''
def showUI():
    cmds.showWindow("Attr. Utils")

def createLayout(w):
    w.setGeometry(400, 400, 200, 500)

    '''Util Menu'''
    w.utilBox = QtGui.QComboBox()
    w.utilBox.addItems(['Set Attributes', 'Copy', 'Re-arrange', 'Clone Channel Box', 'Lock/Hide toggle'])

    '''Attribute Box'''
    w.attributeBox = QtGui.QGroupBox("")
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

    # Create main layout
    ''' Create the main layouts and add widgets '''
    w.mainLayout = QtGui.QVBoxLayout()
    w.setLayout(w.mainLayout)
    w.mainLayout.setContentsMargins(2, 2, 2, 2)
    w.mainLayout.addWidget(w.header)
    w.mainLayout.addWidget(w.utilBox)
    w.mainLayout.addWidget(w.attributeBox)
    w.mainLayout.addWidget(w.optionsWidget)
    w.mainLayout.addWidget(w.brand)

    # Create Connections
    ''' SIGNALS '''
    w.showAll.stateChanged.connect(lambda: showAll(w))
    w.reload.clicked.connect(lambda: refresh(w))
    w.runButton.clicked.connect(lambda: utilsRun(w))
    w.utilBox.currentIndexChanged.connect(lambda: utilsChanged(w))
    w.clearSelection.clicked.connect(lambda: clearSel(w))
