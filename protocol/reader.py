import socket
import struct


class MessageReader:
    
    def __init__(self, conn: socket.socket) -> None:
        self.conn = conn
        
    def read_exact(self, size: int) -> bytes:
        data = bytearray()
        
        while len(data) < size:
            chunk = self.conn.recv(size - len(data))
            
            if not chunk:
                raise ConnectionError("Connection closed")
            
            data.extend(chunk)
            
        return bytes(data)
    
    def read_uint32(self) -> int:
        data = self.read_exact(4)
        return struct.unpack("!I", data)[0]
    
    def read_byte(self) -> bytes:
        return self.read_exact(1)
    
    def read_cstring(self) -> str:
        data = bytearray()
        
        while True:
            byte = read_exact(1)
            
            if byte == b"\x00":
                return data.decode("utf-8")
            
            data.extend(byte)
            
    def read_message(self):
        message_type = self.read_byte()
        
        length = self.read_uint32()
        
        # Length includes the 4-bytes length field.
        payload_length = length - 4
        
        payload = self.read_exact(payload_length)
        
        return message_type, payload