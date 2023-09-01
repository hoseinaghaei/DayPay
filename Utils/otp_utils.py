from django.core.cache import cache

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


def validate_otp(user, user_entered_otp: str):
    stored_otp_data = cache.get(get_otp_cache_key(user.id))

    if not stored_otp_data:
        raise Exception("OTP expired or not generated.")

    otp = pyotp.TOTP(user.secret_key)
    if not otp.verify(user_entered_otp, stored_otp_data[1]):
        raise Exception("Invalid OTP code.")

    cache.delete(get_otp_cache_key(user.id))
    return True


def get_otp_cache_key(user_id: int):
    return f"user_otp:{user_id}"


def generate_otp_and_set_on_cache(user, timeout: int = 120):
    otp_code, now = otp_generator(user.secret_key)
    old_opt = cache.get(get_otp_cache_key(user.id))
    if old_opt:
        cache.delete(get_otp_cache_key(user.id))

    cache.set(get_otp_cache_key(user.id), [otp_code, now], timeout=120)
    return otp_code
