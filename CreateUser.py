#!/usr/bin/env python
"""Create a new admin user able to view the /reports endpoint."""
from getpass import getpass
import sys
from flask_bcrypt import Bcrypt
from WebApp import app

from dbFunctions import createUser

bcrypt = Bcrypt(app)


def main():
    print 'Enter username:',
    username = raw_input()
    password = getpass()
    assert password == getpass('Password (again):')
    createUser(username, bcrypt.generate_password_hash(password))
    print 'User added.'

if __name__ == '__main__':
    sys.exit(main())