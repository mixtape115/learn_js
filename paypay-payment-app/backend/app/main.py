from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.paypay import create_payment
from fastapi.responses import JSONResponse

app = FastAPI()

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切なオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# コインオプションの定義（サーバー側で信頼できるデータとして管理）
COIN_OPTIONS = {
    1: 100,
    3: 300,
    10: 900,
}


@app.post("/api/create_payment")
async def api_create_payment(request: Request):
    data = await request.json()
    coins = data.get("coins")
    price = data.get("price")

    # 入力値の検証
    if coins not in COIN_OPTIONS or COIN_OPTIONS[coins] != price:
        return JSONResponse(
            status_code=400, content={"error": "無効な購入オプションです"}
        )

    response, merchant_payment_id = create_payment(coins, price)

    if response:
        if response.get("resultInfo", {}).get("code") == "SUCCESS":
            response_data = response.get("data", {})
            # merchantPaymentIdをレスポンスに含める
            response_data["merchantPaymentId"] = merchant_payment_id
            return JSONResponse(status_code=200, content=response_data)
        else:
            error_message = response.get("resultInfo", {}).get(
                "message", "決済の作成に失敗しました"
            )
            return JSONResponse(status_code=500, content={"error": error_message})
    else:
        return JSONResponse(
            status_code=500, content={"error": "決済の作成に失敗しました"}
        )
