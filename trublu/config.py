"""trublu development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = (b'\x9b)f\x9f\x02\xef\xff\xb3\x0c\x9d,1MD\xe6j\xd7m\x06\xcd\
                xee\xd3\x06\xda')
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
trublu_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = trublu_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/trublu.sqlite3
DATABASE_FILENAME = trublu_ROOT/'var'/'trublu.sqlite3'
