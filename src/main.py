import socket
import threading

HOST = "127.0.0.1"
PORT = 5432


def handle_client(conn: socket.socket, address: tuple[str, int]):
    print(f"[+] Client connected: {address}")

    try:
        while True:
            data = conn.recv(1024)

            if not data:
                break

            message = data.decode("utf-8")

            print(f"[{address}] → {message}")

            response = "world"
            conn.sendall(response.encode("utf-8"))

    except ConnectionResetError:
        print(f"[!] Client forcibly disconnected: {address}")

    finally:
        conn.close()
        print(f"[-] Client disconnected: {address}")


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        # Allows immediate restart after stopping the server.
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server.bind((HOST, PORT))
        server.listen()

        print(f"[*] Server listening on {HOST}:{PORT}")

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
    