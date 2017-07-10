# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################

if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('google:datastore')              # connect to Google BigTable
                                              # optional DAL('gae://namespace')
    session.connect(request, response, db = db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
else:                                         # else use a normal relational database
    db = DAL('mysql://sis2pydba:Swdefrgthy6!@localhost/sis2py')

# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Mail, Auth, Crud, Service, PluginManager, prettydate
mail = Mail()                                  # mailer
auth = Auth(db)                                # authentication/authorization
crud = Crud(db)                                # for CRUD helpers using auth
service = Service()                            # for json, xml, jsonrpc, xmlrpc, amfrpc
plugins = PluginManager()                      # for configuring plugins

mail.settings.server = 'logging' or 'smtp.gmail.com:587'  # your SMTP server
mail.settings.sender = 'you@gmail.com'         # your email
mail.settings.login = 'username:password'      # your credentials or None

from gluon.contrib.states import *
db.define_table('city',
                Field('city', length=32),
                Field('state', length=2, requires=IS_IN_SET(US_STATES)),
                format='%(city)s, %(state)s')
db.define_table('zip',
                Field('zip', unique=True),
                Field('city', db.city),
                format='%(zip)s')
db.define_table('address',
                Field('strno', length=64, label=T('Street number')),
                Field('zip', db.zip, requires=IS_IN_DB(db, db.zip.id, '%(zip)s', zero=T('choose one'))))

auth.settings.extra_fields[auth.settings.table_user_name] =\
    [Field('phone', length=16),
     Field('address', length=80),
     Field('zip', length=12, requires=IS_IN_DB(db, 'zip.id', db.zip._format, multiple=False))]
auth.settings.hmac_key = 'sha512:4a4dd9ee-fed0-40b2-a195-a363579e087a'   # before define_tables()
auth.define_tables()                           # creates all needed tables
db.auth_user._format='%(first_name)s %(last_name)s'
auth.settings.mailer = mail                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL('default','user',args=['verify_email'])+'/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL('default','user',args=['reset_password'])+'/%(key)s to reset your password'

#########################################################################
## If you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, uncomment and customize following
from gluon.contrib.login_methods.rpx_account import RPXAccount
auth.settings.actions_disabled=['register','change_password','request_reset_password']
auth.settings.login_form = RPXAccount(request, api_key='e381032311a0c6b0313380b1df4e47bf8f8c4d38',domain='c9rocs',
   url = "https://%(host)s/%(app)s/default/user/login" % {'host':request.env.http_host, 'app':request.application})
## other login methods are in gluon/contrib/login_methods
#########################################################################

crud.settings.auth = None        # =auth to enforce authorization on crud

##      Classroom information: name, location, capacity, etc.
db.define_table('classroom',
                Field('room', length=16, label=T('Room')),
                Field('campus', length=16),
                Field('building', length=16),
                Field('capacity', 'integer'),
                format='%(campus)s-%(building)s-%(room)s')

##      Classinfo: data for a class at the school
db.define_table('classinfo',
                Field('course', length=32, label=T('Class')),
                Field('teacher', db.auth_user), # must be in 'teacher' auth_group
                Field('schedule', 'time'),
                Field('count', 'integer', label=T('Enrollment'), writable=False),
                Field('max', 'integer', label=T('Capacity')), # maximum enrollment
                Field('room', db.classroom),
                Field('intro', length=80, label=T('Introduction')),
                Field('description', 'text'))

class IS_A_USER:
    '''
    A validator to check if a given value is a user id, optionally with a specified role.
    '''
    def __init__(self,
                 role=None,
                 error_message='User has no role based authorization',
                 no_such_role='No such role',
                 no_such_user='No such user'):
        self.role_id = auth.id_group(role) if role != None else ''
        self.role = role

    def __call__(self, value):
        '''
        Check if a given user (value) has the specified role.
        '''
        rows = db(db.auth_user.id == value).select()
        if not rows:
            return (value, self.no_such_user)

        if self.role != None:
            user_id = rows[0].id
            roles = db(db.auth_membership.user_id == value and db.auth_membership.group_id == self.role_id).select()
            if roles:
                return (value, self.error_message)
        return (value, None)

##      Guardian: Parent/student relationship
db.define_table('guardian',
                Field('parent', db.auth_user, requires=IS_A_USER('parent')),
                Field('child', db.auth_user, requires=IS_A_USER('student')),
                Field('confirmed', 'boolean', default=False, required=True),
                )

##      Enrollment: Class/student relationship (multi-to-multi)
db.define_table('enrollment',
                Field('student', db.auth_user, requires=IS_A_USER('student')),
                Field('enrolled', db.classinfo, requires=IS_IN_DB(db, 'db.classinfo')))
