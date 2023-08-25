import pyotp
import datetime


def generate_user_secret_key():
    user_secret = pyotp.random_base32()
    return user_secret


def otp_generator(user_secret: str):
    otp = pyotp.TOTP(user_secret)
    now = datetime.datetime.now()
    otp_code = otp.at(now)

    return otp_code, now


def validate_otp(user_secret: str, user_entered_otp: str, time: datetime):
    otp = pyotp.TOTP(user_secret)
    if not otp.verify(user_entered_otp, time):
        raise Exception("Invalid OTP code.")

    return True


def get_otp_cache_key(user_id: int):
    return f"user_otp:{user_id}"
