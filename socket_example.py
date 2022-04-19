import socket

QUEUE_SIZE = 5
MESSAGE_SIZE = 1024
HOSTNAME = "127.0.0.1"
PORT = 9000
TERMINATE_STRING = "\n"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOSTNAME, PORT))
server_socket.listen(QUEUE_SIZE)
print(f"Listening on {HOSTNAME}:{PORT}")

def read_message(client_socket):
    chunks = []
    while True:
        data = client_socket.recv(MESSAGE_SIZE).decode()
        if data:
            if TERMINATE_STRING in data:
                idx = data.index(TERMINATE_STRING) + len(TERMINATE_STRING)
                chunks.append(data[:idx])
                break
            else:
                chunks.append(data)
        else:
            break
    return "".join(chunks)

while True:
    client_socket, _ = server_socket.accept()
    message = read_message(client_socket)
    response = f"ECHO: {message}"
    print(response)
    client_socket.send(response.encode())
    client_socket.close()