"""
@name:      coopSetup
@version:   1.0
@author:    Santiago Montesdeoca [artineering.io]

@summary:   This files sets up the coopUtilities in any machine, regarding of OS

@requires:  coopLib, coopQt, coopRestart, userPrefs

@run:       import coopQt as cqt (suggested)

@created:   14 Jul, 2016
@change:    08 Aug, 2016
"""
import userPrefs as prefs
import maya.cmds as cmds
import maya.mel as mel
import coopLib as lib
import subprocess
import shutil
import sys
import os


def run(root):
    """
    Change Maya.env, run user prefs and restart Maya

    :param root: Root directory of system
    """
    print "-> Installing {0} Utilities".format(prefs.companyName)

    # update maya.env
    mayaEnvFileDir = cmds.about(env=True, q=True)
    # adapt separator character to OS
    sep = ':'
    if cmds.about(nt=True, q=True):
        sep = ';'
    # keep track of existing data
    variables = {'MAYA_SHELF_PATH':[os.path.abspath(os.path.join(root, "shelves")),False],
    'MAYA_SCRIPT_PATH':[os.path.abspath(os.path.join(root, "scripts")),False],
    'PYTHONPATH':[os.path.abspath(os.path.join(root, "scripts")),False],
    'MAYA_PLUG_IN_PATH':[os.path.abspath(os.path.join(root, "plugins")),False],
    'XBMLANGPATH':[os.path.abspath(os.path.join(root, "icons")),False]
    }

    # create temporary file and populate directories
    tempFileDir = os.path.join(os.path.dirname(mayaEnvFileDir),"maya.tmp")
    with open(mayaEnvFileDir, 'rb') as f:
        for line in f:
            line = line.replace(" ", "") #get rid of whitespaces
            #get rid of new lines
            line = line.replace("\n", "")
            line = line.replace("\r", "")
            #check for shelf directory as it needs to go first in Maya.env
            if not variables['MAYA_SHELF_PATH'][1]:
                if 'MAYA_SHELF_PATH' not in line:
                    outLine = 'MAYA_SHELF_PATH={0};'.format(variables['MAYA_SHELF_PATH'][0])
                    with open (tempFileDir, 'ab') as tmp:
                        tmp.write(outLine+"\n")
                    variables['MAYA_SHELF_PATH'][1] = True #mark as found
            #let the fun begin
            outLine = line
            equation = line.split('=')
            variable = equation[0]
            # if variable is found in line
            if variable in variables:
                if len(equation)>1:
                    values = equation[1]
                    #if directory not found within existing variable
                    if variables[variable][0] not in values:
                        if values[-1]==sep or values[-2]==sep:
                            outLine = line+variables[variable][0]+sep
                        else:
                            outLine = line+sep+variables[variable][0]+sep
                    variables[variable][1] = True #mark as found
            #write line in temp file
            with open (tempFileDir, 'ab') as tmp:
                tmp.write(outLine+"\n")
    # check that all variables have been found and append missing ones
    appendix = ''
    #if no lines are in Maya.env, shelf still needs to be inserted first
    if not variables['MAYA_SHELF_PATH'][1]:
        appendix += 'MAYA_SHELF_PATH={0};\n'.format(variables['MAYA_SHELF_PATH'][0])
        variables['MAYA_SHELF_PATH'][1] = True #mark as found
    #append the rest of the missing variables
    for key in variables:
        if not variables[key][1]:
            appendix += "{0}={1};\n".format(key, variables[key][0])
    with open(tempFileDir, 'a') as tmp:
        tmp.write(appendix)

    #replace environment file
    shutil.move(tempFileDir, mayaEnvFileDir)

    #custom setups depending on desired utils
    prefs.setup()

    print "{0} Utilities Installed.".format(prefs.companyName),
    # restart maya
    cmds.confirmDialog( title='Restart Maya',
                message='\nPlease restart Maya to show all changes',
                icn='warning', button='OK', ma='center' )

    #Pythonpath is not loaded after automatic restart as of Maya 2017
    #lib.restartDialog(brute=False)
