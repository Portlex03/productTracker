from .base_table import Table


class StoresTable(Table):
    def get_store_data_from_chat_id(self, chat_id: int) -> dict:
        response = (
            self.supabase.table("Stores").select("*").eq("chat", chat_id).execute()
        )
        response_data: list[dict] = response.data

        if not response_data:
            raise ValueError(f"Chat with ID {chat_id} not found.")

        if len(response_data) != 1:
            raise ValueError(f"Chat with ID {chat_id} has more than one store.")

        store: dict = response_data[-1]
        return store

    def insert_shop_with_temp_code(self, chat_id: int) -> None:
        pass
