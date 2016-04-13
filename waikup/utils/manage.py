#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from getpass import getpass

from flask.ext.mail import Message
from flask.ext.security import PeeweeUserDatastore
from flask.ext.script import Manager
from jinja2 import Environment, PackageLoader

from waikup.app import app, db, mail
from waikup.lib.errors import ApiError
from waikup.models import BaseModel, Category, User, Role, UserRole, Link

try:
    import simplejson as json
except ImportError:
    import json

TABLES = BaseModel.__subclasses__()
manager = Manager(app)


def create_categories():
    for cat in app.config['DEFAULT_CATEGORIES']:
        if Category.select().where(Category.name == cat).count() == 0:
            print "[+] Inserting category: %s" % cat
            Category.create(name=cat)


def read_db_version():
    version = 0
    if os.path.exists(app.config['DB_VERSION_FILE']):
        with open(app.config['DB_VERSION_FILE']) as inf:
            version = inf.read().strip() or '0'
            if not version.isdigit():
                print "[!] Unexpected version value: %s" % version
                sys.exit(2)
    return int(version)


def write_db_version(ver):
    with open(app.config['DB_VERSION_FILE'], 'w') as outf:
        outf.write(str(ver))


@manager.command
def setupdb():
    """Creates the database schema."""
    for table in TABLES:
        print "[+] Creating table: %s..." % table._meta.name
        table.create_table(fail_silently=True)
    create_categories()
    print "[+] Done"


@manager.command
def resetdb():
    """Resets database content."""
    for table in reversed(TABLES):
        print "[+] Resetting table: %s..." % table._meta.name
        table.delete().execute()
        db.database.execute_sql(*db.database.compiler().drop_table(table, cascade=True))
    setupdb()


@manager.command
def adduser(admin=False, inactive=False):
    """Adds a new user."""
    user_datastore = PeeweeUserDatastore(db, User, Role, UserRole)
    print "[+] Creating new user (admin=%r, inactive=%r)" % (admin, inactive)
    username = raw_input("[>] Username: ")
    first_name = raw_input("[>] First name: ")
    last_name = raw_input("[>] Last name: ")
    email = raw_input("[>] Email: ")
    password1 = getpass("[>] Password: ")
    password2 = getpass("[>] Confirm password: ")
    if password1 != password2:
        print "[!] Passwords don't match!"
        sys.exit(1)
    user_datastore.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        admin=admin,
        active=not inactive,
        password=password1
    )
    print "[+] Done"


@manager.command
def chpasswd(username):
    """Change given user's password."""
    try:
        user = User.get(User.username == username)
    except ApiError:
        print "[!] Unknown user: %s" % username
        sys.exit(1)
    password1 = getpass("[>] Password: ")
    password2 = getpass("[>] Confirm password: ")
    if password1 != password2:
        print "[!] Passwords don't match!"
        sys.exit(2)
    print "[+] Changing %s's password" % username
    user.set_password(password1)
    user.save()
    print "[+] Done"


@manager.command
def sendmail():
    """Sends an email containing last submitted links."""
    links = Link.select().where(Link.archived == False)
    print "[+] Loading and populating email templates..."
    env = Environment(loader=PackageLoader('waikup', 'templates/emails'))
    html = env.get_template('html.jinja2').render(links=links)
    text = env.get_template('text.jinja2').render(links=links)
    print "[+] Sending email..."
    msg = Message(recipients=app.config['MAIL_RECIPIENTS'])
    msg.subject = app.config['MAIL_TITLE']
    msg.body = text
    msg.html = html
    mail.send(msg)
    print "[+] Archiving links..."
    for link in links:
        link.archived = True
        link.save()
    print "[+] Done"


def main():
    manager.run()


if __name__ == '__main__':
    main()
