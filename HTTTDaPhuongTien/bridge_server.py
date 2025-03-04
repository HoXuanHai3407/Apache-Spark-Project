import socket
import threading

class BridgeServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(2)  # Chấp nhận hai kết nối: một từ Spark, một từ YOLOv8
        self.clients = []

    def handle_client(self, client):
        while True:
            data = client.recv(1024)
            if not data:
                break
            # Chuyển tiếp dữ liệu đến client khác
            for c in self.clients:
                if c != client:
                    c.sendall(data)

    def run(self):
        print(f"Bridge server đang lắng nghe trên {self.host}:{self.port}")
        while True:
            client, _ = self.server.accept()
            self.clients.append(client)
            thread = threading.Thread(target=self.handle_client, args=(client,), daemon=True)
            thread.start()

if __name__ == "__main__":
    bridge = BridgeServer('10.254.216.44', 9999)
    bridge.run()

