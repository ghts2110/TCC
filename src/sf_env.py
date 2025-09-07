# envs.py
import time
from dataclasses import dataclass
import numpy as np
import retro

from src.actions import spam_start_for_seconds


@dataclass
class EnvConfig:
    game: str
    state: str | None
    discrete: bool
    fps: float
    frame_skip: int = 1        
    render_every: int = 10     
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

        self.obs, self.info = None, {}
        self.reset()
        print(f"Ação: {self.env.action_space} | Obs: {getattr(self.env.observation_space, 'shape', None)}")

    def reset(self):
        try:
            self.obs, self.info = self.env.reset()
        except Exception:
            self.obs = self.env.reset()
            self.info = {}

        self.ep_reward = 0.0
        
        return self.obs, self.info

    def step(self):
        action = spam_start_for_seconds(self.steps, self.env) # <- aleatório

        total_reward = 0.0
        terminated = truncated = False
        info = {}

        for _ in range(max(1, self.cfg.frame_skip)):
            self.obs, reward, terminated, truncated, info = self.env.step(action)
            total_reward += float(reward)
            if terminated or truncated:
                break

        self.ep_reward += total_reward

        # render a cada N passos
        self.env.render()

        # limitador de FPS estável
        if self.cfg.fps > 0:
            now = time.perf_counter()
            dt = (1.0 / self.cfg.fps) - (now - last)
            if dt > 0: time.sleep(dt)
            last = now
            
        return self.obs, total_reward, terminated, truncated, info

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
