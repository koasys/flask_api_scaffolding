import json
import string
import random
from flask.ext.login import UserMixin
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId


# Configuration Parameters
# ------------------------
encryption_method = 'pbkdf2:sha256:5000'


# Custom Exception
# 
class NotUniqueException(Exception):
    '''
    If an object to handle is not unique and already exists in a system.
    '''
    def __init__(self, mssg):
        self.mssg = mssg


# Classes
#
class User(UserMixin):
    '''
    User object that will be managed by Flask-Login and work with MongoDB.
    This model should work with Eve framework schema definition. However, 
    this resource type is managed OUTSIDE of eve framework.
    '''
    def __init__(self, username, firstname, middlename, lastname, email, 
        active, anonymous, validated, password_hash=''):   
        self.active = active
        self.anonymous = anonymous
        self.validated = validated
        self.username = username
        self.password_hash = password_hash
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.email = email
        self.generate_appkey()
    
    
    def authenticate(self, password):
        # if password is same with password in db
        # set self.authenticated = True
        return check_password_hash(self.password_hash, password)
            
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        

    def generate_appkey(self):
        key_length = 8
        key_chars = string.ascii_lowercase + string.digits
        appkey = ''.join(random.choice(key_chars) for x in range(key_length))
        self.appkey = appkey
        return appkey

    
    def update_password(self, newone):
        self.password_hash = generate_password_hash(newone, 
            method=encryption_method)    
        
    def save(self):
        mongo = current_app._get_current_object().data.driver
        obj_str = json.dumps(self, default=lambda o: o.__dict__)
        obj = json.loads(obj_str)
        #print 'new user json is: %s' % obj_str
        mongo.db.users.update({'username':self.username},obj, upsert=True)
        
        
    @staticmethod
    def create(username, password, firstname, middlename, lastname, email):
        mongo = current_app._get_current_object().data.driver
        # To check if username is already existing.
        user = mongo.db.users.find_one({'username': username})
        if user:
            print 'current db name"', mongo.db.name
            print 'the new user already exists!'
            return None # the username is already existing. Throw an exception.
        else:
            # Generate a salted password by using PBKDF2-SHA256
            password_hash = generate_password_hash(password, 
                method=encryption_method)
           
            new_user = User(username=username, password_hash=password_hash,
                firstname=firstname, middlename=middlename, lastname=lastname,
                email=email, active=True, anonymous=False, validated=False)
        
            return new_user       
        
        
    @staticmethod
    def get_with_username(username=''):
        '''
        Return User object that matches a given username by reading a db.
        This method should be called inside of request context in order to get
        current_app object.
        '''
        mongo = current_app._get_current_object().data.driver
        user = mongo.db.users.find_one({'username': username})
        
        if user is None:
            return None
        
        return User(username=user['username'],  firstname=user['firstname'], 
            middlename=user['middlename'], lastname=user['lastname'], 
            email=user['email'], password_hash=user['password_hash'], 
            validated=user['validated'], active=user['active'], 
            anonymous=False)
            
            
    @staticmethod
    def get_with_userid(useroid):
        mongo = current_app._get_current_object().data.driver
        user = mongo.db.users.find_one({'_id': ObjectId(useroid)})
        return User.get_with_username(username=user['username'])
        
        
                
    # methods for Flask-Login user
    # ===
    def is_authenticated(self):
        ''' Assume all User object after login point are authenticated. 
            That means that if you have User ID stored in user session,
            it is authenticated.
        '''
        return True
        
    def is_active(self):
        return self.active
    
        
    def is_anonymous(self):
        return self.anonymous
    
    
    def get_id(self):
        return self.username       
                  

