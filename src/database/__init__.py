from supabase import Client, create_client

from .products import ProductsTable
from .storage import Storage
from .stores import StoresTable

STORES_TABLE_NAME = "Stores"

PRODUCTS_TABLE_NAME = "Products"

STORAGE_NAME = "ProductsPhoto"

tables = (stores_table, products_table, storage_table) = (
    StoresTable(STORES_TABLE_NAME),
    ProductsTable(PRODUCTS_TABLE_NAME),
    Storage(STORAGE_NAME),
)


def connect2db_from_settings(settings) -> None:
    supabase: Client = create_client(settings.supabase_url, settings.supabase_key)
    supabase.auth.sign_in_with_password(
        {"email": settings.user_email, "password": settings.user_password}
    )
    for table in tables:
        table.connect2db(supabase)
