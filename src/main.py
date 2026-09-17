import socket
import threading
import struct

from protocol.reader import MessageReader
from protocol.writer import MessageWriter
from protocol.constants import (
    QUERY,
    TERMINATE,
    AUTHENTICATION,
    READY_FOR_QUERY,
)


HOST = "127.0.0.1"
PORT = 5433


def handle_client(conn, address):
    print(f"[+] Connection: {address}")

    reader = MessageReader(conn)
    writer = MessageWriter(conn)

    try:
        length = reader.read_uint32()

        startup_payload = reader.read_exact(length - 4)

        protocol_version = struct.unpack("!I", startup_payload[:4])[0]

        print(f"[+] PostgreSQL protocol: {protocol_version}")

        # Connection is: AuthenticationOk
        writer.send_message(AUTHENTICATION, struct.pack("!I", 0))


        # Send to client that the server is ready to query.
        writer.send_message(READY_FOR_QUERY, b"I")

        # Message loop
        while True:
            message_type, payload = (reader.read_message())

            if message_type == QUERY:
                query = payload.rstrip(b"\x00").decode("utf-8")
                print(f"[SQL] {query}")

            elif message_type == TERMINATE:
                print("[+] Client terminated")
                break
            else:
                print(f"[?] Message: {message_type!r}")

    except ConnectionError:
        print("[-] Connection closed")

    finally:
        conn.close()


def start_server():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server.bind((HOST, PORT))
        server.listen()

        print(f"[*] MemoraDB running listening on {HOST}:{PORT}")

        while True:
            conn, address = server.accept()

            threading.Thread(
                target=handle_client,
                args=(conn, address),
                daemon=True,
            ).start()


if __name__ == "__main__":
    start_server()