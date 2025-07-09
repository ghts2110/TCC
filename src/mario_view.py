import cv2
import numpy as np
import os

class CustomMarioView():
    def __init__(self, threshold=0.8):
        self.threshold = threshold
        self.templates = self.load_templates()
    

    def load_templates(self):
        templates = {}
        
        #enemie
        enemie = {}
        enemie_path = os.path.join("src", "assets", "enemie")
        if os.path.exists(enemie_path):
            for fname in os.listdir(enemie_path):
                name = os.path.splitext(fname)[0]
                img = cv2.imread(os.path.join(enemie_path, fname))
                if img is not None:
                    enemie[name] = img
        
        templates["enemie"] = enemie

        #item
        item = {}
        item_path = os.path.join("src", "assets", "item")
        if os.path.exists(item_path):
            for fname in os.listdir(item_path):
                name = os.path.splitext(fname)[0]
                img = cv2.imread(os.path.join(item_path, fname))
                if img is not None:
                    item[name] = img
        
        templates["item"] = item

        #misc
        misc = {}
        misc_path = os.path.join("src", "assets", "misc")
        if os.path.exists(misc_path):
            for fname in os.listdir(misc_path):
                name = os.path.splitext(fname)[0]
                img = cv2.imread(os.path.join(misc_path, fname))
                if img is not None:
                    misc[name] = img
        
        templates["misc"] = misc

        #obstacle
        obstacle = {}
        obstacle_path = os.path.join("src", "assets", "obstacle")
        if os.path.exists(obstacle_path):
            for fname in os.listdir(obstacle_path):
                name = os.path.splitext(fname)[0]
                img = cv2.imread(os.path.join(obstacle_path, fname))
                if img is not None:
                    obstacle[name] = img
        
        templates["obstacle"] = obstacle

        #player
        player = {}
        player_path = os.path.join('src', 'assets', 'player')
        if os.path.exists(player_path):
            for fname in os.listdir(player_path):
                name = os.path.splitext(fname)[0]
                img = cv2.imread(os.path.join(player_path, fname))
                if img is not None:
                    player[name] = img
        
        templates["player"] = player

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


    def detect_obstacle_ahead(self, obs, mario_pos):
        """Detecta todos os obstáculos presentes à frente do Mario."""
        x, y = mario_pos
        region = obs[y:y+40, x+16:x+56]  

        detections = {}
        obstacle_templates = self.templates.get("obstacle", {})

        for name, template in obstacle_templates.items():
            result = cv2.matchTemplate(cv2.cvtColor(region, cv2.COLOR_RGB2BGR), template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            detections[f"{name}_ahead"] = max_val >= self.threshold

        return detections
    

    def detect_enemie_ahead(self, obs, mario_pos):
        """Detecta se algum inimigo especificado está à frente do Mario."""
        x, y = mario_pos
        region = obs[y:y+40, x+16:x+56]

        detections = {}
        enemie_templates = self.templates.get("enemie", {})

        for name, template in enemie_templates.items():
            result = cv2.matchTemplate(cv2.cvtColor(region, cv2.COLOR_RGB2BGR), template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            detections[f"{name}_ahead"] = max_val >= self.threshold

        return detections


    def detect_item_ahead(self, obs, mario_pos):
        """Detecta todos os itens presentes à frente do Mario."""
        x, y = mario_pos
        region = obs[y:y+40, x+16:x+56]

        detections = {}
        item_templates = self.templates.get("item", {})

        for name, template in item_templates.items():
            result = cv2.matchTemplate(cv2.cvtColor(region, cv2.COLOR_RGB2BGR), template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            detections[f"{name}_ahead"] = max_val >= self.threshold

        return detections


    def detect_misc_ahead(self, obs, mario_pos):
        """Detecta elementos diversos (bandeiras, etc) à frente do Mario."""
        x, y = mario_pos
        region = obs[y:y+40, x+16:x+56]

        detections = {}
        misc_templates = self.templates.get("misc", {})

        for name, template in misc_templates.items():
            result = cv2.matchTemplate(cv2.cvtColor(region, cv2.COLOR_RGB2BGR), template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            detections[f"{name}_ahead"] = max_val >= self.threshold

        return detections
