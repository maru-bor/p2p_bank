import threading
import time
from flask import Flask, render_template



class WebMonitor:
    def __init__(self, bank, server, logger, host, port):
        self.bank = bank
        self.server = server
        self.logger = logger
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.start_time = time.time()
        self._setup_routes()

    def _setup_routes(self):
        @self.app.route("/")
        def index():
            uptime = int(time.time() - self.start_time)
            return render_template(
                "index.html",
                ip=self.bank.bank_ip,
                uptime=uptime,
                clients=self.bank.number_of_clients(),
                total=self.bank.total_amount()
            )

        @self.app.route("/shutdown", methods=["POST"])
        def shutdown():
            exit(0)

    def start(self):
        threading.Thread(
            target=self.app.run,
            kwargs={"host": self.host, "port": self.port},
            daemon=True
        ).start()
