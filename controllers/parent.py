import gettext
T = gettext.gettext


@auth.requires_membership('parent')
def student():
    response.view = 'classes.html'
    role = 'student'
    query = db((db.guardian.parent == auth.user_id) & (db.guardian.child == db.auth_user.id))
    rows = query.select(db.auth_user.id, db.auth_user.last_name, db.auth_user.first_name, db.auth_user.email, db.auth_user.phone)
    if not rows:
        response.flash = T('You have not enrolled a student yet.')
    return dict(title=T("Ann-Hua Chinese School"),
                main_header="%s: %s" % (T("Users"), T(role).capitalize() if role else T('All')),
                main_content=SQLTABLE(rows, headers='labels', renderstyle=True),
                rsidebar=UL(LI(A(T('Authorize'), _href=URL('admin', 'authorize'), _title=T('Authorize user role'))), )
               )
