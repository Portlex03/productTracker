from .base_table import Table


class ProductsTable(Table):
    def insert_product(self, product: dict) -> None:
        self.table.insert(product).execute()
