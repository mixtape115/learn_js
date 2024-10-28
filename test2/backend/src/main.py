from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import time
import os
from dotenv import load_dotenv
import paypayopa
from pydantic import BaseModel, Field

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

PAYPAY_API_KEY = os.getenv("PAYPAY_API_KEY")
PAYPAY_API_SECRET = os.getenv("PAYPAY_API_SECRET")
MERCHANT_ID = os.getenv("MERCHANT_ID")
PRODUCTION_MODE = False  # 本番環境ではTrueに設定

client = paypayopa.Client(
    auth=(PAYPAY_API_KEY, PAYPAY_API_SECRET), production_mode=PRODUCTION_MODE
)
client.set_assume_merchant(MERCHANT_ID)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://payment-frontend-test2",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic モデルの定義
class PaymentRequest(BaseModel):
    price: int = Field(
        ..., gt=0, description="支払いに使用する価格は正の整数でなければなりません"
    )


@app.get("/")
def Hello():
    return {"Hello": "World!"}


@app.post("/create_payment")
def create_payment_endpoint(request: PaymentRequest):
    try:
        price = request.price
        logger.info(f"Received coins: {price}")
        response, merchant_payment_id = create_payment(price)

        if response:
            return {
                "merchantPaymentId": merchant_payment_id,
                "qrCodeUrl": response["data"]["url"],
            }
        else:
            raise HTTPException(status_code=500, detail="Payment creation failed.")
    except Exception as e:
        logger.error(f"Error in create_payment_endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def create_payment(price: int):
    merchant_payment_id = f"payment_{int(time.time())}"

    request = {
        "merchantPaymentId": merchant_payment_id,
        "codeType": "ORDER_QR",
        "redirectUrl": "http://localhost:3000/payment_status",
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
