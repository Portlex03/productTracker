from supabase import Client, create_client

from ..config import AppSettings
from .products_available import ProductsAvailable
from .products import Products
from .stores import Stores

tables = (stores_table, products_available_table, products_table) = (
    Stores(),
    ProductsAvailable(),
    Products(),
)


def connect2db_with_settings(settings: AppSettings) -> None:
    client: Client = create_client(settings.supabase_url, settings.supabase_key)
    client.auth.sign_in_with_password(
        {"email": settings.user_email, "password": settings.user_password}
    )
    for table in tables:
        table.client = client
