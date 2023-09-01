from kavenegar import *
import json
from decouple import config


def send_login_otp(otp_code: str, receptor: str):
    try:
        api = KavenegarAPI(config("SMS_API_KEY"))
        params = {
            "receptor": receptor,
            "token": otp_code,
            "template": "daypayotp"
        }
        api.verify_lookup(params)
    except Exception as e:
        pass


def send_withdraw_otp(otp_code: str, receptor: str):
    try:
        api = KavenegarAPI(config("SMS_API_KEY"))
        params = {
            "receptor": receptor,
            "token": otp_code,
            "template": "daypayset"
        }
        api.verify_lookup(params)
    except Exception as e:
        pass
