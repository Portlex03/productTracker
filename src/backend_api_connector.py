import requests

PRODUCTS_API_URL = "https://pip3.parfum-lider.ru/api/v1/parfum/get_inventory_items_by_store"

STORES_API_URL = "https://www.parfum-lider.ru/upload/bot/map.json"


def get_products(token: str, store_id: int, count_items: int) -> list[dict]:
    """Returns a list of products dictionaries from store"""
    response = requests.get(
        url=PRODUCTS_API_URL,
        params={"store": store_id, "count_items": count_items},
        headers={"Authorization": token},
    )
    json: list[dict] = response.json()[0]["data"]
    return json

def get_stores() -> list[dict]:
    response = requests.get(STORES_API_URL)
    json: list[dict] = response.json()
    return json
