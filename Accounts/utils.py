import pyotp


def otp_generator():
    user_secret = pyotp.random_base32()

    otp = pyotp.TOTP(user_secret)

    otp_code = otp.now()

    return otp_code
