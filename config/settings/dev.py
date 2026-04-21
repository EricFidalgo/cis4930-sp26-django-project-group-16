from .base import *
from decouple import config, Csv

try:
    DEBUG = config('DEBUG', default=True, cast=bool)
except ValueError:
    DEBUG = True
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost,testserver', cast=Csv())
