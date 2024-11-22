from supabase import create_client, Client

STORES_TABLE_NAME = "stores"

class DBAPIConnector:
    supabase: Client

    def connect(self, supabase_url: str, supabase_key: str) -> None:
        self.supabase = create_client(supabase_url, supabase_key)


class StoresDBConnector(DBAPIConnector):
    table_name: str = STORES_TABLE_NAME

    store_id: str = "store_id"

    store_name: str = "store_name"

    store_chat_id: str = "store_chat_id"

    def get_store_data_from_chat_id(self, chat_id: int) -> dict:
        """Returns db row with specific chat_id"""
        response = (
            self.supabase.table(self.table_name)
            .select("*")
            .eq(self.store_chat_id, chat_id)
            .execute()
        )
        response_data: list[dict] = response.data
        store: dict = response_data[0]
        return store

