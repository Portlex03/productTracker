from .base_table import Table


class StoresTable(Table):
    def get_store_data_from_chat_id(self, chat_id: int) -> dict:
        response = (
            self.supabase.table(self.table_name)
            .select("*")
            .eq("chat", chat_id)
            .execute()
        )
        response_data: list[dict] = response.data
        store: dict = response_data[-1]
        return store
