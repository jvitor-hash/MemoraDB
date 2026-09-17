import struct


class AuthenticationOk:
    def encode(self) -> bytes:
        return struct.pack("!I", 0)
    
class ReadyForQuery:
    def __init__(self, status: bytes = b"I"):
        self.status = status
        
    def encode(self) -> bytes:
        return self.status
    
class Query:
    
    def __init__(self, query: str):
        self.query = query
        
    @classmethod
    def decode(cls, payload: bytes):
        # SQL: Payload = b"SELECT * FROM users;\x00" -> Payload = b"SELECT * FROM users;"
        query.payload.rstrip(b"\x00").decode("utf-8")
        
        return cls(query) # Returns a Query Object