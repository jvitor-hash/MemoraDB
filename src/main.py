import socket
import threading

from protocol import encode_message, decode_message


HOST = "127.0.0.1"
PORT = 8888

MESSAGE_HELLO = 1
MESSAGE_WORLD = 2


def handle_client(conn: socket.socket, address):
    print(f"[+] Client connected: {address}")

    try:
        while True:
            message_type, payload = decode_message(conn)

            print(
                f"[{address}] "
                f"type={message_type} "
                f"payload={payload!r}"
            )

            if message_type == MESSAGE_HELLO:
                response = encode_message(
                    MESSAGE_WORLD,
                    b"world",
                )

                conn.sendall(response)

    except ConnectionError:
        print(f"[-] Client disconnected: {address}")

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