import socket, threading, json, sys, struct

class Servidor:
    def __init__(self, port, host):
        self.max_recv = 2**16
        self.host = host
        self.port = port
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockets = {}
        self.bind_listen()
        self.accept_connections()

    def bind_listen(self):
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen(250)
        print(f'Servidor escuchando en {self.host} : {self.port}')

    def accept_connections(self):
        thread = threading.Thread(target=self.accept_connections_thread)
        thread.start()

    def accept_connections_thread(self):
        while True:
            client_socket, address = self.socket_server.accept()
            self.sockets[client_socket] = address
            listening_client_thread = threading.Thread(
                target=self.listen_client_thread,
                args=(client_socket, ),
                daemon=True)
            listening_client_thread.start()

    def listen_client_thread(self, client_socket):
        while True:
            try:
                data = self.decodificar_mensaje(client_socket)
                if data:
                    self.chat_management(data)
                else:
                    print('Cliente desconectado.')
                    del self.sockets[client_socket]
                    break
            except Exception as e:
                print(f"Error en listen_client_thread: {e}")
                del self.sockets[client_socket]
                break

    def chat_management(self, msg):
        msg_to_send = {
            "type": msg["type"],
            "username": msg["username"],
            "data": msg["data"]
        }
        for skt in self.sockets.keys():
            self.send(msg_to_send, skt)

    def send(self, value, sock):
        try:
            sock.sendall(self.decodificar_mensaje(value))
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")

    def codificar_mensaje(self, message):
        json_msg = json.dumps(message).encode('utf-8')
        length = len(json_msg)
        header = struct.pack('>I', length)
        chunks = [json_msg[i:i + 25].ljust(25, b'\x00') for i in range(0, length, 25)]
        chunked_message = b''
        for i, chunk in enumerate(chunks):
            chunked_message += struct.pack('>I', i)[:3] + chunk
        return header + chunked_message

    def decodificar_mensaje(self, sock):
        try:
            raw_header = sock.recv(4)
            if not raw_header:
                return None
            length = struct.unpack('>I', raw_header)[0]
            chunks = []
            while length > 0:
                raw_chunk_header = sock.recv(3)
                chunk_length = min(25, length)
                chunk_data = sock.recv(chunk_length)
                chunk_data = chunk_data.rstrip(b'\x00')
                chunks.append(chunk_data)
                length -= len(chunk_data)
            return json.loads(b''.join(chunks).decode('utf-8'))
        except Exception as e:
            print(f"Error al decodificar mensaje: {e}")
            return None

if __name__ == '__main__':
    with open('seridor.json') as config_file:
        config = json.load(config_file)

    host = config["host"]

    if len(sys.argv) != 2:
        print("Uso: python server.py <puerto>")
        sys.exit(1)

    port = int(sys.argv[1])

    server = Servidor(port, host)