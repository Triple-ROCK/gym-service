# gym_service
A socket-based bridge between reinforcement(Imitation) learning algorithms and Gymnasium simulation environments.

## 🧠 Motivation
In many real-world reinforcement learning (RL) or imitation learning(IL) projects, the simulation environment (e.g., PyBullet, Isaac Gym, Mujoco, etc.) and the RL algorithm often require different or conflicting Python dependencies. This creates problems such as:

- Environment needs a specific version of python, which clashes with the training pipeline.
- **integrating simulation benchmarks from papers** into your own pipeline for comparison becomes cumbersome.
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
- Supports the full standard Gym API: reset, step, render, close.
- Support vectorized env using separate threads

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
import matplotlib.pyplot as plt

if __name__ == "__main__":
    print("[Example Client] Starting client...")
    env = SocketGymClient(env_id="CartPole-v1", host="localhost", port=2333)

    obs, _ = env.reset()
    print("Reset observation:", obs)

    for _ in range(5):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        print(f"Action: {action}, Obs: {obs}, Reward: {reward}, Terminated: {terminated}")
        
        img = env.render()
        plt.imshow(img)
        plt.axis('off')
        plt.show()
    env.close()
```

**Or you can simply register the client as a gym env**
```python
from gymnasium.envs.registration import register
import gymnasium as gym

register(
    id="gym_service/PushT-v0",
    entry_point="gym_service.envs:SocketGymClient",
    max_episode_steps=300,
    nondeterministic=True,
    kwargs={"env_id": "gym_pusht/PushT-v0"},
)
...
gym.make("gym_service/PushT-v0")
```

## 🤝 Compatible with Lerobot
The package is fully compatible with lerobot, See [lerobot_compatible.md](./lerobot_compatible.md)

## 🧪 TODO
1. improve image rendering efficiency
2. improve pickele usage

## 🔒 License
MIT License © Lei Ouyang

## 📧 Contact
Feel free to reach out via email: hitlearner@gmail.com
