import string
import random
from functools import wraps
from flask import g, request, redirect, url_for, session, abort
from flask import current_app


def generate_key(key_length=8):
    key_chars = string.ascii_lowercase + string.digits
    random.seed() # initialize with system time to generate different key.
    appkey = ''.join(random.choice(key_chars) for x in range(key_length))
    return appkey
    
    
def csrf_protect(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):    
        if request.method == "POST":
            token = session.pop('_csrf_token', None)
            if not token or token != request.form.get('_csrf_token'):
                abort(403)
        elif request.method == 'GET':
            #keygen = KeyGenerator()
            #token = keygen.getkey(20)
            token = generate_key(20)
            session['_csrf_token'] = token
            current_app.jinja_env.globals['csrf_token'] = token
            print 'assigning token...'
            print 'csrf token:', session['_csrf_token']
        return f(*args, **kwargs)
        
    return decorated_function
        
