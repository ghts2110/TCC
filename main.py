# random_play.py
import argparse, time
import retro
import numpy as np

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
    sfe = sf_env(args)


    # LOOP PRINCIPAL (RODAR O JOGO)
    while sfe.steps < args.max_steps:
        obs, reward, terminated, truncated, info = sfe.step()

        sfe.steps += 1
        if terminated or truncated:
            ep += 1
            print(f"Episódio {ep} acabou | reward={sfe.ep_reward:.2f}")
            sfe.env.reset()

    sfe.env.close()

if __name__ == "__main__":
    main()
