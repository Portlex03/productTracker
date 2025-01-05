from supabase import create_client, Client

STORES_TABLE_NAME = "ParfumLeaderStores"

PRODUCTS_TABLE_NAME = "Products"


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
        responce = (
            self.supabase.table(STORES_TABLE_NAME)
            .select("*")
            .eq("chat", chat_id)
            .execute()
        )
        responce_data: list[dict] = responce.data
        store: dict = responce_data[-1]
        return store


class ProductsDBConnector(Connector):
    table_name: str = PRODUCTS_TABLE_NAME

    def insert_product(
        self, prod_id: str, prod_name: str, prod_avail: bool, prod_store_code: str
    ) -> None:
        self.supabase.table(self.table_name).insert(
            {
                "prod_id": prod_id,
                "prod_name": prod_name,
                "prod_avail": prod_avail,
                "prod_store_code": prod_store_code,
            }
        ).execute()


stores_db_connector = StoresDBConnector()
products_db_connector = ProductsDBConnector()
