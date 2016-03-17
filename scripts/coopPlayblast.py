'''
@name:          coopPlayblast.py
@repository:    https://github.com/studiocoop/maya
@version:       0.9
@license:       UNLICENCE
@authors:       Santiago Montesdeoca [artineering.io]

@summary:       playblasts animation with user settings

@requires:      -

@run:           import coopPlayblast
                coopPlayblast.playblast

@created:       15 Aug, 2015
@change:        15 Aug, 2015
'''
#import showSettings as ss
import os
import maya.cmds as cmds
import userPrefs as prefs
reload(prefs)
import coopModelEditorManager as editor

def playblast():
    #check if current scene is named
    fileName = cmds.file(q=True, sn=True, shn=True)
    if not fileName:
        fileName = "unnamed"
    else:
        fileName = os.path.splitext(fileName)[0]
    print "Playblast will be saved under the following filename: {0}".format(fileName)
    #get camera to playblast from scene
    cameraName = prefs.defaultCamera
    if not cmds.objExists(cameraName):
        cameraName = cmds.lookThru( q=True )
    cameraShape = cmds.listRelatives(cameraName, s=True)[0]
    cmds.camera(cameraShape, e=True, displaySafeTitle = prefs.safeTitle, displaySafeAction = prefs.safeAction, displayResolution = prefs.displayResolution)
    #playblast with user settings except ornaments
    editor.hideAllDisplayObjects()
    editor.showOnlyPlayblast()
    #wh=prefs.resolution,
    cmds.playblast(showOrnaments=prefs.HUD,  f=prefs.playblastDir+fileName, format=prefs.playblastFormat,
    w=prefs.resolution[0], h=prefs.resolution[1], percent=100, qlt=70, v=prefs.openFile, fo=prefs.overwrite, os=True)
    print "it reaches this stage"
    #editor.showOnlyAnim()
