import socket
import pickle
import threading
import importlib
import traceback
import gymnasium as gym
from multiprocessing import Process, Pipe
from .utils import serialize_space
from .worker import env_worker
    

class SocketGymServer:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port

    def handle_client(self, conn):
        parent_conn, child_conn = Pipe()
        worker = Process(target=env_worker, args=(child_conn,))
        worker.start()

        with conn:
            try:
                while True:
                    data = self._recv_msg(conn)
                    if data is None:  # an elegant way for socket to close
                        break

                    request = pickle.loads(data)
                    parent_conn.send(request)
                    response = parent_conn.recv()
                    self._send_msg(conn, pickle.dumps(response))
                    if response["status"] == "error":
                        break  # break the while loop when the child process errors

            except Exception as e:
                response = {"status": "error", "message": "Server error: " + str(e) + "\n", "traceback": traceback.format_exc()}
                self._send_msg(conn, pickle.dumps(response))
                
        if worker.is_alive():
            try:
                parent_conn.send(None)  # notify the child process to exit
            except (BrokenPipeError, EOFError):
                pass
        worker.join(timeout=2.0)
        parent_conn.close()
        child_conn.close()

    def _send_msg(self, conn, data_bytes):
        msg = len(data_bytes).to_bytes(4, 'big') + data_bytes
        conn.sendall(msg)

    def _recv_msg(self, conn):
        # receive the first 4 bytes for length head
        raw_msglen = self._recvall(conn, 4)
        if not raw_msglen:
            return None
        msglen = int.from_bytes(raw_msglen, 'big')
        return self._recvall(conn, msglen)

    def _recvall(self, conn, n):
        data = b''
        while len(data) < n:
            packet = conn.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"[Server] Listening on {self.host}:{self.port}")
            while True:
                conn, addr = s.accept()
                print(f"[Server] Connected by {addr}")
                threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()


# run_server.py
if __name__ == "__main__":
    server = SocketGymServer()
    server.start()
