# Fully Compatible with LeRobot Framework

To integrate this project with the LeRobot framework, follow the steps below:


## 1.register the ServiceEnv in lerobot/common/envs/factory.py:

Append the following code to the end of the file lerobot/common/envs/factory.py:
``` python
@EnvConfig.register_subclass("service")
@dataclass
class ServiceEnv(EnvConfig):
    task: str = "PushT-v0"
    fps: int = 10
    port: int = 2333
    episode_length: int = 300
    obs_type: str = "pixels_agent_pos"
    render_mode: str = "rgb_array"
    visualization_width: int = 384
    visualization_height: int = 384
    features: dict[str, PolicyFeature] = field(
        default_factory=lambda: {
            "action": PolicyFeature(type=FeatureType.ACTION, shape=(2,)),
            "agent_pos": PolicyFeature(type=FeatureType.STATE, shape=(2,)),
        }
    )
    features_map: dict[str, str] = field(
        default_factory=lambda: {
            "action": ACTION,
            "agent_pos": OBS_ROBOT,
            "environment_state": OBS_ENV,
            "pixels": OBS_IMAGE,
        }
    )

    def __post_init__(self):
        if self.obs_type == "pixels_agent_pos":
            self.features["pixels"] = PolicyFeature(type=FeatureType.VISUAL, shape=(384, 384, 3))
        elif self.obs_type == "environment_state_agent_pos":
            self.features["environment_state"] = PolicyFeature(type=FeatureType.ENV, shape=(16,))

    @property
    def gym_kwargs(self) -> dict:
        return {
            "port": self.port,
            "obs_type": self.obs_type,
            "render_mode": self.render_mode,
            "visualization_width": self.visualization_width,
            "visualization_height": self.visualization_height,
            "max_episode_steps": self.episode_length,
        }

```

## 2. start the server
`python examples/server_example.py`

## 3. Evaluate the PushT Task via Diffusion Policy

In a separate virtual environment where LeRobot is installed, run the following command to evaluate:
``` shell
python lerobot/scripts/eval.py \
    --policy.path=lerobot/diffusion_pusht \
    --env.type=service \
    --eval.batch_size=10 \
    --eval.n_episodes=10 \
    --policy.use_amp=false \
    --policy.device=cuda
```