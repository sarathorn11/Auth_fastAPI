from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from .. import models, schemas

def get_all(db):
    blogs = db.query(models.Blog).all()
    return blogs

def create_blog(request:schemas.Blog, db:Session):
    new_blog = models.Blog(title=request.title, body=request.body,user_id=1)

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

def get_blog(id:int, db:Session):
    blogs = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blogs:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"ID {id} NOT FOUND.")

    return blogs

def delete_blog(id:int, db:Session):
    blogs = db.query(models.Blog).filter(models.Blog.id == id)

    if not blogs.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"ID {id} is NOT FOUND.")

    blogs.delete(synchronize_session=False)
    db.commit()

    return "DELETED"

def update_blog(id:int, request: schemas.Blog, db:Session):
    blogs = db.query(models.Blog).filter(models.Blog.id == id)

    if not blogs.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"ID {id} is NOT FOUND.")

    blogs.update(request.dict())
    db.commit()

    return "UPDATED"