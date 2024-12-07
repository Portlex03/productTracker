from supabase import create_client, Client

STORES_TABLE_NAME = "stores"

PRODUCTS_TABLE_NAME = "products_tracking"


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
        response = (
            self.supabase.table(self.table_name)
            .select("*")
            .eq(self.store_chat_id, chat_id)
            .execute()
        )
        response_data: list[dict] = response.data
        store: dict = response_data[0]
        return store


class ProductsDBConnector(DBAPIConnector):
    table_name: str = PRODUCTS_TABLE_NAME

    prod_id: str = "prod_id"
    prod_name: str = "prod_name"
    prod_avail: str = "prod_avail"
    prod_store_id: str = "prod_store_id"

    def insert_shelf_status(
        self, prod_id: str, prod_store_id: int, prod_avail: bool, prod_name: str
    ) -> None:
        record = {
            self.prod_id: prod_id,
            self.prod_store_id: prod_store_id,
            self.prod_avail: prod_avail,
            self.prod_name: prod_name,
        }

        self.supabase.table(self.table_name).insert(record).execute()
