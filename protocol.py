import struct


HEADER_SIZE = 5 # The size of the header in bytes (header + payload)

def encode_message(message_type: int, payload: bytes) -> bytes:
    length = len(payload)

    # !BI -> convert python values into raw bytes.
    # ! B I
    # │ │ │
    # │ │ └── unsigned 4-byte integer
    # │ └──── unsigned 1-byte integer
    # └────── network byte order (big-endian)
    header = struct.pack(
        "!BI",
        message_type,
        length,
    )

    return header + payload

def decode_message(conn):
    header = recv_exact(conn, HEADER_SIZE)

    message_type, length = struct.unpack(
        "!BI",
        header,
    )

    payload = recv_exact(conn, length)

    return message_type, payload

def recv_exact(conn, size: int) -> bytes:
    data = bytearray()

    while len(data) < size:
        chunk = conn.recv(size - len(data))

        if not chunk:
            raise ConnectionError("Connection closed")

        data.extend(chunk)

    return bytes(data)