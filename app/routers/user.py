from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print(user)
    user_exists = db.query(models.User).filter_by(email=user.email).first()

    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'The user with {user.email} is already registered')

    #hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user_dict = user.dict()

    new_user = models.User(**new_user_dict)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The user with id {id} is not exist")

    return user


@router.delete('')
def purge_all_users(db: Session = Depends(get_db)):
    db.query(models.User).delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)