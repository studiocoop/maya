import maya.cmds as cmds
import maya.utils

def openTool():
    window = cmds.window('Copymation Toolset', tb=False, s=False)

    #cmds.windowPref('Copymation_Toolset', ra=True)
    shelf = cmds.shelfLayout()

    button = cmds.shelfButton(annotation='Clone animation', image1='animCopymationClone.png', command='animCopymation.clone()', imageOverlayLabel='clone')

    cmds.shelfButton(annotation="Open advanced copy tool",
        image1="redo.png", command="", imageOverlayLabel="copy",
        overlayLabelColor=(1, 1, .25), overlayLabelBackColor=(.15, .9, .1, .4))

    cmds.shelfButton(annotation="Open animation cycler tool",
        image1="undo.png", command="", imageOverlayLabel="cycler",
        overlayLabelColor=(1, .25, .25))

    cmds.shelfButton(annotation="Close Copymation toolset",
        image1="close.png", command='maya.utils.executeDeferred("cmds.deleteUI(\'Copymation_Toolset\')")' , imageOverlayLabel="close",
        overlayLabelColor=(1, .25, .25))

    #resize toolset
    buttonH = cmds.shelfButton(button, q=True, h=True)
    buttonW = cmds.shelfButton(button, q=True, w=True)
    cmds.window(window, edit=True, widthHeight=(buttonW*4+10, buttonH+10))

    #show UI
    showUI()

def showUI():
    if cmds.window('Copymation_Toolset', ex=True):
        cmds.showWindow('Copymation_Toolset')
    else:
        openTool()

def clone():
    selected = cmds.ls(sl=True)
    source = selected.pop(0)
    cmds.copyKey(source, option="curve")
    for target in selected:
        cmds.pasteKey(target, option='replaceCompletely' )
    print "Keys copied successfully",
