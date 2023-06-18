from time import sleep

import psycopg2
import requests
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session

import environ
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host=environ.POSTGRES_HOST,
                                database=environ.POSTGRES_DB,
                                user=environ.POSTGRES_USER,
                                password=environ.POSTGRES_PASSWORD,
                                port=environ.POSTGRES_PORT,
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection established")
        break
    except Exception as error:
        sleep(5)
        print(f"Error {error} connecting to database")


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World from root path"}


@app.get('/rates', tags=['Exchange rates'])
def get_currency_rates():

    return requests.get('https://www.cbr-xml-daily.ru/latest.js').json()
