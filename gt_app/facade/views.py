from flask import render_template, Blueprint
from flask import current_app, session
import gt_app.gts_settings as settings


# Define the blueprint
facade_views = Blueprint('facade', __name__, template_folder='templates',
    static_folder='static')
    

@facade_views.route('/')
def index():
    debug_set = current_app.config["DEBUG"]   # settings.DEBUG
    if debug_set == True :
        print "\n\n\n==========> facade->views.py -> index() "
    return render_template('index.html')  