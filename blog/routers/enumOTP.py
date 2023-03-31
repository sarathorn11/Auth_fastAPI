import enum

from sqlalchemy import Enum

class OTPType(enum.Enum):
    phone = "Phone"
    email = "Email"