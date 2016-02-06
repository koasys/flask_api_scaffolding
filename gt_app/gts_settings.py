from pymongo import MongoClient
from schemas import domain


# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
# individual items  (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']


# API URL CONFIG
URL_PREFIX = 'api'
API_VERSION = '0.1'


# User Package Settings
is_username_email = True
using_email_validation = True
APPKEY_LENGTH = 8

# Not in framework, I added to give option to use RECAPTCHA
RECAPTCHA_ENABLED = False 
# WTF Configuration for Rechaptcha
RECAPTCHA_USE_SSL = False
# These keys are for a testing purpose
RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'

# Flask-Mail configuration
MAIL_SERVER = '' # example: ''smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
DEFAULT_MAIL_SENDER = MAIL_USERNAME

# App Secret Key
# NEED TO CHANGE FOR EACH APP
SECRET_KEY = 'B1Xp83k/4qY1S~GIH!jnM]KES/,?CT'

# App debug mode
DEBUG = True

# Factual API KEY
FACTUAL_APIKEY = 'pC9gGyNpqpTupGkc89DGOpKFAzAtPyo9EVawfHoR'

# Session settings (Flask-Session)
SESSION_TYPE = 'mongodb'
SESSION_KEY_PREFIX = 'gtapp'


# upload setting
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])




# Project Mode (Single | Multiple)
SINGLE_PROJECT_MODE = True
USE_SINGLE_PROJECT_FORM = True
SINGLE_PROJECT_FORM_CONFIG = '''
        { "formId":"1234567890",
            "items":[
                    {"type":"freetext", "itemId":"1", "question":"Name of Surveyor:"},
                    {"type":"freetext", "itemId":"2", "question":"Date:"},
                    {"type":"freetext", "itemId":"3", "question":"Village Name:"},
                                        
                    {"type":"freetext", "itemId":"4", "question":"GPS Location - Latitude:"},
                    {"type":"freetext", "itemId":"5", "question":"GPS Location - Longitude:"},
                    {"type":"freetext", "itemId":"6", "question":"Population of Village:"},
                    {"type":"freetext", "itemId":"7", "question":"Village Leader(s):"},
                    {"type":"freetext", "itemId":"8", "question":"Languages Spoken:"},



                    {"type":"radio", "itemId":"9", "question":"Bible in Mother Tongue?", "choices":["Yes", "No"]},
                    {"type":"radio", "itemId":"10", "question":"Are Bibles Needed?", "choices":["Yes", "No"]},
                    {"type":"freetext", "itemId":"11", "question":"In which Language?"},
                    {"type":"freetext", "itemId":"12", "question":"Best way to contribute?", "note":"(additional notes):"},



                    {"type":"radio", "itemId":"13", "question":"School in Village?", "choices":["Yes", "No"]},
                    {"type":"freetext", "itemId":"14", "question":"Ages of children at school:"},
                    {"type":"freetext", "itemId":"15", "question":"What languages are the students taught in?"},
                    {"type":"freetext", "itemId":"16", "question":"How many students?"},
                    {"type":"freetext", "itemId":"17", "question":"How many teachers?"},



                    {"type":"radio", "itemId":"18", "question":"Mobile phone reception?", "choices":["Yes", "No"]},
                    {"type":"radio", "itemId":"19", "question":"Access to Radio?", "choices":["Yes", "No"]},
                    {"type":"freetext", "itemId":"20", "question":"Station listened to?"},



                    {"type":"freetext", "itemId":"21", "question":"Closest maintained airstrip?"},
                    {"type":"radio", "itemId":"22", "question":"Any Dinghies in the village?", "choices":["Yes", "No"]},
                    {"type":"freetext","itemId":"23", "question":"If Yes, how many?"},
                    {"type":"freetext", "itemId":"24", "question":"Road for vehicles?"},
                    {"type":"freetext", "itemId":"25", "question":"Fuel source location?"},
                    


                    {"type":"radio", "itemId":"26", "question":"Health Care Center?", "choices":["Yes", "No"]},
                    {"type":"checkbox", "itemId":"27", "question":"What type of health care center?", "choices":["Hospital", "Aid Post", "Health Care Center", "None"]},
                    {"type":"freetext", "itemId":"28", "question":"Are immunizations available?"},
                    {"type":"freetext", "itemId":"29", "question":"When was the last patrol?"},
                    {"type":"checkbox", "itemId":"30", "question":"Does this village suffer from any of the following diseases?", "note":"Check all that apply.", "choices":["Tuberculosis", "HIV", "Malaria", "Blindness"]},
                    {"type":"freetext", "itemId":"31", "question":"List the main health concerns of the village:"},
                    {"type":"radio", "itemId":"32", "question":"Have any mother/babies died from/during childbirth?", "choices":["Yes", "No"]},
                    {"type":"freetext", "itemId":"33", "question":"If Yes, how many?"},



                    {"type":"freetext", "itemId":"34", "question":"What is the current source of water?"},
                    {"type":"radio", "itemId":"35", "question":"Is it contaminated?", "choices":["Yes", "No"]},
                    {"type":"radio", "itemId":"36", "question":"Does the village have any water tanks?", "choices":["Yes", "No"]},
                    {"type":"freetext", "itemId":"37", "question":"If Yes, how many?"},
                    {"type":"freetext", "itemId":"38", "question":"Current type of toilets?"},



                    {"type":"freetext", "itemId":"39", "question":"What typical foods are eaten?"},
                    {"type":"radio", "itemId":"40", "question":"Is there farming?", "choices":["Yes", "No"]},
                    {"type":"radio", "itemId":"41", "question":"Is there hunting/fishing?", "choices":["Yes", "No"]}
            ]
        }

        '''   