class Project:
    '''
    Project object that holds project information.
    This model should work with Eve framework schema definition. However, 
    this resource type is managed OUTSIDE of eve framework.
    '''
    # Class Static Variables
    ROLE_OWNER = 'owner'
    ROLE_MEMBER = 'member'    
    
    
    def __init__(self, prj_name, prj_desc, owner, prj_id=None, is_private=True,
            member_list=[]):
        self.name = prj_name
        self.desc = prj_desc
        self.owner = owner # owner's username
        self.member_list = member_list # object id list of members
        self.prj_id = prj_id
        self.is_private = is_private # flag to indicate private vs public dataset
        if prj_id is None:
            self.prj_id = self.create_prj_id()
        
        
    def save(self):
        mongo = current_app._get_current_object().data.driver
        obj_str = json.dumps(self, default=lambda o: o.__dict__)
        obj = json.loads(obj_str)
        #print 'new project json is: %s' % obj_str
        mongo.db.projects.update({'prj_id':self.prj_id}, obj, upsert=True)
        return self.prj_id
        
            
    def create_prj_id(self):
        '''
        System generated project id
        '''
        r_num = 6 # the length of prj_id
        char_range = string.ascii_lowercase + string.digits
        # prj_id is one of IDs that a user need to type into an app.
        mongo = current_app._get_current_object().data.driver
        prj_id = ''.join(random.choice(char_range) for x in range(r_num))
        # Check if prj_id is unique. If not, generate it again.
        while True: 
            prj = mongo.db.projects.find_one({'prj_id': prj_id})
            if prj is None:
                break
            prj_id = ''.join(random.choice(char_range) for x in range(r_num))
        
        return prj_id
        
        
    def add_member(self, name, email, role):
        '''
        Add a member of a project.
        Check if new member's email exists in the member list, and if not, add
        the member to the member list.
        '''
        # Before checking, create a list of member emails
        email_list = {}
        for m in self.member_list:
            email_list[m['email']] = True

        # Check if new member email is already in member email list
        if email not in email_list.keys():  
            new_member = {}
            new_member['name'] = name
            new_member['email'] = email
            new_member['role'] = role # values in ['owner','member']
            self.member_list.append(new_member)
            # save
            self.save()
        else: # Need to inform user
            raise NotUniqueException('New member email already exists!')
      
    def delete_member(self, email):
        for mem in self.member_list:
            if mem['email'] == email:
                self.member_list.remove(mem)
        self.save()
    
    
    def get_num_member(self):
        return len(self.member_list)
        
    
    # CLASS METHODS
    # -----    
    @staticmethod
    def get_projects_for_username(username):
        '''
        Get a list of projects for a user id (user's object id in mongodb)
        '''
        mongo = current_app._get_current_object().data.driver
        projects = mongo.db.projects.find({'owner': username})
        
        prj_list = []
        for row in projects:
            print 'project row', row
            prj = Project(prj_name=row['name'], prj_desc=row['desc'],
                owner=username, prj_id=row['prj_id'], is_private=row['is_private'],
                member_list=row['member_list'])
            #prj.member_list = json.loads(row['member_list'])  
            prj_list.append(prj)
        
        return prj_list        
    
    @staticmethod
    def get_project_for_projectid(prj_id):
        mongo = current_app._get_current_object().data.driver
        row = mongo.db.projects.find_one({'prj_id': prj_id})
        if row is not None:
            prj = Project(prj_name=row['name'], prj_desc=row['desc'],
                owner=row['owner'], prj_id=row['prj_id'], 
                is_private=row['is_private'], member_list=row['member_list'])
            #prj.member_list = json.loads(row['member_list'])    
            return prj  
        else:
            return None
    
    @staticmethod
    def check_project_member(prj_id, member_email):
        project = Project.get_project_for_projectid(prj_id)
        
        if project is None:
            return False
        
        for mem in project.member_list:
            if mem['email'] == member_email:
                return True
        
        return False


class ProjectMemberKey:
    '''
    Manages a project member's appkey.
    '''
    
    def __init__(self, prj_id, member_email, appkey):
        self.prj_id = prj_id
        self.member_email = member_email
        self.appkey = appkey
        
        
    def save(self):
        mongo = current_app._get_current_object().data.driver
        obj_str = json.dumps(self, default=lambda o: o.__dict__)
        obj = json.loads(obj_str)
        #print 'new project json is: %s' % obj_str
        mongo.db.project_member_key.update(
            {'prj_id':self.prj_id,'member_email':self.member_email}, obj, upsert=True)
            
            
    @staticmethod
    def find_one(prj_id, member_email):
        mongo = current_app._get_current_object().data.driver
        row = mongo.db.project_member_key.find_one({'prj_id': prj_id, 'member_email':member_email})
        return row

    @staticmethod
    def find_one_prj_id(member_email, appkey):
        mongo = current_app._get_current_object().data.driver
        row = mongo.db.project_member_key.find_one({'member_email':member_email, 'appkey': appkey })
        return row       
    
    @staticmethod        
    def get_memberkeys_for_project(prj_id):
        mongo = current_app._get_current_object().data.driver
        rows = mongo.db.project_member_key.find({'prj_id': prj_id})
        memkeys = {}
        for row in rows:
            print row
            memkeys[row['member_email']] = row['appkey']        
        return memkeys
        
        
        
    






        
    
    
    
    