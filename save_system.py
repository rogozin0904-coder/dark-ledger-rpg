import json
import os

class SaveSystem:
    def __init__(self):
        self.current_character = "hero"
    
    def get_save_file(self):
        return f"{self.current_character}.json"
    
    def save_game(self, game_data):
        try:
            with open(self.get_save_file(), "w", encoding='utf-8') as f:
                json.dump(game_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            return False
    
    def load_game(self, name):
        self.current_character = name
        try:
            with open(self.get_save_file(), "r", encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            return None
    
    def list_characters(self):
        try:
            return [f.replace(".json", "") for f in os.listdir() if f.endswith(".json")]
        except:
            return []
    
    def get_class_for_character(self, char_name):
        try:
            with open(f"{char_name}.json", "r", encoding='utf-8') as f:
                data = json.load(f)
                return data.get("hero_class", "Рыцарь")
        except:
            return "Рыцарь"