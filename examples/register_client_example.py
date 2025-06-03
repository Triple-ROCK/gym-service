import gymnasium as gym
import gym_service


env_kwargs = {
    "host": "localhost",
    "port": 2333,
}
env = gym.make("gym_service/PushT-v0", **env_kwargs)

obs, _ = env.reset()
print("Reset observation:", obs)
for _ in range(5):
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    print(f"Action: {action}, Obs: {obs}, Reward: {reward}, Terminated: {terminated}")
    if terminated:
        break
env.close()