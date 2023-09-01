import json
import requests
import os

from django.core.cache import cache

import Treasury.models


def get_url(action: str):
    base_url = "https://napi.jibit.ir/trf/v2"
    jibit_urls = {
        "access_token": "/tokens/generate",
        "refresh_token": "/tokens/refresh",
        "transfer": "/transfers"
    }

    return base_url + jibit_urls[action]


def get_access_token():
    access_token = cache.get(get_jibit_access_token_cache_key())

    if access_token:
        return access_token

    payload = {
      "apiKey": os.getenv("JIBIT_API_KEY"),
      "secretKey": os.getenv("JIBIT_SECRET_KEY")
    }
    url = get_url("access_token")
    headers = headers = {
        'Content-Type': 'application/json',
    }

    data_json = json.dumps(payload)
    headers['Content-Length'] = str(len(data_json))

    response = requests.post(url=url, data=data_json, headers=headers).json()
    access_token = response.get("accessToken")
    cache.set(get_jibit_access_token_cache_key(), access_token, timeout=3600)
    return access_token


def send_transaction_to_jibit(transaction: Treasury.models.Transaction):
    url = get_url("transfer")
    payload = {
        "batchID": str(transaction.id),
        "submissionMode": "TRANSFER",
        "transfers": [
            {
                "transferID": transaction.transfer_id,
                "transferMode": transaction.transfer_mode,
                "destination": transaction.destination,
                "amount": transaction.amount,
                "currency": "RIALS",
                "description": "daypay withdraw from wallet"
            }
        ]
    }

    headers = headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + get_access_token()
    }

    data_json = json.dumps(payload)
    headers['Content-Length'] = str(len(data_json))

    requests.post(url=url, data=data_json, headers=headers).json()


def get_jibit_access_token_cache_key():
    return "jibit_access_token"
