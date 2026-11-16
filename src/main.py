import threading
import socket
from header import Header, MsgType
from server import Server
from worker import worker

SERVER_ADDR = ("127.0.0.1", 9000)

def main():
    server = Server(SERVER_ADDR)

    t1 = threading.Thread(target=worker, args=(1,), daemon=True)
    t1.start()

    server.main()

if __name__ == "__main__":
    main()