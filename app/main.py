from typing import Optional
from time import sleep

import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel

import environ


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = 0


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


@app.get("/")
def root():
    return {"message": "Hello World from root path"}


@app.get("/login")
def login():
    return {'login': 'You are logged in! Welcome!'}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM post""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    #Passing statements as f-strings may be vulnerable to SQL
    # injections so always do it like below
    cursor.execute("""INSERT INTO post (title, content, published) 
        VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/latest")
def get_latest_post():
    """Above next path to avoid error"""

    latest_post = my_posts[-1]
    return {"data": latest_post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("SELECT * FROM post WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f'post with id: {id} not found'}
    return {"post_detail": post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(f"""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} does not exist')
    return {"data": updated_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} does not exist')
    return Response(status_code=status.HTTP_204_NO_CONTENT)

