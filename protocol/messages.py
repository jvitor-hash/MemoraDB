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
        query = payload.rstrip(b"\x00").decode("utf-8")
        
        return cls(query) # Returns a Query Object
    
def row_description(columns):
    payload = struct.pack("!H", len(columns))
    
    for name in columns:
        name = name.encode()
        
        payload += name + b"\x00"
        payload += struct.pack(
            "!IhIhi h", 
            0,  # Table_oid
            0,  # column_number
            25, # type_oid (text)
            -1, # type_size
            -1, # type_modifier
            0   # format_code (text)
        )
        
    return payload

def data_row(row):
    payload = struct.pack("!H", len(row))
    
    for value in row:
        value = str(value).encode()
        
        payload += struct.pack("!I", len(value))
        payload += value
        
    return payload

def command_complete(count):
    return f"SELECT {count}".encode() + b"\x00"