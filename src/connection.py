class Connection:

    def __init__(self, conn, address):
        self.conn = conn
        self.address = address

    def close(self):
        print(f"[-] Closing connection: {self.address}")
        self.conn.close()