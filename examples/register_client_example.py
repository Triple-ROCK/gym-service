import gymnasium as gym
import gym_service
import argparse


args = argparse.ArgumentParser()
args.add_argument("--env_id", "-e", type=str, default="PushT-v0")
args.add_argument("--host", type=str, default="localhost")
args.add_argument("--port", type=int, default=2333)
args = args.parse_args()


env_kwargs = {
    "host": args.host,
    "port": args.port,
}
env = gym.make(f"gym_service/{args.env_id}", **env_kwargs)

obs, _ = env.reset()
print("Reset observation:", obs)
for _ in range(5):
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    print(f"Action: {action}, Obs: {obs}, Reward: {reward}, Terminated: {terminated}")
    if terminated:
        break
env.close()