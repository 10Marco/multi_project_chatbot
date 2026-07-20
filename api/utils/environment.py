import os

APP_ENV = os.getenv("APP_ENV", "development")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

def is_dev():
    return APP_ENV == "development"

def is_prod():
    return APP_ENV == "production"