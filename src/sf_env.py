# envs.py
import time
from dataclasses import dataclass
import numpy as np
import retro


@dataclass
class EnvConfig:
    game: str
    state: str | None
    discrete: bool
    fps: float
    frame_skip: int = 1        
    render_every: int = 1     
    seed: int | None = None


class SFEnv:
    def __init__(self, cfg: EnvConfig):
        action_mode = retro.Actions.DISCRETE if getattr(cfg, "discrete", False) else retro.Actions.ALL
        self.env = retro.make(game=cfg.game, state=cfg.state, use_restricted_actions=action_mode)

        try:
            obs, info = self.env.reset()
        except Exception:
            obs = self.env.reset()
            info = {}

        self.cfg = cfg
        self.steps = 0
        self.ep = 0
        self.ep_reward = 0.0
        self._next_frame = time.perf_counter()
        self.last = time.perf_counter()

        print(f"Ação: {self.env.action_space} | Obs: {getattr(self.env.observation_space, 'shape', None)}")


def sf_env(args) -> SFEnv:
    """
    Cria e reseta o ambiente Retro conforme os argumentos.
    Retorna: env, obs, info, steps, ep, ep_reward, last
    """
    cfg = EnvConfig(
        game=args.game,
        state=args.state,
        discrete=getattr(args, "discrete", False),
        fps=args.fps,
        frame_skip=getattr(args, "frame_skip", 1),
        render_every=getattr(args, "render_every", 1),
        seed=getattr(args, "seed", None),
    )

    return SFEnv(cfg)
