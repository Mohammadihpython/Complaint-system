from config import settings
import databases
import sqlalchemy
DATABASE_URL = settings("DATABASE_URL")

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()