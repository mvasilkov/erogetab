'Debug settings'

import platform

from .base import *

DEBUG = True

SECRET_KEY = 'potato'


# Other settings

if platform.system() == 'Windows':
    NPM_EXECUTABLE_PATH = r'C:\Program Files\nodejs\node_modules\npm\bin\npm.cmd'
