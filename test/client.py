import socket

from protocol import encode_message, decode_message


HOST = "127.0.0.1"
PORT = 8888

MESSAGE_HELLO = 1


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))

    message = encode_message(
        MESSAGE_HELLO,
        b"hello",
    )

    client.sendall(message)

    message_type, payload = decode_message(client)

    print("Type:", message_type)
    print("Payload:", payload.decode())