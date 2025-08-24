import os, sys, time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.zelda_env import ZeldaEnv

def main():
    env = ZeldaEnv() 
    env.reset()

    for _ in range(1200):          
        env.render(mode='human')    
        obs, r, done, info = env.step(0)  
        if done:
            env.reset()
        time.sleep(1/60)
    env.close()

if __name__ == "__main__":
    main()
