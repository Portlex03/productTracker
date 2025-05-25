import requests

STORES_API_URL = "https://www.parfum-lider.ru/upload/bot/map.json"


def get_stores() -> list[dict]:
    response = requests.get(STORES_API_URL)
    json: list[dict] = response.json()
    return json
