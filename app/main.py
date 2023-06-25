import requests
from fastapi import FastAPI

from . import models
from .database import engine
from .routers import post, user, auth, vote


# Since we have alembic now, we don't need this line
#models.Base.metadata.create_all(bind=engine)


app = FastAPI()


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
