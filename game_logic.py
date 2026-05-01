import random
from config import *

class GameLogic:
    def __init__(self, character, update_callback):
        self.character = character
        self.update_callback = update_callback
    
    def check_level_up(self):
        leveled = False
        while self.character.xp >= self.character.level * 50:
            self.character.xp -= self.character.level * 50
            self.character.level += 1
            self.character.max_hp = int(100 + (self.character.level - 1) * 20 * 
                                       CLASS_MULTIPLIERS[self.character.hero_class]["hp"])
            self.character.hp = self.character.max_hp
            
            stat_to_increase = random.choice(list(self.character.stats.keys()))
            self.character.stats[stat_to_increase] += 1
            
            print(f"LEVEL UP! Уровень {self.character.level}, +1 к {stat_to_increase}")
            leveled = True
        
        if leveled and self.update_callback:
            self.update_callback()
        return leveled
    
    def complete_task(self, task_index):
        current_class_tasks = self.character.get_tasks_for_current_class()
        
        if task_index >= len(current_class_tasks):
            return False, "Задание не найдено"
        
        task = current_class_tasks[task_index]
        if task.get('completed', False):
            return False, "Это задание уже выполнено"
        
        gold_reward = task["gold"]
        xp_reward = random.randint(TASK_XP_MIN, TASK_XP_MAX) * self.character.level
        
        self.character.add_completed_task(task["name"], gold_reward, xp_reward)
        self.character.gold += gold_reward
        self.character.xp += xp_reward
        task['completed'] = True
        
        self.check_level_up()
        if self.update_callback:
            self.update_callback()
        
        return True, f"✅ +{gold_reward}💰\n⭐ +{xp_reward} опыта"
    
    def add_task(self, name):
        if not name.strip():
            return False, "Введите название задания!"
        
        reward = random.randint(TASK_REWARD_MIN, TASK_REWARD_MAX)
        self.character.tasks.append({
            "name": name, 
            "gold": reward, 
            "completed": False, 
            "class": self.character.hero_class
        })
        if self.update_callback:
            self.update_callback()
        return True, ""
    
    def use_potion(self):
        if self.character.use_potion():
            if self.update_callback:
                self.update_callback()
            return True, "Вы выпили зелье и восстановили 30 HP!"
        elif self.character.hp >= self.character.max_hp:
            return False, "У вас уже полное здоровье!"
        elif self.character.potions == 0:
            return False, "У вас нет зелий! Купите их в таверне."
        else:
            return False, "Неизвестная ошибка."