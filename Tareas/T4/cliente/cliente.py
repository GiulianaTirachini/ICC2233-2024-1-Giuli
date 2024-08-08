import socket, threading, json, sys, struct
from PyQt6.QtCore import pyqtSignal, QObject

class Cliente(QObject):
    update_lobby_chat = pyqtSignal(str)
    send_username = pyqtSignal(str)

    def __init__(self, port, host):
        super().__init__()
        print('Creando cliente')
        self.port = port
        self.host = host
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connect_to_server()
            self.init_backend()
            self.listen()
        except ConnectionError:
            print('Conexión terminada')
            self.socket_cliente.close()
            self.is_connected = False
            exit()

    def connect_to_server(self):
        self.socket_cliente.connect((self.host, self.port))
        print('Cliente conectado a servidor')

    def listen(self):
        thread = threading.Thread(target=self.listen_thread, daemon=True)
        thread.start()

    def listen_thread(self):
        while self.is_connected:
            try:
                data = self.decodificar_mensaje(self.socket_cliente)
                if data:
                    self.decode_msg_from_server(data)
                else:
                    print('Servidor desconectado.')
                    self.is_connected = False
            except Exception as e:
                print(f"Error en listen_thread: {e}")
                self.is_connected = False

    def send(self, msg):
        try:
            self.socket_cliente.sendall(self.decodificar_mensaje(msg))
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
            return b''.join(chunks).decode('utf-8')
        except Exception as e:
            print(f"Error al decodificar mensaje: {e}")
            return None

    def init_backend(self):
        self.is_connected = True
        self.chat = ''

    def send_init_info_to_chat(self):
        self.send_username.emit(self.username)

    def receive_msg_from_lobby(self, event):
        self.send(event)

    def decode_msg_from_server(self, msg):
        data = json.loads(msg)
        string_to_add = f'{data["username"]}: {data["data"]}\n'
        self.chat += string_to_add
        self.update_lobby_chat.emit(self.chat)

if __name__ == '__main__':
    with open('cliente.json') as config_file:
        config = json.load(config_file)

    host = config["host"]

    if len(sys.argv) != 2:
        print("Uso: python client.py <puerto>")
        sys.exit(1)

    port = int(sys.argv[1])

    client = Cliente(port, host)