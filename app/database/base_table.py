from supabase import Client


class Table:
    def __init__(self, table_name: str) -> None:
        self.table_name = table_name
        self.client: Client | None = None

    def connect2db(self, client: Client) -> None:
        self.client = client

    @property
    def table(self):
        if not self.client:
            raise Exception("Client not found.")
        return self.client.table(self.table_name)
