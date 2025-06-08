from gymnasium.envs.registration import register
from .envs import SocketGymClient, SocketGymServer


__all__ = ["SocketGymClient", "SocketGymServer"]


register(
    id="gym_service/PushT-v0",
    entry_point="gym_service.envs:SocketGymClient",
    max_episode_steps=300,
    nondeterministic=True,
    kwargs={"env_id": "gym_pusht/PushT-v0", "env_type": "pusht"},
)

register(
    id="gym_service/adroit-door",
    entry_point="gym_service.envs:SocketGymClient",
    max_episode_steps=300,
    nondeterministic=True,
    kwargs={"env_id": "adroit/adroit-door", "env_type": "adroit"},
)

register(
    id="gym_service/adroit-hammer",
    entry_point="gym_service.envs:SocketGymClient",
    max_episode_steps=300,
    nondeterministic=True,
    kwargs={"env_id": "adroit/adroit-hammer", "env_type": "adroit"},
)

register(
    id="gym_service/adroit-pen",
    entry_point="gym_service.envs:SocketGymClient",
    max_episode_steps=300,
    nondeterministic=True,
    kwargs={"env_id": "adroit/adroit-pen", "env_type": "adroit"},
)