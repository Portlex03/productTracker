from supabase import create_client, Client

STORES_TABLE_NAME = "ParfumLeaderStores"

PRODUCTS_TABLE_NAME = "ProductsTracking"


class Connector:
    supabase: Client

    def connect(
        self, supabase_url: str, supabase_key: str, user_email: str, user_password: str
    ) -> None:
        self.supabase = create_client(supabase_url, supabase_key)

        self.supabase.auth.sign_in_with_password(
            {"email": user_email, "password": user_password}
        )


class StoresDBConnector(Connector):
    def get_store_data_from_chat_id(self, chat_id: int) -> dict:
        response = (
            self.supabase
            .table(STORES_TABLE_NAME)
            .select("*")
            .eq("chat", chat_id)
            .execute()
        )
        response_data: list[dict] = response.data
        store: dict = response_data[-1]
        return store


class ProductsDBConnector(Connector):
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


stores_db_connector = StoresDBConnector()
products_db_connector = ProductsDBConnector()
