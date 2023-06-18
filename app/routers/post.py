from typing import List

from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get("", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM post""")
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    return posts

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # #Passing statements as f-strings may be vulnerable to SQL
    # # injections so always do it like below
    # cursor.execute("""INSERT INTO post (title, content, published)
    #     VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(
    #     title=post.title, content=post.content, published=post.published)

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/latest")
def get_latest_post(db: Session = Depends(get_db)):
    """Above next path to avoid error"""

    latest_post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    return latest_post


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM post WHERE id = %s", (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f'post with id: {id} not found'}
    return post


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(f"""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post_to_update = post_query.first()
    if post_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} does not exist')

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} does not exist')

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
