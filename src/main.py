import socket
import threading

from protocol import (
    read_startup_message,
    authentication_ok,
    ready_for_query,
)


HOST = "127.0.0.1"
PORT = 5433


def handle_client(conn: socket.socket, address):
    print(f"[+] Connection from {address}")

    try:
        protocol_version, parameters = read_startup_message(conn)

        print(f"[+] Protocol version: {protocol_version}")
        print(f"[+] Parameters: {parameters}")

        user = parameters.get("user")
        database = parameters.get("database")

        print(f"[+] User: {user}")
        print(f"[+] Database: {database}")

        # For now: accept everyone.
        conn.sendall(authentication_ok())

        # Tell the client startup is complete.
        conn.sendall(ready_for_query())

        print("[+] Client is ready for queries")

        # Phase 3 will handle Query messages here.

        while True:
            data = conn.recv(1024)

            if not data:
                break

            print(f"[DEBUG] Received: {data.hex()}")

    except ConnectionError:
        print("[-] Client disconnected")

    finally:
        conn.close()


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

        server.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1,
        )

        server.bind((HOST, PORT))
        server.listen()

        print(f"[*] MemoraDB server")
        print(f"[*] Listening on {HOST}:{PORT}")

        while True:
            conn, address = server.accept()

            thread = threading.Thread(
                target=handle_client,
                args=(conn, address),
                daemon=True,
            )

            thread.start()


if __name__ == "__main__":
    start_server()