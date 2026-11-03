# print("Hello from agent-lab!")

#import os
#from dotenv import load_dotenv

#load_dotenv()
#secret = os.getenv("DEMO_SECRET")
#print(f"Secret loaded: {secret is not None}")

import httpx

URL = "https://www.cbr-xml-daily.ru/daily_json.js"

try:
    response = httpx.get(URL, timeout=10)
    response.raise_for_status()          # turns HTTP errors (404, 500) into exceptions
    data = response.json()               # JSON text → Python dict
    usd = data["Valute"]["USD"]["Value"]
    print(f"USD rate: {usd} RUB")
except httpx.HTTPError as error:
    print(f"Could not get the rate: {error}")