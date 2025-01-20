from .base_table import Table


class ProductsTable(Table):
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
