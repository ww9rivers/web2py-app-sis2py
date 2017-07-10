import gettext
T = gettext.gettext


@auth.requires_membership('admin')
def add():
    form = SQLFORM(db.classinfo)
    if form.process(session=None, formname='test').accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    # Note: no form instance is passed to the view
    return dict(form=form)


@auth.requires_membership('admin')
def admin():
    response.view = 'classes.html'
    query = db(db.classinfo.id>0)
    rows = query.select(db.classinfo.id, db.classinfo.course, db.classinfo.teacher, db.classinfo.schedule, db.classinfo.intro,
                        db.classinfo.room, db.classinfo.max, db.classinfo.count)
    if not rows:
        response.flash = T('No class defined yet.')
    return dict(title=T("Ann-Hua Chinese School"),
                main_header=T("Ann-Hua Classes"),
                main_content=SQLTABLE(rows, headers='labels', renderstyle=True),
                rsidebar=UL(LI(A(T('Add'), _href=URL('class', 'add'), _title=T('Add class'))), ),
               )


@auth.requires_membership('parent')
def parent():
    response.view = 'classes.html'
    query = db(
        (db.guardian.parent==auth.user_id)\
            & (db.guardian.child==db.enrollment.student)\
            & (db.enrollment.enrolled==db.classinfo.id)\
            & (db.classinfo.room==db.classroom.id))
    rows = query.select(db.classinfo.id, db.classinfo.course, db.classinfo.teacher, db.classinfo.schedule, db.classinfo.intro,
                        db.classinfo.room, db.classinfo.max, db.classinfo.count)
    if not rows:
        response.flash = T('You have not enrolled any student or class yet.')
    return dict(title=T("Ann-Hua Chinese School"),
                main_header=T("My Student(s)' Classes"),
                main_content=SQLTABLE(rows, headers='labels', renderstyle=True),
                rsidebar=UL(LI(A(T('Add'), _href=URL('class', 'add'), _title=T('Add class'))), ),
               )


@auth.requires(lambda: auth.has_membership(role='student') or auth.has_membership(role='teacher'))
def student():
    response.view = 'classes.html'
    query = db(
        (db.enrollment.student==auth.user_id)\
            & (db.enrollment.enrolled==db.classinfo.id)\
            & (db.classinfo.room==db.classroom.id))
    rows = query.select(db.classinfo.id, db.classinfo.course, db.classinfo.teacher, db.classinfo.schedule, db.classinfo.intro,
                        db.classinfo.room, db.classinfo.max, db.classinfo.count)
    if not rows:
        response.flash = T('You have not enrolled in any class yet.')
    return dict(title=T("Ann-Hua Chinese School"),
                main_header=T("Enrollment"),
                main_content=SQLTABLE(rows, headers='labels', renderstyle=True),
                rsidebar=UL(LI(A(T('Add'), _href=URL('class', 'add'), _title=T('Add class'))), ),
               )


@auth.requires_membership('teacher')
def teacher():
    response.view = 'classes.html'
    query = db(db.classinfo.teacher==auth.user_id)
    rows = query.select(db.classinfo.id, db.classinfo.course, db.classinfo.teacher, db.classinfo.schedule, db.classinfo.intro,
                        db.classinfo.room, db.classinfo.max, db.classinfo.count)
    if not rows:
        response.flash = T('No class defined yet.')
    return dict(title=T("Ann-Hua Chinese School"),
                main_header=T("Classes I Teach"),
                main_content=SQLTABLE(rows, headers='labels', renderstyle=True),
                rsidebar=UL(LI(A(T('Add'), _href=URL('class', 'add'), _title=T('Add class'))), ),
               )


@auth.requires_membership('admin')
def room():
    response.view = 'class/add.html'
    form = SQLFORM(db.classroom)
    if form.process(session=None, formname='test').accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    # Note: no form instance is passed to the view
    return dict(form=form)


@auth.requires_membership('admin')
def rooms():
    response.view = 'classes.html'
    rows = db(db.classroom.id>=0).select()
    if not rows:
        response.flash = T('No classroom defined yet.')
    return dict(title=T("Ann-Hua Chinese School"),
                main_header=T("Classrooms"),
                main_content=SQLTABLE(rows, headers='labels', renderstyle=True),
                rsidebar=UL(LI(A(T('Add'), _href=URL('class', 'room'), _title=T('Add classroom'))), ),
               )
