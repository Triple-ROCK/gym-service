# worker.py
import traceback
import gymnasium as gym
import importlib
from .utils import serialize_space


def env_worker(conn):
    """Worker process to run a Gym environment."""
    env: gym.Env | None = None
    while True:
        try:
            request = conn.recv()
            if request is None:
                break  # Exit signal

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

                response = {
                    "status": "ok",
                    "observation_space": serialize_space(env.observation_space),
                    "action_space": serialize_space(env.action_space),
                    "render_fps": env.metadata.get("render_fps", None)
                }

            elif env is None:
                response = {"status": "error", "message": "Environment not initialized. Send 'make' first."}

            elif rtype == "reset":
                obs, info = env.reset()
                response = {"status": "ok", "observation": obs, "info": info}

            elif rtype == "step":
                action = payload["action"]
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
                response = {"status": "ok", "image": img}

            elif rtype == "close":
                if env:
                    env.close()
                response = {"status": "ok"}

            else:
                response = {"status": "error", "message": f"Unknown request type: {rtype}"}

            conn.send(response)

        except Exception as e:
            error_info = {
                "status": "error", 
                "message": "Worker Error: " + str(e) + "\n",
                "traceback": traceback.format_exc()
            }

            conn.send(error_info)
            break

    if env:
        env.close()