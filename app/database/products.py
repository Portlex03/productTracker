from .base_table import Table


class Products(Table):
    def get_products_list(self) -> list[dict]:
        response = self.table.select("*").execute()
        return response.data

    def get_product_id_by_name(self, prod_name: str) -> str:
        response = self.table.select("id").eq("beautifulName", prod_name).execute()
        prod_id = response.data[0]["id"]
        return prod_id

    def insert_products(self, products: list[dict]) -> None:
        for prod in products:
            prod.pop("code")

        db_products = self.get_products_list()
        exist_prod_names = set(prod["name"] for prod in db_products)

        new_products = [prod for prod in products if prod["name"] not in exist_prod_names]

        if new_products:
            self.table.insert(new_products).execute()
