import settings
from database import db_creator

creator = db_creator.DatabaseCreator(settings.DB_USER, settings.DB_PASSWORD, settings.DB_HOST, settings.DB_NAME,
                                     settings.DB_PORT)
creator.create()
