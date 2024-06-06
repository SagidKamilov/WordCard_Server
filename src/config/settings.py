# ---------------------------------------------------------
# This file describes the basic settings of the application
# ---------------------------------------------------------

from os import environ

from dotenv import load_dotenv


load_dotenv()

POSTGRES_DB = environ.get("POSTGRES_DB")
POSTGRES_USER = environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = environ.get("POSTGRES_HOST")
POSTGRES_PORT = environ.get("POSTGRES_PORT")

HASHING_ALGORITHM = environ.get("HASHING_ALGORITHM")
