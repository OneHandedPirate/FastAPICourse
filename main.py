from typing import Optional
from random import randrange

from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = 0


my_posts = [
    {
        'title': 'Title of the very 1st post',
        'content': 'The content of the very 1st post',
        'id': 1
    },
    {
        'title': 'Favorite food',
        'content': 'My favorite food is.. try to guess',
        'id': 2
    }
]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


@app.get("/")
def root():
    return {"message": "Hello World from root path"}


@app.get("/login")
def login():
    return {'login': 'You are logged in! Welcome!'}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.get("/posts/latest")
def get_latest_post():
    """Above next path to avoid error"""

    latest_post = my_posts[-1]
    return {"data": latest_post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f'post with id: {id} not found'}
    return {"post_detail": find_post(id)}


@app.put("/posts/{pk}")
def update_post(pk):
    return {"data": f"This is the updated post with the id {pk}"}


@app.delete("/posts/{pk}")
def delete_post(pk):
    return {"data": f"The post with the id {pk} was deleted"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(2, 100000)
    my_posts.append(post_dict)
    return {"data": post_dict}



