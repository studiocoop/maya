'''
@name:          animEnvironment.py
@repository:    https://github.com/studiocoop/maya
@version:       1.0
@license:       UNLICENCE
@authors:       Santiago Montesdeoca [artineering.io]

@summary:       Sets animation environment according to user preferences

@requires:      -

@run:           import animEnvironment.py
                animEnvironment.setHotkeys('default')
                || animEnvironment.setHotkeys('alt')
                || animEnvironment.resetHotkeys()

@created:       1 Jul, 2015
@change:        10 Jul, 2015
'''
import coopLib as lib
import maya.mel as mel
import maya.cmds as cmds

#this script may benefit from a userSettings file

hotkeyDict = {
        'default': [False,'o','a','g','t','t','s'],
        'alt': [True,'o','a','g','t','t','s'],
    }


def load():
    '''loads animation environment'''
    print "loading animation environment presets..."
    #set autoKey
    cmds.autoKeyframe( state=True )
    #set 24fps and playback on all viewports
    cmds.playbackOptions(ps=1.0, v='all')
    #set unlimited undo's
    cmds.undoInfo( state=True, infinity=True )
    #set manipulator sizes
    if lib.checkAboveVersion(2014):
        cmds.manipOptions( r=False, hs=55, ls=4, sph=1 )
    else:
        cmds.manipOptions( r=False, hs=55, ls=4 )
    #set framerate visibility
    mel.eval("setFrameRateVisibility(1);")
    #gimbal rotation
    cmds.manipRotateContext('Rotate', e=True, mode=2)
    #world translation
    cmds.manipMoveContext('Move', e=True, mode=2)
    
    #check if hotkeys have been set
    if (cmds.hotkey( 't', ctl=True, query=True, name = True)== 'CharacterAnimationEditorNameCommand'):
        print "Hotkeys have been previously loaded"
    else:
        setHotkeys('default')
    
    print "ENVIRONMENT SET\n", #the comma forces output on the status line


def setHotkeys(pref):
    '''set hotkeys according to pref dictionary'''
    #first reset
    resetHotkeys()
    hotkeys = hotkeyDict[pref]
    #outliner
    cmds.nameCommand( 'OutlinerWindowNameCommand', ann='OutlinerWindowNameCommand', c='OutlinerWindow')
    cmds.hotkey( k=hotkeys[1], alt=hotkeys[0], name='OutlinerWindowNameCommand', releaseName='')
    #attribute editor
    cmds.nameCommand( 'AttributeEditorNameCommand', ann='AttributeEditorNameCommand', c='AttributeEditor')
    cmds.hotkey( k=hotkeys[2], alt=hotkeys[0], name='AttributeEditorNameCommand', rn='')
    #graph editor
    cmds.nameCommand( 'GraphEditorNameCommand', ann='GraphEditorNameCommand', c='GraphEditor')
    cmds.hotkey( k=hotkeys[3], alt=hotkeys[0], name='GraphEditorNameCommand' )
    #tool settings
    cmds.nameCommand( 'ToolSettingsWindowNameCommand', ann='ToolSettingsWindowNameCommand', c='ToolSettingsWindow')
    cmds.hotkey( k=hotkeys[4], alt=hotkeys[0], name='ToolSettingsWindowNameCommand' )
    #trax editor
    cmds.nameCommand( 'CharacterAnimationEditorNameCommand', ann='CharacterAnimationEditorNameCommand', c='CharacterAnimationEditor')
    cmds.hotkey( k=hotkeys[5], ctl=True, name='CharacterAnimationEditorNameCommand' )
    #script editor
    cmds.nameCommand( 'ScriptEditorNameCommand', ann='ScriptEditorNameCommand', c='ScriptEditor')
    cmds.hotkey( k=hotkeys[6], alt=True, name='ScriptEditorNameCommand' )
    print pref + " hotkeys set (to change or reset hotkeys, right mouse click on the same shelf button\n",
    


def resetHotkeys():
    '''reset hotkeys'''
    #outliner
    cmds.hotkey( k='o', alt=False, name='PolyBrushMarkingMenuNameCommand', releaseName='PolyBrushMarkingMenuPopDownNameCommand')
    cmds.hotkey( k='o', alt=True, name='' )
    #attribute editor
    cmds.hotkey( k='a', alt=False, name='NameComFit_All_in_Active_Panel_MMenu', rn='NameComFit_All_in_Active_Panel_MMenu_release' )
    cmds.hotkey( k='a', alt=True, name='artisanToggleWireframe_press' )
    #graph editor
    cmds.hotkey( k='g', alt=False, name='NameComRepeat_Last_Menu_Action' )
    cmds.hotkey( k='g', alt=True, name='HyperGraph_IncreaseDepth' )
    #tool settings
    cmds.hotkey( k='t', alt=False, name='NameComShowManip_Tool' )
    cmds.hotkey( k='t', alt=True, name='HyperGraph_DecreaseDepth' )
    #trax editor
    cmds.hotkey( k='t', ctl=True, name='NameComUniversalManip' )
    #script editor
    cmds.hotkey( k='s', alt=True, name='NameCom_HIKSetFullBodyKey' )
    print "reverted to default maya hotkeys (to change or reset hotkeys, right mouse click on the same shelf button\n",

