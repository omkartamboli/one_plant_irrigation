#!/usr/bin/env python
"""Create a new admin user able to view the /reports endpoint."""
from getpass import getpass
import sys
from flask.ext.bcrypt import Bcrypt
from WebApp import db, app
import User




def main():
    """Main entry point for script."""
    with app.app_context():
        print 'Enter email address: ',
        email = raw_input()
        password = getpass()
        assert password == getpass('Password (again):')

        user = User(email=email, password=Bcrypt.generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        print 'User added.'

if __name__ == '__main__':
    sys.exit(main())