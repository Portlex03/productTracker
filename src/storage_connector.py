import io

from db_api_connector import Connector


STORAGE_NAME = "ProductsPhoto"


class StorageConnector(Connector):
    storage_name: str = STORAGE_NAME

    def upload_product_photo(self, file_bytes: io.BytesIO, product_id: str) -> None:
        self.supabase.storage.from_(self.storage_name).upload(
            file=file_bytes.getvalue(),
            path=f"public/product_{product_id}.png",
        )


storage_connector = StorageConnector()
