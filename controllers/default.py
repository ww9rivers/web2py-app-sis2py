# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
<<<<<<< HEAD:applications/sis2py/controllers/default.py
    html = P(SPAN('The home page main content is still being developed. Please '),
             SPAN(''  if auth.is_logged_in() else [A('login', _href=URL('user/login')), ' and ']),
             SPAN('try other menu entries.'))
    return dict(message=T('School Information System'),
                main_content=html)
=======
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

>>>>>>> 1e66fa3a93560aa5d32c27a6b1b7251e0dd8a428:applications/welcome/controllers/default.py

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


<<<<<<< HEAD:applications/sis2py/controllers/default.py
=======
@cache.action()
>>>>>>> a1524d4da46ff851429a1de2022d852f8f2c8e53:applications/welcome/controllers/default.py
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


<<<<<<< HEAD:applications/sis2py/controllers/default.py
@auth.requires_login() 
def api():
    """
<<<<<<< HEAD:applications/sis2py/controllers/default.py
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id[
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs bust be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
=======
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
>>>>>>> a1524d4da46ff851429a1de2022d852f8f2c8e53:applications/welcome/controllers/default.py
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
=======
>>>>>>> 1e66fa3a93560aa5d32c27a6b1b7251e0dd8a428:applications/welcome/controllers/default.py
