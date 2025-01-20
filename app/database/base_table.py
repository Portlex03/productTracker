from supabase import Client


class Table:
    def __init__(self, table_name: str) -> None:
        self.table_name = table_name
        self.supabase: Client | None = None

    def connect2db(self, supabase: Client) -> None:
        self.supabase = supabase
