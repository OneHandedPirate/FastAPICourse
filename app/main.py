import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import post, user, auth, vote
from . import models
from .database import engine

# Since we have alembic now, we don't need this line
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World from root path"}


@app.get('/rates', tags=['Exchange rates'])
def get_currency_rates():

    return requests.get('https://www.cbr-xml-daily.ru/latest.js').json()
