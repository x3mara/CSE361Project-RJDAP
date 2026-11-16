import socket, time
import random
from header import MsgType, Header

SERVER_ADDR = ("127.0.0.1", 9000)

def worker(worker_id: int):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 9100 + worker_id))
    sock.settimeout(1)

    # worker join
    sock.sendto(Header(MsgType.WORKER_JOIN, worker_id=worker_id).pack(),SERVER_ADDR)

    while True:
        try: 
            data, addr = sock.recvfrom(65535)
        except socket.timeout: continue

        header, payload = Header.unpack(data)
        if header.msg_type == MsgType.TASK_DISPATCH:
            sock.sendto(Header(MsgType.TASK_RESULT, worker_id=worker_id, task_id=header.task_id).pack(payload=(random.randint(60,127)).to_bytes()),SERVER_ADDR)

        # heartbeat
        sock.sendto(Header(MsgType.HEARTBEAT, worker_id=worker_id).pack(),SERVER_ADDR)