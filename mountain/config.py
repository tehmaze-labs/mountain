from ConfigParser import ConfigParser
from os.path import abspath, basename, dirname, join

# Define the application directory
BASE_DIR = dirname(abspath(__file__))

# Application configuration file
CONFIG = ConfigParser()
CONFIG.read(join(dirname(BASE_DIR), 'conf', 'mountain.conf'))

# Statement for enabling the development environment
DEBUG  = True

# Define the database
SQLALCHEMY_DATABASE_URI = \
    'postgresql+psycopg2://{username}:{password}@{hostname}/{database}'.format(
        **dict(CONFIG.items('database'))
    )

# Cross-Site Request Forgery
CSRF_ENABLED = True
CSRF_SESSION_KEY = '66a9d60608ef2d271592ac20e50783acae537333b70cad3a85878f1c429222bc'.decode('hex')

# Cookies
SECRET_KEY = '7f72534e36988b88497959e6bc893ad592b6459d33a4c82c29df56e776d9310b'.decode('hex')
