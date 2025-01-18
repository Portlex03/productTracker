import io

from .base_table import Table


class Storage(Table):
    def upload_product_photo(self, file_bytes: io.BytesIO, product_id: str) -> None:
        self.supabase.storage.from_(self.table_name).upload(
            file=file_bytes.getvalue(),
            path=f"public/product_{product_id}.png",
        )
