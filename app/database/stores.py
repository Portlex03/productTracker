import random

from .base_table import Table


class Stores(Table):
    def get_store_data_from_chat_id(self, chat_id: int) -> dict:
        response = self.table.select("*").eq("chat", chat_id).execute()
        response_data: list[dict] = response.data

        if not response_data:
            raise ValueError(f"Chat with ID {chat_id} not found.")

        if len(response_data) != 1:
            raise ValueError(f"Chat with ID {chat_id} has more than one store.")

        store: dict = response_data[-1]
        return store

    def insert_store_with_temp_code(self, chat_id: int) -> dict:
        response = self.table.select("*").execute()
        max_id = max(store["id"] for store in response.data)

        new_store: dict = random.sample(response.data, k=1)[0]
        changed_data = {
            "id": max_id + 1,
            "name": "TempStore",
            "chat": chat_id,
            "code": "0" + new_store["code"],
        }
        new_store.update(changed_data)

        response = self.table.insert(new_store).execute()
        return response.data[-1]
