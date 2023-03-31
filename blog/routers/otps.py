from .. import models
from fastapi import APIRouter, Depends, status,HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, database
from . import oauth2
from . import enumOTP
import uuid
from datetime import datetime


router = APIRouter(
    prefix='/otp',
    tags=['Otps']
)

    

@router.post('/send')
def send_otp(
    type: enumOTP.OTPType,
    request: schemas.CreateOTP,
    db: database.SessionLocal = Depends(database.get_db)
    
):
    # check block OTP
    otp_blocks = oauth2.find_block_otp(db,request.recipient_id)
    if otp_blocks:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Sorry, this phone number is bloked in 5 minutes.")
   
    # Generate and save to table on db
    otp_code = oauth2.random(6)
    session_id = str(uuid.uuid1())
    oauth2.save_otp(db,request,session_id, otp_code,'1')
    
    return {'recipient_id':request.recipient_id,'session_id':session_id,'otp_code':otp_code}

@router.post("/verify")
def send_verify(request:schemas.VerifyOTP, 
db: database.SessionLocal = Depends(database.get_db)):
    # check block OTP
    otp_blocks = oauth2.find_block_otp(db,request.recipient_id)
    if otp_blocks:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail="Sorry, this phone number is bloked in 5 minutes.")
    # Check OTP code 6 digit tifetime
    lifetime_result = oauth2.find_otp_lifetime(db,request)
    if not lifetime_result:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail="OTP code has expired, please request a new one.")
    
    # Verify OTP code
    # if not verfied
    if lifetime_result.otp_code != request.otp_code:
        # increment OTP failed count
        oauth2.update_otp_failed_count(db,lifetime_result)
         
        # if OTP failed count 5 time 
        # then block OTP(otp block)
        if lifetime_result.otp_failed_count == 5:
            oauth2.save_block_otp(db,lifetime_result)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail= "Sorry, This phone numver is blocked in 5 minutes")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="The OTP code you've entered is incorrect.")
    # Check if OTP code is already used
    lifetime_results = lifetime_result.status
    if lifetime_results=="9":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail="OTP code has used, please request a new one.")
    #  Disable OTP code when success verified
    oauth2.disable_otp_code(db,lifetime_result)
    new_user = db.query(models.User).filter(models.User.email==request.recipient_id)
    new_user.update({"status":1})
    db.commit()
    db.refresh(new_user)
    return{
        "status_code":status.HTTP_200_OK,
        "detail":"OTP verified successfully"
    }