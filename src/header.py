from enum import IntEnum
from dataclasses import dataclass
import struct 
import zlib

class MsgType(IntEnum):
    WORKER_JOIN = 1
    HEARTBEAT = 2
    TASK_DISPATCH = 3
    TASK_RESULT = 4
    ACK_RESULT = 5

HEADER_FORMAT = "!BBBBBBH"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

@dataclass
class Header:
    msg_type: MsgType
    task_id: int = 0
    worker_id: int = 0
    attempt_num: int = 0
    frag_index: int = 0
    frag_count: int = 0
    payload_len: int = 0
    # payload_checksum is calculated during packing and unpacking

    def pack(self, payload: bytes = b"") -> bytes:
        self.payload_len = len(payload)
        body = struct.pack(HEADER_FORMAT, self.msg_type, self.task_id,
                           self.worker_id, self.attempt_num, 
                           self.frag_index, self.frag_count, self.payload_len)
        checksum = struct.pack("!I", zlib.crc32(body + payload))
        return body + checksum + payload

    @classmethod
    def unpack(cls, data: bytes) -> tuple["Header", bytes]:
        if len(data) < HEADER_SIZE + 4:
            raise ValueError("too short")
        
        body, (crc,) = data[:HEADER_SIZE], struct.unpack("!I", data[HEADER_SIZE:HEADER_SIZE+4])
        payload = data[HEADER_SIZE + 4:]
        mt, ti, wi, an, fi, fc, pl = struct.unpack(HEADER_FORMAT, body)
        
        if len(payload) != pl:
            raise ValueError("bad payload length")
        if zlib.crc32(body + payload) != crc:
            raise ValueError("bad checksum")
        
        return cls(MsgType(mt), ti, wi, an, fi, fc, pl), payload