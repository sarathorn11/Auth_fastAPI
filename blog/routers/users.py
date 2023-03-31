from fastapi import APIRouter, Depends, Request, status, HTTPException
from sqlalchemy.orm import Session

from blog.routers import oauth2
from .. import schemas, database
from ..repository import users
from typing import List


router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get('/')
def get_all(request:Request,db: Session = Depends(database.get_db)):
    if request.cookies.get('role')!="admin":
        return {"message":"You do not have permission"}
    else:
        return users.get_all(db)
    

@router.post('/') #, response_model=schemas.ShowUser if you want to set view
def create_user(request: schemas.User,requests:Request, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if requests.cookies.get('role')!="admin":
        return {"message":"You do not have permission"}
    else:
        return users.create_user(request, db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_user(id:int,request:Request, db: Session = Depends(database.get_db)):
    if request.cookies.get('role')!="admin":
        return {"message":"You do not have permission"}
    else:
        return users.get_user(id, db)
 
