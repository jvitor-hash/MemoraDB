import struct


def recv_exact(conn, size: int) -> bytes:
    """ 
    Forces the recv method to be a method that returns exactly the correct data based on the length otherwise it will return a ConnectionError.
    """
    data = bytearray()

    while len(data) < size:
        chunk = conn.recv(size - len(data))

        if not chunk:
            raise ConnectionError("Connection closed")

        data.extend(chunk)

    return bytes(data)

def read_startup_message(conn):
    # First 4 bytes = total message length
    length_bytes = recv_exact(conn, 4)
    
    length = struct.unpack("!I", length_bytes)[0]
    
    # Length includes the 4-byte length field itself.
    payload = recv_exact(conn, length - 4)
    
    protocol_version = struct.unpack("!I", payload[:4])[0]
    
    parameters_data = payload[4:]
    parameters = {}
    
    parts = parameters_data.rstrip(b"\x00").split(b"\x00")
    
    for i in range(0, len(parts), 2):
        key = parts[i].decode("utf-8")
        value = parts[i + 1].decode("utf-8")
        
        parameters[key] = value
        
    return protocol_version, parameters

def make_message(message_type: bytes, payload: bytes) -> bytes:
    """
    PostgreSQL backend message:
        1 byte  = message type
        4 bytes = length INCLUDING the 4-byte length field
        N bytes = payload
    """
    
    length = 4 + len(payload)
    
    return (message_type + struct.pack("!I", length) + payload)


def authentication_ok() -> bytes:
    # 'R' = Authentication
    # 4 = length
    # 0 = AuthenticationOk
    payload = struct.pack("!I", 0)

    return make_message(b"R", payload)


def ready_for_query() -> bytes:
    # 'Z' = ReadyForQuery
    # 4 + 1 = 5
    # 'I' = idle transaction state

    return make_message(b"Z", b"I")