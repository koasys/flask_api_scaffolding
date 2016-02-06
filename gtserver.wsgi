activate_this = '/home/admin/PYENV/gtserver/ENV/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

# put server.py into python path.
import sys
sys.path.insert(0, '/home/admin/PYENV/gtserver/')

from gt_app import app as application