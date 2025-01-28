from .base_table import Table


class StoresTable(Table):
    def get_store_data_from_chat_id(self, chat_id: int) -> dict:
        response = self.table.select("*").eq("chat", chat_id).execute()
        response_data: list[dict] = response.data

        if not response_data:
            raise ValueError(f"Chat with ID {chat_id} not found.")

        if len(response_data) != 1:
            raise ValueError(f"Chat with ID {chat_id} has more than one store.")

        store: dict = response_data[-1]
        return store

    def insert_store_with_temp_code(self, chat_id: int) -> None:
        response = self.table.select("*").execute()
        new_store: dict = response.data[-1]
        new_store.update(
            {
                "id": new_store["id"] + 1,
                "name": "TempStore",
                "chat": chat_id,
                "code": "0" + new_store["code"],
            }
        )
        response = self.table.insert(new_store).execute()
        assert len(response.data) > 0
