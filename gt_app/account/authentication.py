from eve.auth import BasicAuth, HMACAuth
from werkzeug.security import check_password_hash
from hashlib import sha1
import hmac
from flask import current_app

# Supported Authentication
# ---
class HMACAuth(HMACAuth):
    def check_auth(self, username, hmac_hash, headers, data, allowed_roles,  resource, method):
        # use Eve's own db driver; no additional connections/resources are
        # used
        app = current_app._get_current_object()
        accounts = app.data.driver.db['accounts']
        user = accounts.find_one({'username': username})
        if user:
            secret_key = user['secret_key']
        # in this implementation we only hash request data, ignoring the
        # headers.
        return ( user and 
            hmac.new(str(secret_key), str(data), sha1).hexdigest() == hmac_hash) 

class Sha1Auth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        # use Eve's own db driver; no additional connections/resources are used
        app = current_app._get_current_object()
        accounts = app.data.driver.db['accounts']
        account = accounts.find_one({'username': username})
        # If you saved a hashed password in db.
        return account and (password == account['password']) 
        # If you saved a clear text password
        #return account and check_password_hash(account['password'], password) 
        

class HMACAuth_Appkey(HMACAuth):
    '''
    HMAC Authentication with a user's app key. 
    This is used for mobile application to submit user data.
    '''
    def check_auth(self, username, hmac_hash, headers, data, allowed_roles, resource, method):
        # Use Eve's own db driver; no additional connections/resources are
        # used
        app = current_app._get_current_object()

        #users = app.data.driver.db['users']
        #user = users.find_one({'username': username})
        users = app.data.driver.db['project_member_key']
        user = users.find_one({'member_email': username}) 
        if user:
            app_key = user['appkey']
        # In this implementation we only hash request data, ignoring the
        # headers.
        make_hmac = hmac.new(str(app_key), str(data), sha1).hexdigest()
        #print "======> username: ", username        
        #print "======> app_key: ", app_key
        #print "===> input hmac_hash: ", hmac_hash
        #print "===> make_hmac: ", make_hmac
        return ( user and  make_hmac == hmac_hash)


