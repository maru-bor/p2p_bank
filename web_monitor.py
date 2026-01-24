import threading
import time
from flask import Flask, render_template_string



class WebMonitor:
    def __init__(self, bank, logger, host="0.0.0.0", port=8080):
        self.bank = bank
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
            return render_template_string("""
                <html>
                <head><title>Bank Node Monitor</title></head>
                <body>
                    <h1>Bank Node Monitor</h1>
                    <p><b>Bank IP:</b> {{ ip }}</p>
                    <p><b>Uptime:</b> {{ uptime }} s</p>
                    <p><b>Total money amount:</b> {{ total }}</p>
                    <p><b>Clients:</b> {{ clients }}</p>
                    
                    <form action="/shutdown" method="post">
                        <button style="color:red;">Shutdown node</button>
                    </form>
                </body>
                </html>
            """,
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
