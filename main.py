# random_play.py
import argparse, time
import retro

def main():
    # PARSING DE ARGUMENTOS
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="StreetFighterIISpecialChampionEdition-Genesis")
    ap.add_argument("--state", default=None)  
    ap.add_argument("--discrete", action="store_true",
                    help="Usa conjunto de ações DISCRETE (bom p/ Sonic).")
    ap.add_argument("--fps", type=float, default=60.0)
    ap.add_argument("--max-steps", type=int, default=10_000)
    args = ap.parse_args()


    # CRIAÇÃO DO AMBIENTE
    action_mode = retro.Actions.DISCRETE if args.discrete else retro.Actions.ALL
    env = retro.make(game=args.game, state=args.state, use_restricted_actions=action_mode)

    obs, info = env.reset()
    steps, ep, ep_reward = 0, 0, 0.0
    last = time.perf_counter()
    print(f"Ação: {env.action_space} | Obs: {getattr(env.observation_space,'shape', None)}")


    # LOOP PRINCIPAL (RODAR O JOGO)
    while steps < args.max_steps:
        action = env.action_space.sample()  # <- aleatório
        obs, reward, terminated, truncated, info = env.step(action)
        ep_reward += reward
        env.render()  # mostra a janela

        steps += 1
        if terminated or truncated:
            ep += 1
            print(f"Episódio {ep} acabou | reward={ep_reward:.2f}")
            ep_reward = 0.0
            obs, info = env.reset()

        if args.fps > 0:
            now = time.perf_counter()
            dt = (1.0 / args.fps) - (now - last)
            if dt > 0: time.sleep(dt)
            last = now

    env.close()

if __name__ == "__main__":
    main()
