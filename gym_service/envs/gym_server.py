import socket
import pickle
import threading
import importlib
import traceback
import gymnasium as gym
from .utils import serialize_space
    

class SocketGymServer:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port

    def handle_client(self, conn):
        env = None
        with conn:
            while True:
                data = self._recv_msg(conn)
                if data is None:  # an elegant way for socket to close
                    break
                try:
                    request = pickle.loads(data)
                    rtype = request.get("type")
                    payload = request.get("payload", {})

                    if rtype == "make":
                        env_type = payload.get("env_type", None)
                        if env_type is not None:
                            package_name = f"gym_{env_type}"
                            try:
                                importlib.import_module(package_name)
                            except ModuleNotFoundError as e:
                                print(f"{package_name} is not installed.")
                                raise e
                            
                        env_id = payload["env_id"]
                        kwargs = payload.get("kwargs", {})
                        env = gym.make(env_id, **kwargs)
                        obs_space = env.observation_space
                        act_space = env.action_space

                        response = {
                            "status": "ok",
                            "observation_space": serialize_space(obs_space),
                            "action_space": serialize_space(act_space),
                            "render_fps": env.metadata.get("render_fps", None)
                        }
                    elif env is None:
                        response = {"status": "error", "message": "Environment not initialized. Send 'make' first."}
                    elif rtype == "reset":
                        obs, info = env.reset()
                        response = {"status": "ok", "observation": obs, "info": info}
                    elif rtype == "step":
                        action = payload['action']
                        obs, reward, terminated, truncated, info = env.step(action)
                        response = {
                            "status": "ok",
                            "observation": obs,
                            "reward": reward,
                            "terminated": terminated,
                            "truncated": truncated,
                            "info": info
                        }
                    elif rtype == "render":
                        img = env.render()
                        response = {
                            "status": "ok",
                            "image": img
                        }
                    else:
                        response = {"status": "error", "message": "Invalid type"}
                except Exception as e:
                    response = {
                        "status": "error", 
                        "message": str(e),
                        "traceback": traceback.format_exc()
                    }

                self._send_msg(conn, pickle.dumps(response))

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
                conn, _ = s.accept()
                print(f"[Server] Got a request {conn}")
                threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()


# run_server.py
if __name__ == "__main__":
    server = SocketGymServer()
    server.start()
