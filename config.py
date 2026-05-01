# config.py
import random

# Начальные значения
START_GOLD = 0
START_LEVEL = 1
START_XP = 0
START_HP = 100
START_CLASS = "Рыцарь"

# Характеристики по умолчанию
DEFAULT_STATS = {"Сила": 1, "Интеллект": 1, "Ловкость": 1}

# Множители классов
CLASS_MULTIPLIERS = {
    "Рыцарь": {"hp": 1.3, "attack": 1.2, "Сила": 2, "Ловкость": 1, "Интеллект": 0.5},
    "Маг": {"hp": 0.8, "attack": 1.5, "Сила": 0.5, "Ловкость": 1, "Интеллект": 2},
    "Вор": {"hp": 1.0, "attack": 1.3, "Сила": 1, "Ловкость": 2, "Интеллект": 0.8}
}

# Стили кнопок для разных классов
BUTTON_STYLES = {
    "Рыцарь": {"bg": "#8B7355", "active_bg": "#9B8365", "fg": "#FFD700", "relief": "ridge", "bd": 3},
    "Маг": {"bg": "#8B5A2B", "active_bg": "#9B6A3B", "fg": "#C0C0C0", "relief": "groove", "bd": 2},
    "Вор": {"bg": "#696969", "active_bg": "#797979", "fg": "#E0E0E0", "relief": "sunken", "bd": 2}
}

# Цвета для шкалы опыта
CLASS_COLORS = {"Рыцарь": "#CD7F32", "Маг": "#8B5A2B", "Вор": "#696969"}

# Настройки боя
ENEMY_HP_BASE = 30
ENEMY_HP_PER_LEVEL = 10
ENEMY_POWER_BASE = 5
ENEMY_POWER_PER_LEVEL = 2

# Награды
TASK_REWARD_MIN = 5
TASK_REWARD_MAX = 15
TASK_XP_MIN = 10
TASK_XP_MAX = 20
BATTLE_GOLD_MIN = 20
BATTLE_GOLD_MAX = 50
BATTLE_XP_MIN = 30
BATTLE_XP_MAX = 60

# Стоимость
HEAL_COST = 10
POTION_COST = 20
POTION_HEAL = 30
STAT_UPGRADE_COST = 100

# Здания города
BUILDINGS = [
    {"x": 50, "y": 200, "w": 80, "h": 120, "name": "Таверна"},
    {"x": 160, "y": 180, "w": 90, "h": 140, "name": "Гильдия"},
    {"x": 280, "y": 150, "w": 100, "h": 170, "name": "Замок"},
    {"x": 410, "y": 190, "w": 85, "h": 130, "name": "Кузница"},
    {"x": 520, "y": 210, "w": 75, "h": 110, "name": "Башня"},
    {"x": 620, "y": 180, "w": 80, "h": 140, "name": "Рынок"}
]

# Персонаж
CHARACTER = {
    "icons": {"Рыцарь": "⚔️", "Маг": "🔮", "Вор": "🗡️", "default": "👤"},
    "walk_icons": {"Рыцарь": ["⚔️", "🛡️"], "Маг": ["🔮", "✨"], "Вор": ["🗡️", "🔑"], "default": ["👤", "🚶"]},
    "font_size": 20,
    "color": "#ffdd99",
}

# Эффекты
EFFECTS = {
    "fight": {"Рыцарь": ["⚔️", "💥"], "Маг": ["🔮", "✨"], "Вор": ["🗡️", "💨"], "default": ["✨", "⭐"]},
    "complete": {"Рыцарь": ["⭐", "✨"], "Маг": ["⭐", "🔮"], "Вор": ["⭐", "💰"], "default": ["✨", "⭐"]}
}

# Отладка
DEBUG = {"show_coordinates": False, "print_load_info": True}