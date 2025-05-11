import os
from os import environ

class Config:
    SECRET_KEY = environ.get('SECRET_KEY')  # Load from env
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True  # Debug mode only in dev
