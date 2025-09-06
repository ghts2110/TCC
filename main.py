# random_play.py
import argparse, time
import retro

from src.actions import spam_start_for_seconds
from src.sf_env import sf_env


def main():
    # PARSING DE ARGUMENTOS
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="StreetFighterIISpecialChampionEdition-Genesis")
    ap.add_argument("--state", default=None)  
    ap.add_argument("--discrete", action="store_true",
                    help="Usa conjunto de ações DISCRETE (bom p/ Sonic).")
    ap.add_argument("--fps", type=float, default=0.0) # velocidade do jogo
    ap.add_argument("--max-steps", type=int, default=10_000) # duração 
    args = ap.parse_args()


    # CRIAÇÃO DO AMBIENTE
    env, obs, info, steps, ep, ep_reward, last = sf_env(args)


    # LOOP PRINCIPAL (RODAR O JOGO)
    while steps < args.max_steps:
        action = spam_start_for_seconds(steps=steps, env=env)  # <- aleatório
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
