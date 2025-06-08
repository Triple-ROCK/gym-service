import gymnasium as gym
import numpy as np
import socket
import pickle
from .utils import deserialize_space


class SocketGymClient(gym.Env):
    metadata = {"render_modes": ["rgb_array"]}  # only RGB array rendering supported

    def __init__(self, env_id="CartPole-v1", env_type=None, 
                       host='127.0.0.1', port=65432, **env_kwargs):
        super().__init__()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Connecting to server at {}:{}".format(host, port))
        self.sock.connect((host, port))

        env_kwargs = env_kwargs or {}
        env_kwargs["render_mode"] = self.metadata["render_modes"][0]
        response = self._send_request({
            "type": "make",
            "payload": {
                "env_id": env_id,
                "env_type": env_type,
                "kwargs": env_kwargs
            }
        })

        self.observation_space = deserialize_space(response["observation_space"])
        self.action_space = deserialize_space(response["action_space"])
        self.metadata = SocketGymClient.metadata.copy()
        self.metadata["render_fps"] = response["render_fps"]  # compatible with lerobot

    def _send_request(self, request):
        data = pickle.dumps(request)
        msg = len(data).to_bytes(4, 'big') + data
        self.sock.sendall(msg)

        raw_len = self._recvall(4)
        if not raw_len:
            raise RuntimeError("Server closed connection")
        msglen = int.from_bytes(raw_len, 'big')
        data = self._recvall(msglen)

        response = pickle.loads(data)
        if response['status'] != 'ok':
            print("\n[Trackback from worker]:\n", response['traceback'], "\n")
            raise RuntimeError(response.get('message', 'Unknown error'))
        
        return response
    
    def _recvall(self, n):
        data = b''
        while len(data) < n:
            packet = self.sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        response = self._send_request({"type": "reset", "payload": {}})
        obs = response["observation"]
        info = response.get("info", {})
        return obs, info

    def step(self, action):
        response = self._send_request({"type": "step", "payload": {"action": action}})
        observation = response["observation"]
        reward = response["reward"]
        terminated = response["terminated"]
        truncated = response["truncated"]
        info = response["info"]
        return observation, reward, terminated, truncated, info
    
    def render(self):
        response = self._send_request({"type": "render", "payload": {}})
        return response["image"]

    def close(self):
        self.sock.close()


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    env = SocketGymClient()
    obs, _ = env.reset()
    print("Reset:", obs)

    for step in range(5):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        print(f"Step: {step}, Action: {action}, Obs: {obs}, Reward: {reward}, terminated: {terminated}")

        img = env.render()
        plt.imshow(img)
        plt.axis('off')
        plt.show()

    env.close()