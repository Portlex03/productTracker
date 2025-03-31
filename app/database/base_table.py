from supabase import Client


class Table:
    def __init__(self) -> None:
        self.table_name = self.__class__.__name__
        self.client: Client | None = None

    @property
    def table(self):
        if not self.client:
            raise Exception("Client not found.")
        return self.client.table(self.table_name)
