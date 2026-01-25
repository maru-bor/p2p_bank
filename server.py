import socket
import threading
import time
from cmd_parser import CommandParser
from utils import get_own_ip

MAX_INVALID_COMMAND_ATTEMPTS = 3
INVALID_COMMAND_TIME_WINDOW = 10

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
        self.server_socket = None

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)

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

        invalid_cmd_count = 0
        first_bad_time = None

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

                if response.startswith("ER"):
                    now = time.time()

                    if invalid_cmd_count == 0:
                        invalid_cmd_count = 1
                        first_bad_time = now
                    else:
                        if now - first_bad_time > INVALID_COMMAND_TIME_WINDOW:
                            invalid_cmd_count = 1
                            first_bad_time = now
                        else:
                            invalid_cmd_count += 1

                    if invalid_cmd_count >= MAX_INVALID_COMMAND_ATTEMPTS:
                        self.logger.warning(
                            f"CLIENT {addr} disconnected (too many bad commands)"
                        )
                        client_socket.sendall(
                            b"ER Too many invalid commands. Connection closed.\r\n"
                        )
                        break
                else:
                    invalid_cmd_count = 0
                    first_bad_time = None

                client_socket.sendall(response.encode("utf-8") + b"\r\n")

        except socket.timeout:
            self.logger.error(f"TIMEOUT: {addr}")
            client_socket.sendall(b"ER Timeout limit reached.\r\n")

        except Exception as e:
            error = f"ER Server error: {str(e)}"
            self.logger.error(error)
            try:
                client_socket.sendall(error.encode("utf-8"))
            except Exception:
                pass

        finally:
            client_socket.close()
            self.logger.info(f"CLIENT DISCONNECTED: {addr}")

    def shutdown(self):
        self.logger.info("SERVER SHUTDOWN REQUESTED")
        self.running = False
        self.server_socket.close()