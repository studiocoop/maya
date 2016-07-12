'''
@name:          coopRestart.py
@repository:    https://github.com/studiocoop/maya
@version:       1.0
@license:       UNLICENCE
@authors:       Santiago Montesdeoca [artineering.io]

@summary:       Script to restart maya after it has been closed

@requires:      coopLib

@run:           import coopLib as lib (suggested)
                lib.restartMaya(brute=False)

@created:       12 Jul, 2016
@change:        12 Jul, 2016
'''

import subprocess
import platform
import time
import sys
import os

mayaDir = os.path.join(os.path.dirname(sys.executable), 'maya')
platf = platform.system()
if platf == 'Windows':
    mayaDir += '.exe'
print mayaDir
print "Waiting for Maya to close..."
time.sleep(6)
subprocess.Popen(mayaDir)
