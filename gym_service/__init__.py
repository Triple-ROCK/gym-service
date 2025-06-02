from gymnasium.envs.registration import register
from .envs.gym_client import SocketGymClient
from .envs.gym_server import SocketGymServer


__all__ = ["SocketGymClient", "SocketGymServer"]


register(
    id="gym_service/PushT-v0",
    entry_point="gym_service.envs:SocketGymClient",
    max_episode_steps=300,
    nondeterministic=True,
    kwargs={"env_id": "gym_pusht/PushT-v0"},
)