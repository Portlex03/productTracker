from supabase import Client, create_client

from ..config import AppSettings
from .products import ProductsTable
from .storage import FileStorage
from .stores import StoresTable

STORES_TABLE_NAME = "Stores"

PRODUCTS_TABLE_NAME = "Products"

STORAGE_NAME = "ProductsPhoto"

tables = (stores_table, products_table, file_storage) = (
    StoresTable(STORES_TABLE_NAME),
    ProductsTable(PRODUCTS_TABLE_NAME),
    FileStorage(STORAGE_NAME),
)


def connect2db_from_settings(settings: AppSettings) -> None:
    supabase: Client = create_client(settings.supabase_url, settings.supabase_key)
    supabase.auth.sign_in_with_password(
        {"email": settings.user_email, "password": settings.user_password}
    )
    for table in tables:
        table.connect2db(supabase)
