# envs.py
import time
import retro

def sf_env(args):
    """
    Cria e reseta o ambiente Retro conforme os argumentos.
    Retorna: env, obs, info, steps, ep, ep_reward, last
    """
    action_mode = retro.Actions.DISCRETE if getattr(args, "discrete", False) else retro.Actions.ALL
    env = retro.make(game=args.game, state=args.state, use_restricted_actions=action_mode)

    # Algumas versões do retro retornam (obs, info); outras só obs
    try:
        obs, info = env.reset()
    except Exception:
        obs = env.reset()
        info = {}

    steps, ep, ep_reward = 0, 0, 0.0
    last = time.perf_counter()

    print(f"Ação: {env.action_space} | Obs: {getattr(env.observation_space, 'shape', None)}")
    return env, obs, info, steps, ep, ep_reward, last
