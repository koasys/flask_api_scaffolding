from authentication import HMACAuth, Sha1Auth, HMACAuth_Appkey

# Current API authentication method, make an instance        
hmacauth = HMACAuth_Appkey()


schema_user = {
    'username': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 50,
        'required': True,
        'unique': True,
    },
    'password': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 200,
        'required': True,
    },
    'firstname': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 30,
        'required': True
    },
    'middlename': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 30,
        'required': True,        
    },        
    'lastname': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 30,
        'required': True,        
    },
    'email': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 100
    },
    'is_active': {
        'type': 'boolean',
    },
    # If a system uses email validation process.
    'is_validated': {
        'type': 'boolean',
    },
    'last_login': {
        'type': 'datetime',
    },
    'app_key': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 100,
    }

}


email_regex = "\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*"
users = {
    'item_title': 'user',
    # Additional lookup with username
    'additional_lookup': {
        'url': 'regex("%s")' % email_regex,
        'field': 'username'
    },    
    # We choose to override global cache-control directives for this resource.
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,
    # most global settings can be overridden at resource level
    'resource_methods': ['GET', 'POST'],
    'schema': schema_user,
    #'authentication': hmacauth
}


schema_project = {
    'owner': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 50,
        'required': True,
        'unique': True,
    },
    'name': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 200,
        'required': True,
    },
    'desc': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 200,
        'required': False,
    },
    'member_list': {
        'type': 'list',
    },
    'prj_id': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 50,
        'required': True,
    },
    
}

projects = {
    'item_title': 'project',   
    # Additional lookup with username
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'prj_id'
    },
    # We choose to override global cache-control directives for this resource.
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,
    # most global settings can be overridden at resource level
    'resource_methods': ['GET', 'POST'],
    'schema': schema_project,
    #'authentication': hmacauth    
}


schema_project_member_key = {
    'prj_id': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 100,
        'required': True,
    },
    'member_email': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 100,
        'required': True,
    },
    'appkey': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 100,
        'required': True,
    },    
}


project_member_keys = {
    'item_title': 'project_member_key',   
    # Additional lookup with username
    # We choose to override global cache-control directives for this resource.
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,
    # most global settings can be overridden at resource level
    'resource_methods': ['GET', 'POST'],
    'schema': schema_project_member_key,
    #'authentication': hmacauth     
    
}
