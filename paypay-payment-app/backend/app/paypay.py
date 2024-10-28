# backend/app/paypay.py

import os
import time
from dotenv import load_dotenv
import paypayopa

# from paypayopa import Client, ApiError, ConnectionError

load_dotenv()

PAYPAY_API_KEY = os.getenv("PAYPAY_API_KEY")
PAYPAY_API_SECRET = os.getenv("PAYPAY_API_SECRET")
MERCHANT_ID = os.getenv("MERCHANT_ID")
PRODUCTION_MODE = False  # 本番環境ではTrueに設定

client = paypayopa.Client(
    auth=(PAYPAY_API_KEY, PAYPAY_API_SECRET), production_mode=PRODUCTION_MODE
)
client.set_assume_merchant(MERCHANT_ID)


def create_payment(coins, price):
    merchant_payment_id = f"payment_{int(time.time())}"  # ユニークなIDを生成

    request = {
        "merchantPaymentId": merchant_payment_id,
        "codeType": "ORDER_QR",
        "redirectUrl": "http://localhost:3000/payment_status",  # フロントエンドのURLに変更
        "redirectType": "WEB_LINK",
        "orderDescription": "Example - Mune Cake shop",
        "orderItems": [
            {
                "name": "Moon cake",
                "category": "pasteries",
                "quantity": 1,
                "productId": "67678",
                "unitPrice": {"amount": price, "currency": "JPY"},
            }
        ],
        "amount": {"amount": price, "currency": "JPY"},
    }

    try:
        response = client.Code.create_qr_code(request)
        if response and "data" in response and "url" in response["data"]:
            return response, merchant_payment_id
        else:
            print("Invalid response structure:", response)
            return None, merchant_payment_id
    except AttributeError as e:
        print(f"AttributeError: {e}")
        return None, merchant_payment_id
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, merchant_payment_id


def get_payment_details(merchant_payment_id):
    try:
        response = client.payment.get_payment_details(merchant_payment_id)
        return response
    # except (ApiError, ConnectionError) as e:
    #     print(f"API error: {e}")
    #     return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
