from datetime import datetime, timezone
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from blog import database
from . import token
from .. import models,schemas
from sqlalchemy.orm import Session
import string
from random import choice
import pytz




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_token_user(token:str = Depends(oauth2_scheme)):
    return token

def get_current_user(db: database.SessionLocal = Depends(database.get_db),data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # when we logout to make user can not do anything
    block_list_token = find_black_list_token(db,data)
    if block_list_token:
        raise credentials_exception
    return token.verify_token(data, credentials_exception)   

def find_black_list_token(db:Session,token:str):
    return db.query(models.Token_blacklist).filter(models.Token_blacklist.token == token).first()

def save_black_list_token(token:str,db:Session,current_user: models.User.email):
    blok_token = models.Token_blacklist(token=token,email=current_user)
    db.add(blok_token)
    db.commit()
    db.refresh(blok_token)
    return blok_token

def find_block_otp(db:Session,recipient_id:str):
    return db.query(models.OtpBlocks).filter(models.OtpBlocks.recipient_id == recipient_id).first()

def random(digits:int):
    chars = string.digits
    return "".join(choice(chars) for _ in range(digits))

def save_otp(db:Session,request:schemas.CreateOTP,session_id:int,otp_code:str,status):
    new_otp = models.Otps(recipient_id=request.recipient_id,session_id=session_id,otp_code=otp_code,status=status)
    db.add(new_otp)
    db.commit()
    db.refresh(new_otp)
    return new_otp

def find_otp_lifetime(db:Session,request:schemas.VerifyOTP):
    return db.query(models.Otps).filter(models.Otps.recipient_id == request.recipient_id and
     models.Otps.session_id == request.session_id and models.Otps.created_on >= datetime.now(pytz.timezone('Asia/Phnom_Penh'))).first()
def update_otp_failed_count(db:Session,request:schemas.OTPList):
    old_otp = db.query(models.Otps).filter(models.Otps.recipient_id == request.recipient_id)
    old_otp.update({'otp_failed_count':request.otp_failed_count+1})
    db.commit()
    return {"recipient_id":request.recipient_id,"session_id":request.session_id ,"otp_code":request.otp_code}

def save_block_otp(db:Session,request:schemas.OTPList):
    new_otp_block = models.OtpBlocks(recipient_id=request.recipient_id,created_on=datetime.now(pytz.timezone('Asia/Phnom_Penh')))
    db.add(new_otp_block)
    db.commit()
    db.refresh(new_otp_block)
    return new_otp_block

def disable_otp_code(db:Session,request:schemas.OTPList):
    otp_code = db.query(models.Otps).filter(models.Otps.status == "1" and models.Otps.recipient_id==request.recipient_id)
    if not otp_code.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'otp_code with the id {id} is not available')
    otp_code.update({'status':"9"})
    db.commit()
    return {"recipient_id":request.recipient_id,"session_id":request.session_id,"otp_code":request.otp_code}


def find_exit_user(email:str, db:Session):
    user_exit = db.query(models.User).filter(models.User.email ==email).first()
    if not user_exit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")
    return user_exit

def create_reset_code(email:str,reset_code:str, db:Session):
    new_code = models.Codes(email=email, reset_code=reset_code,status="1",expired_in= datetime.now(pytz.timezone('Asia/Phnom_Penh')))
    db.add(new_code)
    db.commit()
    db.refresh(new_code)
    return new_code

def check_reset_password_token(reset_password_token:str, db:Session):
    token_reset = db.query(models.Codes).filter(models.Codes.status =="1" and models.Codes.reset_code==reset_password_token and models.Codes.expired_in>= datetime.now(pytz.timezone('Asia/Phnom_Penh'))).first()
    if not token_reset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")
    return token_reset

def reset_password(new_hashed_password:str,email:str,db:Session):
    old_password = db.query(models.User).filter(models.User.email == email)
    old_password.update({'password':new_hashed_password})
    db.commit()
    return old_password

def disable_reset_code(reset_password_token:str,email:str,db:Session):
    old_password = db.query(models.Codes).filter(models.Codes.status == "1" and models.Codes.email == email and models.Codes.reset_code==reset_password_token)
    old_password.update({"status":"9"})
    db.commit()
    return old_password
