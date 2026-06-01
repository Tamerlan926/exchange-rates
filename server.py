from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Literal
import httpx
import time

app = FastAPI()



FALLBACK_RATES = {
    "USD": 1.0,
    "EUR": 0.8599,
    "RUB": 71.3901,
    "GBP": 0.7429,
    "JPY": 158.9658,
    "CNY": 6.8016
}

rates_cache = FALLBACK_RATES.copy() 
last_update = 0

class ConvertRequest(BaseModel):
    amount: float = Field(..., ge=0)
    from_curr: Literal["USD", "EUR", "RUB", "GBP", "JPY", "CNY"]
    to_curr: Literal["USD", "EUR", "RUB", "GBP", "JPY", "CNY"]

    @field_validator('amount')
    @classmethod
    def check_amount(cls, v):
        if v < 0:
            raise ValueError('Сумма не может быть отрицательной')
        return v

async def get_rates():
    global rates_cache, last_update


    if time.time() - last_update > 3600:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get("https://open.er-api.com/v6/latest/USD", timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    new_rates = data.get("conversion_rates", {})
                    if all(curr in new_rates for curr in ["USD", "EUR", "RUB", "GBP", "JPY", "CNY"]):
                        rates_cache = new_rates
                        last_update = time.time()
                        print("Курсы обновлены из API")
                    else:
                        print("️ В ответе API нет нужных валют, используем резервные")
                else:
                    print(f"API вернул статус {resp.status_code}, используем резервные курсы")
        except Exception as e:
            print(f"Не удалось получить курсы из API: {e}. Используем резервные.")
    return rates_cache

@app.post("/convert")
async def convert_currency(req: ConvertRequest):
    rates = await get_rates()


    if req.from_curr not in rates or req.to_curr not in rates:
        raise HTTPException(
            status_code=400, 
            detail=f"Валюта '{req.from_curr}' или '{req.to_curr}' не найдена в базе курсов"
        )

    rate_from = rates[req.from_curr]
    rate_to = rates[req.to_curr]
    


    if rate_from == 0:
        raise HTTPException(status_code=500, detail="Курс исходной валюты равен нулю")

    result = (req.amount / rate_from) * rate_to
    
    return {
        "result": round(result, 2),
        "rate": round(rate_to / rate_from, 4)
    }

@app.get("/")
def root():
    return {"message": "Сервер работает. Используй POST /convert"}
