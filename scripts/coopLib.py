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
import maya.cmds as cmds

def checkAboveVersion(year):
    '''checks if Maya is above version $year'''
    mVersion = cmds.about(v=True)
    mVersion = int(mVersion.split()[0])
    if (mVersion > year):
        return True
    return False
    

def createEmptyNode(inputName):
    '''creates a completely empty node with $inputName'''
    cmds.select(cl=True)
    cmds.group( em=True, name=inputName )
    nodeName = cmds.ls(sl=True)
    keyableAttributes = cmds.listAttr(nodeName, k=True )
    for attribute in keyableAttributes:
        cmds.setAttr('{0}.{1}'.format(nodeName[0], attribute), l=True, k=False)
    

def restartMaya():
    '''force restart maya (make sure to save before calling this definition)'''
    os.execl(sys.executable, sys.executable, * sys.argv)


def getActiveModelPanel():
    '''gets the string of the active model editor panel (3D viewport returns none if none is active'''
    activePanel = cmds.getPanel(wf=True);
    if cmds.getPanel(typeOf=activePanel)=='modelPanel':
        return activePanel
    else:
        return None
    

def openUrl(url):
    '''opens url in browser'''
    import webbrowser
    webbrowser.open(url, new=2, autoraise=True)