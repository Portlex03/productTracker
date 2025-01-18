from typing import Annotated

import requests
from pydantic import Field, validate_call

PRODUCTS_API_URL = (
    "https://pip3.parfum-lider.ru/api/v1/parfum/get_inventory_items_by_store"
)


@validate_call
def get_products_request(
    token: str, store_id: int, count_items: Annotated[int, Field(gt=0, lt=1000)]
) -> list[dict]:
    params = {"store": store_id, "count_items": count_items}
    headers = {"Authorization": token}

    response = requests.get(url=PRODUCTS_API_URL, params=params, headers=headers)
    response_json: list | dict = response.json()

    if isinstance(response_json, dict):
        raise ValueError(response_json["error"])

    responce_data: str | list[dict] = response_json[0]["data"]
    if isinstance(responce_data, str):
        raise ValueError(f"Store with ID {store_id} not found.")

    return responce_data
