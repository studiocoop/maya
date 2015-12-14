'''
@name:          coopLib.py
@repository:    https://github.com/studiocoop/maya
@version:       0.*
@license:       UNLICENCE
@authors:       Santiago Montesdeoca [artineering.io]

@summary:       Maya coop python library

@requires:      -

@run:           import coopLib as lib (suggested)

@created:       05 May, 2015
@change:        08 Aug, 2015
'''
import os
import sys
import maya.mel as mel
import maya.cmds as cmds
######################################################################################
#GENERAL UTILITIES
######################################################################################
def checkAboveVersion(year):
    '''checks if Maya is above version $year'''
    mVersion = cmds.about(v=True)
    mVersion = int(mVersion.split()[0])
    if (mVersion > year):
        return True
    return False

def getEnvDir():
    '''returns environment dir'''
    scriptsDir = os.path.abspath(cmds.internalVar(usd=True))
    return os.path.dirname(scriptsDir)
    
def openUrl(url):
    '''opens url in browser'''
    import webbrowser
    webbrowser.open(url, new=2, autoraise=True)
    
def restartMaya():
    '''force restart maya (make sure to save before calling this definition)'''
    os.execl(sys.executable, sys.executable, * sys.argv)
   
def restartDialog():
    restart = cmds.confirmDialog( title='Restart Maya', 
                message='Maya needs to be restarted in order to show changes\n\nWould you like to restart maya?\n(REMEMBER TO SAVE)',
                button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No', ma='center' )
    if restart == 'Yes':
        restartMaya()


######################################################################################
#MAYA UTILITIES
######################################################################################
def createEmptyNode(inputName):
    '''creates a completely empty node with $inputName'''
    cmds.select(cl=True)
    cmds.group( em=True, name=inputName )
    nodeName = cmds.ls(sl=True)
    keyableAttributes = cmds.listAttr(nodeName, k=True )
    for attribute in keyableAttributes:
        cmds.setAttr('{0}.{1}'.format(nodeName[0], attribute), l=True, k=False)
        
        
def deleteShelf():
    if cmds.shelfLayout('CurvesSurfaces', q=True, ex=True):
        cmds.deleteUI('CurvesSurfaces', layout=True)


def getActiveModelPanel():
    '''gets the string of the active model editor panel (3D viewport returns none if none is active'''
    activePanel = cmds.getPanel(wf=True);
    if cmds.getPanel(typeOf=activePanel)=='modelPanel':
        return activePanel
    else:
        return None


def deleteShelves(shelvesDict=None):
    '''delete shelves
    $shelves: dictionary of shelf name and mel file without prefix
    e.g. {"Animation" : "Animation.mel"}'''
    envDir = getEnvDir()
    if not shelvesDict:
        cmds.error('No shelf array given')
    #Maya creates all default shelves in prefs only after each has been opened (initialized)
    for shelf in shelvesDict:
        try:
            mel.eval('jumpToNamedShelf("{0}");'.format(shelf))
        except:
            continue
    mel.eval('saveAllShelves $gShelfTopLevel;') #all shelves loaded (save them)
    #time to delete them
    shelfTopLevel = mel.eval('$tempMelVar=$gShelfTopLevel') + '|'
    for shelf in shelvesDict:
        shelfLayout = shelvesDict[shelf].split('.mel')[0]
        if cmds.shelfLayout(shelfTopLevel + shelfLayout, q=True, ex=True):
            cmds.deleteUI(shelfTopLevel+shelfLayout, layout=True)
    #mark them as deleted to avoid startup loading
    shelfDir = os.path.join(envDir,'prefs','shelves')
    for shelf in shelvesDict:
        shelfName = os.path.join(shelfDir,'shelf_' + shelvesDict[shelf])
        deletedShelfName = shelfName + '.deleted'
        if os.path.isfile(shelfName):
            #make sure the deleted file doesn't already exist
            if os.path.isfile(deletedShelfName):
                os.remove(shelfName)
                continue
            os.rename(shelfName,deletedShelfName)
    restartDialog()


def restoreShelves():
    '''restore deleted shelves'''
    scriptsDir = os.path.abspath(cmds.internalVar(usd=True))
    envDir = os.path.dirname(scriptsDir)
    shelfDir = os.path.join(envDir,'prefs','shelves')
    for shelf in os.listdir(shelfDir):
        if shelf.endswith('.deleted'):
            restoredShelf = os.path.join(shelfDir, shelf.split('.deleted')[0])
            deletedShelf = os.path.join(shelfDir, shelf)
            #check if it has not been somehow restored
            if os.path.isfile(restoredShelf):
                os.remove(deletedShelf)
            else:
                os.rename(deletedShelf, restoredShelf)
    restartDialog()


######################################################################################
#PYSIDE UTILITIES
######################################################################################
#Convert .ui file to .py file
def uiToPy(path):
    from pysideuic import compileUi
    pyfile = open(path, 'w')
    compileUi("[path to input ui file]\makeCube.ui", pyfile, False, 4,False)
    pyfile.close()
