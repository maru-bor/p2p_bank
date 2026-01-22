from server import BankServer

if __name__ == "__main__":
    server = BankServer("0.0.0.0", 65530, 80)
    server.start()