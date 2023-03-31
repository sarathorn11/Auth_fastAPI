from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime, TIMESTAMP, text
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
from sqlalchemy.sql import func



class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates='blogs')

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    status = Column(Integer, default=1)
    role = Column(String, default="website_user")
    blogs = relationship("Blog", back_populates='creator')

class Token_blacklist(Base):
    __tablename__ = 'blacklist'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)  
    token = Column(String, unique=True)  

class Otps(Base):
    __tablename__ = 'otps'

    id = Column(Integer, primary_key=True, index=True)
    recipient_id = Column(String)  
    session_id = Column(String(100))
    otp_code = Column(String(6))
    status = Column(String(1))
    created_on = Column(DateTime, default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    otp_failed_count= Column(Integer,default=0)


class OtpBlocks(Base):
    __tablename__ = 'otp_blocks'

    id = Column(Integer, primary_key=True, index=True)
    recipient_id = Column(String(100))  
    created_on = Column(DateTime)  


class Codes(Base):
    __tablename__ = 'codes'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100)) 
    reset_code = Column(String(50)) 
    status = Column(String(1)) 
    expired_in = Column(DateTime) 