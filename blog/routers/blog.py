from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, database
from ..repository import blog
from . import oauth2


router = APIRouter(
    prefix='/blogs',
    tags=['Blogs']
)

@router.get('/', response_model=List[schemas.ShowBlog])
def get_all(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    return blog.get_all(db)
    
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_blog(request:schemas.Blog, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    return blog.create_blog(request, db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_blog(id:int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    return blog.get_blog(id, db)

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_blog(id:int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    return blog.delete_blog(id, db)

@router.put('/{id}', status_code=status.HTTP_200_OK)
def update_blog(id:int,request: schemas.Blog, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    return blog.update_blog(id, request, db)

