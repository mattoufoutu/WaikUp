# -*- coding: utf-8 -*-

DEBUG = True
SECRET_KEY = "PLEASE CHANGE ME"
SECURITY_URL_PREFIX = '/user'
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = 'MTc2\x0cR=\x0c8`\r! t)A4L;\n)R6\x0b\\":_Jr}\t'
DATABASE = {
    "name": "waikup",
    "user": "waikup",
    "password": "waikup",
    "engine": "peewee.PostgresqlDatabase"
}
DEFAULT_CATEGORIES = [
    'Web',
    'Forensics',
    'Reverse Engineering',
    'Cryptography',
    'Networking',
    'Development',
    'Malware',
    'News',
    'Fun',
    'Other'
]
DEFAULT_CATEGORY = 'Other'
ITEMS_PER_PAGE = 10
ATOM_LINKS_COUNT = 50
DATETIME_FORMAT = '%b %d %Y at %H:%M:%S'
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = 'username'
MAIL_PASSWORD = 'password'
MAIL_DEFAULT_SENDER = 'sender@example.com'
MAIL_TITLE = "[WaikUp] Latest selected links"
MAIL_RECIPIENTS = []


try:
    from prod_settings import *
except ImportError:
    pass
