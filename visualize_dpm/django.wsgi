import os
import sys

root_path='/afs/cs.stanford.edu/u/tgebru/cars/code/dpm'
path='/afs/cs.stanford.edu/u/tgebru/cars/code/dpm/visualize_dpm'
dpm_path='/afs/cs.stanford.edu/u/tgebru/cars/code/dpm/visualize_dpm/show_dpm'

if root_path not in sys.path:
    sys.path.append(root_path)
if path not in sys.path:
    sys.path.append(path)
if dpm_path not in sys.path:
    sys.path.append(dpm_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "visualize_dpm.settings")
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
