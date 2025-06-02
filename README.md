# gym_service
A socket-based bridge between reinforcement learning algorithms and Gymnasium simulation environments.

## 🧠 Motivation
In many real-world reinforcement learning (RL) or imitation learning(IL) projects, the simulation environment (e.g., PyBullet, Isaac Gym, Mujoco, etc.) and the RL algorithm often require different or conflicting Python dependencies. This creates problems such as:

- Environment needs a specific version of python, which clashes with algorithm requirements.
- You may need to  **integrate simulation benchmarks from papers** into your own training pipeline for comparison
- Deployment or development across multiple machines is hindered by dependency entanglement.

To solve these issues, gym_service provides a Client-Server architecture where:

- The server runs the Gymnasium-compatible environment.
- The client runs the algorithm and communicates with the server over sockets using Python pickle serialization.
- Both sides can be run in completely isolated environments ( even on different machines or Docker containers).

## 🚀 Features

- Client-Server architecture to decouple simulation and training logic.
- Minimal dependencies: only requires gymnasium and numpy.
- Supports RGB image rendering (render(mode="rgb_array")) with raw numpy array output.
- Fully compatible with Gymnasium environments, 
- Supports step/reset/render/close API calls just like native Gymnasium environments.

## 🛠️ Installation
Install the package in editable mode so you can develop/test easily:

```bash
git clone https://github.com/Triple-ROCK/gym_service.git
pip install -e .
```


## 📦 Usage
Start the server and client in separate Python scripts or terminals.

**examples/example_server.py**

```python
from gym_service import SocketGymServer

if __name__ == "__main__":
    server = SocketGymServer(host="localhost", port=2333)
    print("[Example Server] Starting server...")
    server.start()
```

**examples/example_client.py**

```python
from gym_service import SocketGymClient

if __name__ == "__main__":
    print("[Example Client] Starting client...")
    env = SocketGymClient(host="localhost", port=2333)

    obs, _ = env.reset()
    print("Reset observation:", obs)

    for _ in range(5):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        print(f"Action: {action}, Obs: {obs}, Reward: {reward}, Terminated: {terminated}")
        if terminated:
            break
    env.close()
```

🔒 License
MIT License © Lei Ouyang

📧 Contact
Feel free to reach out via email: hitlearner@gmail.com
