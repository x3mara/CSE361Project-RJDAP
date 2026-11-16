import socket
import random
from header import Header, MsgType

class Server:
    def __init__(self, addr):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(addr)
        self.sock.settimeout(0.1)
        self.workers = dict()

    def main(self):
        while True:
            try: 
                data, addr = self.sock.recvfrom(65535)
            except socket.timeout:
                data = None

            if data is not None:
                header, payload = Header.unpack(data)
                match header.msg_type:
                    case MsgType.WORKER_JOIN:
                        if header.worker_id in self.workers.keys():
                            print("worker already working")
                        else:
                            self.workers[header.worker_id] = addr
                            print(f"added: {header.worker_id}")
                    case MsgType.TASK_RESULT:
                        print(f"{header.worker_id}: {payload}")

            if random.random() < 0.05 and len(self.workers) > 0:
                self.sock.sendto(Header(MsgType.TASK_DISPATCH, 
                                   worker_id=1,
                                   task_id=random.randint(1,100)).pack(),
                                   self.workers[1])