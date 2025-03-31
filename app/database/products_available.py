from .base_table import Table


class ProductsAvailable(Table):
    def insert_product_avail(self, product_avail: dict) -> None:
        self.table.insert(product_avail).execute()
