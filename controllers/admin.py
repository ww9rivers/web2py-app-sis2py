import gettext
T = gettext.gettext


@auth.requires_membership('admin')
def authorize():
    '''
    Ideally, we could exclude users who already have the given role.
    '''
    response.view = 'class/add.html'
    form = SQLFORM(db.auth_membership)
    if form.process(session=None, formname='test').accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    # Note: no form instance is passed to the view
    return dict(form=form)


@auth.requires_membership('admin')
def get_users(role=False):
    response.view = 'classes.html'
    query = db((db.auth_membership.user_id == db.auth_user.id) &
               (db.auth_membership.group_id == db.auth_group.id) &
               (db.auth_group.role == role)) if role else db(db.auth_user.id>=0)
    rows = query.select(db.auth_user.id, db.auth_user.last_name, db.auth_user.first_name, db.auth_user.email, db.auth_user.phone)
    if not rows:
        response.flash = T('There is no %s yet.') % T(role if role else 'user')
    return dict(title=T("Ann-Hua Chinese School"),
                main_header="%s: %s" % (T("Users"), T(role).capitalize() if role else T('All')),
                main_content=SQLTABLE(rows, headers='labels', renderstyle=True),
                rsidebar=UL(LI(A(T('Authorize'), _href=URL('admin', 'authorize'), _title=T('Authorize user role'))), )
               )

def admin():
    return get_users('admin')


def parent():
    return get_users('parent')


def student():
    return get_users('student')


def teacher():
    return get_users('teacher')


def users():
    return get_users()
