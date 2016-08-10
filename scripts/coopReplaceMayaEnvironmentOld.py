'''
@name:          coopReplaceMayaEnvironment.py
@repository:    https://github.com/studiocoop/maya
@version:       1.0
@license:       UNLICENCE
@author:        Santiago Montesdeoca [artineering.io]  

@summary:       replaces the existing Maya.env with a template which has to
                be in the same directory as this file and hides specified shelves

@requires:      -

@run:           MEL:     python("execfile('E:/coopReplaceMayaEnvironment.py')")
                PYTHON:  execfile('E:/coopReplaceMayaEnvironment.py')

@created:       8 Jul, 2015
@change:        10 Jul, 2015
'''
import os
import shutil
import inspect
import maya.mel as mel
import maya.cmds as cmds
    
#find environment directory
scriptsDir = os.path.abspath(cmds.internalVar(usd=True))
envDir = os.path.dirname(scriptsDir)

#hide unnecessary shelves
shelvesDict = { 'Dynamics'      : 'Dynamics.mel',
                'Fluids'        : 'Fluids.mel',
                'Fur'           : 'Fur.mel',
                'Muscle'        : 'Muscle.mel',
                'nCloth'        : 'NCloth.mel',
                'Subdivs'       : 'Subdivs.mel',
                'Toon'          : 'Toon.mel',
                'nHair'         : 'Hair.mel',
                'PaintEffects'  : 'PaintEffects.mel',
                'Sculpting'     : 'Sculpting.mel',
                'FX Caching'    : 'FXCaching.mel',
                'FX'            : 'FX.mel',
                'XGen'          : 'XGen.mel'
    }
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

#get environment file
envFile = os.path.join(envDir, 'Maya.env')
#find template environment file
thisFile = inspect.getframeinfo(inspect.currentframe()).filename
templateDir = os.path.dirname(os.path.abspath(thisFile))
templateFile = os.path.join(templateDir, 'Maya.env')
#copy and replace file
shutil.copy(templateFile, envFile)
cmds.headsUpMessage( '    MAYA EXPLOSION IN...    ')
cmds.pause(sec=3)
cmds.headsUpMessage( '    5    ')
cmds.pause(sec=1) 
cmds.headsUpMessage( '    4    ')
cmds.pause(sec=1) 
cmds.headsUpMessage( '    3    ')
cmds.pause(sec=1) 
cmds.headsUpMessage( '    2    ')
cmds.pause(sec=1) 
cmds.headsUpMessage( '    farewell world...    ')
cmds.pause(sec=1) 
#exit maya
cmds.quit(f=True)
#restarting right away doesn't work



