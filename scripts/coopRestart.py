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

print __file__
mayaDir = os.path.join(os.path.dirname(sys.executable), 'maya')
platf = platform.system()
if platf == 'Windows':
    mayaDir += '.exe'
print mayaDir
print "Waiting for Maya to close..."
time.sleep(10)
sys.path.insert(0, os.path.dirname(__file__))
subprocess.Popen(mayaDir)
