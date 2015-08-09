'''
@name:          coopReplaceMayaEnvironment.py
@repository:    https://github.com/studiocoop/maya
@version:       1.0
@license:       UNLICENCE
@author:        Santiago Montesdeoca [artineering.io]  

@summary:       replaces the existing Maya.env with a template which has to
                be in the same directory as this file

@requires:      -

@run:           MEL:     python("execfile('E:/coopReplaceMayaEnvironment.py')")
                PYTHON:  execfile('E:/coopReplaceMayaEnvironment.py')

@created:       8 Jul, 2015
@change:        10 Jul, 2015
'''
import os
import shutil
import inspect
import maya.cmds as cmds
    
#find environment directory
scriptsDir = os.path.abspath(cmds.internalVar(usd=True))
envDir = os.path.dirname(scriptsDir)
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
cmds.quit(force=True)
#restarting right away doesn't work
#mel.eval('savePrefs;')
#mayaDir = os.getcwd() 
#mayaPath = os.path.join(mayaDir, 'maya.exe')
#webbrowser.open_new(mayaPath)
#os.execl(sys.executable, sys.executable, * sys.argv)

