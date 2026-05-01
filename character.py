from config import *

class Character:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.gold = START_GOLD
        self.level = START_LEVEL
        self.xp = START_XP
        self.hp = START_HP
        self.max_hp = START_HP
        self.hero_class = START_CLASS
        self.stats = DEFAULT_STATS.copy()
        self.tasks = []
        self.completed_tasks = []
        self.inventory = []
        self.potions = 0
    
    def from_dict(self, data):
        self.gold = data.get("gold", START_GOLD)
        self.level = data.get("level", START_LEVEL)
        self.xp = data.get("xp", START_XP)
        self.hp = data.get("hp", START_HP)
        self.max_hp = data.get("max_hp", START_HP)
        self.hero_class = data.get("hero_class", START_CLASS)
        self.tasks = data.get("tasks", [])
        self.completed_tasks = data.get("completed_tasks", [])
        self.stats = data.get("stats", DEFAULT_STATS.copy())
        self.inventory = data.get("inventory", [])
        self.potions = data.get("potions", 0)
    
    def to_dict(self):
        return {
            "gold": self.gold, "level": self.level, "xp": self.xp,
            "hp": self.hp, "max_hp": self.max_hp, "hero_class": self.hero_class,
            "tasks": self.tasks, "completed_tasks": self.completed_tasks,
            "stats": self.stats, "inventory": self.inventory,
            "potions": self.potions
        }
    
    def add_completed_task(self, task_name, gold_reward, xp_reward):
        from datetime import datetime
        self.completed_tasks.append({
            "name": task_name,
            "gold": gold_reward,
            "xp": xp_reward,
            "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "class": self.hero_class
        })
        if len(self.completed_tasks) > 50:
            self.completed_tasks = self.completed_tasks[-50:]
    
    def get_tasks_for_current_class(self):
        return [t for t in self.tasks if t.get("class", self.hero_class) == self.hero_class]
    
    def get_attack_power(self):
        base = 10 * self.level
        if self.hero_class == "Рыцарь":
            bonus = self.stats["Сила"] * 2
        elif self.hero_class == "Маг":
            bonus = self.stats["Интеллект"] * 3
        else:
            bonus = self.stats["Ловкость"] * 2
        return base + bonus
    
    def add_gold(self, amount):
        self.gold += amount
    
    def add_xp(self, amount):
        self.xp += amount
    
    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
    
    def take_damage(self, damage):
        self.hp -= damage
        return self.hp <= 0
    
    def change_class(self, new_class):
        self.hero_class = new_class
        self.max_hp = int(100 + (self.level - 1) * 20 * CLASS_MULTIPLIERS[new_class]["hp"])
        self.hp = min(self.hp, self.max_hp)
    
    def add_potion(self, amount=1):
        self.potions += amount
    
    def use_potion(self):
        if self.potions > 0 and self.hp < self.max_hp:
            self.potions -= 1
            self.heal(30)
            return True
        return False