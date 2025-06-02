import numpy as np
import gymnasium as gym


def serialize_space(space):
    if isinstance(space, gym.spaces.Box):
        return {
            "type": "Box",
            "low": space.low.tolist(),
            "high": space.high.tolist(),
            "shape": space.shape,
            "dtype": str(space.dtype)
        }
    elif isinstance(space, gym.spaces.Discrete):
        return {
            "type": "Discrete",
            "n": space.n
        }
    elif isinstance(space, gym.spaces.MultiDiscrete):
        return {
            "type": "MultiDiscrete",
            "nvec": space.nvec.tolist()
        }
    elif isinstance(space, gym.spaces.MultiBinary):
        return {
            "type": "MultiBinary",
            "n": space.n
        }
    elif isinstance(space, gym.spaces.Dict):
        return {
            "type": "Dict",
            "spaces": {k: serialize_space(v) for k, v in space.spaces.items()}
        }
    elif isinstance(space, gym.spaces.Tuple):
        return {
            "type": "Tuple",
            "spaces": [serialize_space(s) for s in space.spaces]
        }
    else:
        raise NotImplementedError(f"Unsupported space type: {type(space)}")
    

def deserialize_space(space_dict):
    space_type = space_dict["type"]
    if space_type == "Box":
        return gym.spaces.Box(
            low=np.array(space_dict["low"]),
            high=np.array(space_dict["high"]),
            shape=tuple(space_dict["shape"]),
            dtype=np.dtype(space_dict["dtype"])
        )
    elif space_type == "Discrete":
        return gym.spaces.Discrete(n=space_dict["n"])
    elif space_type == "MultiDiscrete":
        return gym.spaces.MultiDiscrete(nvec=np.array(space_dict["nvec"]))
    elif space_type == "MultiBinary":
        return gym.spaces.MultiBinary(n=space_dict["n"])
    elif space_type == "Dict":
        return gym.spaces.Dict({k: deserialize_space(v) for k, v in space_dict["spaces"].items()})
    elif space_type == "Tuple":
        return gym.spaces.Tuple([deserialize_space(s) for s in space_dict["spaces"]])
    else:
        raise NotImplementedError(f"Unknown space type: {space_type}")