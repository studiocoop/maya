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
import maya.cmds as cmds
import coopModelEditorManager as man

def playblast():
    #playblast with user settings except ornaments
    man.hideAllDisplayObjects()
    man.showOnlyPlayblast()
    cmds.playblast(showOrnaments=0)
    man.showOnlyAnim()