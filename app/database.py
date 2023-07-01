from time import sleep

import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import environ

SQLALCHEMY_DATABASE_URL = f"postgres://{environ.POSTGRES_USER}:" \
                          f"{environ.POSTGRES_PASSWORD}@" \
                          f"{environ.POSTGRES_HOST}/" \
                          f"{environ.POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Just for the reference, this part is not used since we use SQLAlchemy to connect to database

# while True:
#     try:
#         conn = psycopg2.connect(host=environ.POSTGRES_HOST,
#                                 database=environ.POSTGRES_DB,
#                                 user=environ.POSTGRES_USER,
#                                 password=environ.POSTGRES_PASSWORD,
#                                 port=environ.POSTGRES_PORT,
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection established")
#         break
#     except Exception as error:
#         sleep(5)
#         print(f"Error {error} connecting to database")
