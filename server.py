import socket
import threading

from logger import Logger
from cmd_parser import CommandParser
from utils import get_own_ip


class BankServer:
    def __init__(self, cfg, bank, logger):
        self.host = "127.0.0.1"
        self.port = int(cfg["bank"]["port"])
        self.timeout = float(cfg["timeouts"]["client_idle_timeout_sec"])
        self.own_ip = get_own_ip()
        self.bank = bank
        self.logger = logger
        self.parser = CommandParser(self.own_ip, bank, logger, self.port)
        self.running = True

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)

        print(f"Bank node {self.host}:{self.port}")
        print(f"Bank code (IP): {self.own_ip}")

        self.logger.info(f"SERVER START: {self.host}:{self.port} (IP {self.own_ip})")

        while self.running:
            try:
                client_socket, addr = server_socket.accept()
                self.logger.info(f"CLIENT CONNECTED: {addr}")

                thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, addr),
                    daemon=True,
                )
                thread.start()
            except OSError:
                break


    def handle_client(self, client_socket, addr):
        client_socket.settimeout(self.timeout)

        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break

                try:
                    text = data.decode("utf-8").strip()
                except UnicodeDecodeError:
                    continue

                response = self.parser.parse_and_execute(text)
                client_socket.sendall(response.encode("utf-8") + b"\r\n")

        except socket.timeout:
            self.logger.error(f"TIMEOUT: {addr}")
            client_socket.sendall(b"ER Timeout limit reached.\r\n")

        except Exception as e:
            error = f"ER Server error: {str(e)}"
            self.logger.error(error)
            try:
                client_socket.sendall(error.encode("utf-8"))
            except:
                pass

        finally:
            client_socket.close()
            self.logger.info(f"CLIENT DISCONNECTED: {addr}")

    def shutdown(self):
        self.logger.info("SERVER SHUTDOWN REQUESTED")
        self.running = False