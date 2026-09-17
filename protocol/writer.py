import socket
import struct


class MessageWriter:
    
    def __init__(self, conn: socket.socket) -> None:
        self.conn = conn
        
    def send_message(self, message_type: bytes, payload: bytes = b""):
        length = 4 + len(payload)
        
        message = (
            message_type
            + struct.pack("!I", length)
            + payload
        )
        
        self.conn.sendall(message)