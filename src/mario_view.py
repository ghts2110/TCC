import cv2
import numpy as np
import os

class CustomMarioView():
    def __init__(self, threshold=0.8):
        self.threshold = threshold
        self.templates = self.load_templates()
    
    def category_templates(self, folder_name):
        category = {}
        category_path = os.path.join("src", "assets", folder_name)

        if os.path.exists(category_path):
            for fname in os.listdir(category_path):
                if fname.endswith(".png"):
                    name = os.path.splitext(fname)[0]
                    path = os.path.join(category_path, fname)
                    img = cv2.imread(path)
                    if img is not None:
                        category[name] = img

        return category


    def load_templates(self):
        templates = {}
        
        categories = ["enemie", "item", "misc", "obstacle", "player"]
        for category in categories:
            templates[category] = self.category_templates(category)
        return templates


    def is_start_screen(self, obs, template_path="src/assets/logo_mario.png"):
        """Detecta se o logo 'SUPER MARIO BROS' está presente no frame."""
        frame = cv2.cvtColor(obs, cv2.COLOR_RGB2BGR)
        result = cv2.matchTemplate(frame, cv2.imread(template_path), cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        return max_val > self.threshold


    def find_mario(self, obs):
        """Retorna a posição (x, y) do Mario no frame, ou None se não encontrado."""
        obs_bgr = cv2.cvtColor(obs, cv2.COLOR_RGB2BGR)

        best_score = 0
        best_pos = None

        player_templates = self.templates.get("player", {})
        for _, template in player_templates.items():
            result = cv2.matchTemplate(obs_bgr, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            if max_val > best_score and max_val >= self.threshold:
                best_score = max_val
                best_pos = max_loc

        return best_pos


    def detect_category_ahead(self, category, obs, mario_pos):
        """Detecta todos os elementos de uma categoria à frente do Mario."""
        x, y = mario_pos
        region = obs[y-10:y+50, x-10:x+80]

        templates = self.templates.get(category, {})
        detections = {}

        region_bgr = cv2.cvtColor(region, cv2.COLOR_RGB2BGR)

        for name, template in templates.items():
            result = cv2.matchTemplate(region_bgr, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            detections[f"{name}_ahead"] = max_val >= self.threshold

        return detections     

    def detect_obstacle_ahead(self, obs, mario_pos):
        """Detecta todos os obstáculos presentes à frente do Mario."""
        return self.detect_category_ahead("obstacle", obs, mario_pos)
    

    def detect_enemie_ahead(self, obs, mario_pos):
        """Detecta se algum inimigo especificado está à frente do Mario."""
        return self.detect_category_ahead("enemie", obs, mario_pos)


    def detect_item_ahead(self, obs, mario_pos):
        """Detecta todos os itens presentes à frente do Mario."""
        return self.detect_category_ahead("item", obs, mario_pos)


    def detect_misc_ahead(self, obs, mario_pos):
        """Detecta elementos diversos (bandeiras, etc) à frente do Mario."""
        return self.detect_category_ahead("misc", obs, mario_pos)
