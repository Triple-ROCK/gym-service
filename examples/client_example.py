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
