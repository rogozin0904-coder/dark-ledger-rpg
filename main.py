from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from character import Character
from game_logic import GameLogic
from save_system import SaveSystem
from city_view import CityView
import random
from config import *

class RPGApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save_system = SaveSystem()
        self.character = Character()
        self.game_logic = GameLogic(self.character, self.update_ui)
        self.selected_button = None
        self.selected_task_index = None
        self.in_battle = False
        
    def build(self):
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Статистика
        self.info_label = Label(
            text=self.get_stats_text(),
            size_hint_y=None,
            height=50
        )
        self.main_layout.add_widget(self.info_label)
        
        # Город
        self.city = CityView(self.character, self.on_building_click, size_hint_y=0.5)
        self.main_layout.add_widget(self.city)
        
        # Добавление задания
        input_layout = BoxLayout(size_hint_y=None, height=50, spacing=5)
        self.task_input = TextInput(hint_text="Название задания...", multiline=False)
        self.add_btn = Button(text="Добавить", size_hint_x=0.3)
        self.add_btn.bind(on_press=self.add_task)
        input_layout.add_widget(self.task_input)
        input_layout.add_widget(self.add_btn)
        self.main_layout.add_widget(input_layout)
        
        # Список заданий
        self.task_scroll = ScrollView()
        self.task_container = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.task_container.bind(minimum_height=self.task_container.setter('height'))
        self.task_scroll.add_widget(self.task_container)
        self.main_layout.add_widget(self.task_scroll)
        
        # Кнопка завершения
        self.complete_btn = Button(text="Завершить задание", size_hint_y=None, height=50)
        self.complete_btn.bind(on_press=self.complete_task)
        self.main_layout.add_widget(self.complete_btn)
        
        # Кнопка битвы
        self.fight_btn = Button(text="БИТВА", size_hint_y=None, height=50)
        self.fight_btn.bind(on_press=self.start_fight)
        self.main_layout.add_widget(self.fight_btn)
        
        # Battle layout
        self.battle_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.battle_layout.opacity = 0
        self.battle_layout.disabled = True
        
        self.battle_title = Label(text="БИТВА", font_size='24sp', size_hint_y=None, height=60)
        self.battle_layout.add_widget(self.battle_title)
        
        self.battle_stats = Label(text="", size_hint_y=0.3)
        self.battle_layout.add_widget(self.battle_stats)
        
        self.battle_log_label = Label(text="", size_hint_y=0.4, valign='top')
        self.battle_log_label.bind(texture_size=self.battle_log_label.setter('size'))
        self.battle_layout.add_widget(self.battle_log_label)
        
        self.attack_btn = Button(text="АТАКОВАТЬ", size_hint_y=None, height=50)
        self.attack_btn.bind(on_press=self.battle_attack)
        self.battle_layout.add_widget(self.attack_btn)
        
        self.back_btn = Button(text="Выйти", size_hint_y=None, height=50)
        self.back_btn.bind(on_press=self.exit_battle)
        self.battle_layout.add_widget(self.back_btn)
        
        self.main_layout.add_widget(self.battle_layout)
        
        # Загрузка сохранения
        data = self.save_system.load_game(self.save_system.current_character)
        if data:
            self.character.from_dict(data)
            self.update_ui()
        
        self.update_task_list()
        return self.main_layout
    
    def on_building_click(self, building_name):
        pass
    
    def get_stats_text(self):
        return f"Gold: {self.character.gold}   HP: {self.character.hp}/{self.character.max_hp}   Lvl: {self.character.level}   Atk: {self.character.get_attack_power()}"
    
    def update_ui(self):
        self.info_label.text = self.get_stats_text()
        self.update_task_list()
        self.city.update_character_icon()
    
    def update_task_list(self):
        self.task_container.clear_widgets()
        for i, task in enumerate(self.character.get_tasks_for_current_class()):
            if task.get('completed', False):
                continue
            btn = Button(
                text=f"• {task['name']} (+{task['gold']} gold)",
                size_hint_y=None,
                height=40,
                background_normal='',
                background_color=(0.3, 0.3, 0.3, 1)
            )
            btn.task_index = i
            btn.bind(on_press=lambda x, idx=i: self.select_task(idx, x))
            self.task_container.add_widget(btn)
    
    def select_task(self, index, button):
        if self.selected_button:
            self.selected_button.background_color = (0.3, 0.3, 0.3, 1)
        self.selected_button = button
        self.selected_button.background_color = (0.6, 0.8, 0.3, 1)
        self.selected_task_index = index
    
    def add_task(self, instance):
        name = self.task_input.text
        if not name.strip():
            self.show_popup("Ошибка", "Введите название!")
            return
        success, msg = self.game_logic.add_task(name)
        if success:
            self.task_input.text = ""
            self.update_task_list()
            self.selected_button = None
            self.selected_task_index = None
        else:
            self.show_popup("Ошибка", msg)
    
    def complete_task(self, instance):
        if self.selected_task_index is None:
            self.show_popup("Ошибка", "Сначала выберите задание!")
            return
        
        building_index = self.selected_task_index % len(self.city.buildings)
        self.city.move_to_building(building_index, "complete")
        Clock.schedule_once(lambda dt: self.do_complete_task(), 0.6)
    
    def do_complete_task(self):
        success, msg = self.game_logic.complete_task(self.selected_task_index)
        if success:
            current_tasks = self.character.get_tasks_for_current_class()
            if self.selected_task_index < len(current_tasks):
                task_to_remove = current_tasks[self.selected_task_index]
                for i, t in enumerate(self.character.tasks):
                    if t.get("name") == task_to_remove.get("name") and t.get("class") == task_to_remove.get("class"):
                        self.character.tasks.pop(i)
                        break
            self.selected_button = None
            self.selected_task_index = None
            self.update_task_list()
            self.update_ui()
            self.show_popup("Задание выполнено!", msg)
        else:
            self.show_popup("Ошибка", msg)
    
    def start_fight(self, instance):
        self.in_battle = True
        self.enemy_hp = ENEMY_HP_BASE + self.character.level * ENEMY_HP_PER_LEVEL
        self.enemy_power = ENEMY_POWER_BASE + self.character.level * ENEMY_POWER_PER_LEVEL
        self.battle_log = []
        
        self.battle_stats.text = f"ВЫ\nHP: {self.character.hp}/{self.character.max_hp}\nАТАКА: {self.character.get_attack_power()}\n\nВРАГ\nHP: {self.enemy_hp}\nАТАКА: {self.enemy_power}"
        self.battle_log_label.text = ""
        self.battle_layout.opacity = 1
        self.battle_layout.disabled = False
        
        for child in self.main_layout.children:
            if child != self.battle_layout:
                child.opacity = 0
                child.disabled = True
    
    def battle_attack(self, instance):
        damage = random.randint(self.character.get_attack_power() - 5, self.character.get_attack_power() + 5)
        damage = max(1, damage)
        self.enemy_hp -= damage
        self.add_battle_log(f"Вы нанесли {damage} урона! Осталось HP врага: {self.enemy_hp}")
        self.battle_stats.text = f"ВЫ\nHP: {self.character.hp}/{self.character.max_hp}\nАТАКА: {self.character.get_attack_power()}\n\nВРАГ\nHP: {self.enemy_hp}\nАТАКА: {self.enemy_power}"
        
        if self.enemy_hp <= 0:
            self.battle_victory()
            return
        
        enemy_damage = random.randint(self.enemy_power - 3, self.enemy_power + 3)
        self.character.take_damage(enemy_damage)
        self.add_battle_log(f"Враг нанес {enemy_damage} урона! Ваше HP: {self.character.hp}")
        self.battle_stats.text = f"ВЫ\nHP: {self.character.hp}/{self.character.max_hp}\nАТАКА: {self.character.get_attack_power()}\n\nВРАГ\nHP: {self.enemy_hp}\nАТАКА: {self.enemy_power}"
        
        if self.character.hp <= 0:
            self.battle_defeat()
        else:
            self.update_ui()
    
    def add_battle_log(self, text):
        self.battle_log.append(text)
        self.battle_log_label.text = "\n".join(self.battle_log[-10:])
    
    def battle_victory(self):
        reward_gold = random.randint(BATTLE_GOLD_MIN, BATTLE_GOLD_MAX) * self.character.level
        reward_xp = random.randint(BATTLE_XP_MIN, BATTLE_XP_MAX) * self.character.level
        self.character.add_gold(reward_gold)
        self.character.add_xp(reward_xp)
        self.add_battle_log(f"\nПОБЕДА! Получено: {reward_gold} золота и {reward_xp} опыта")
        self.game_logic.check_level_up()
        self.update_ui()
        self.attack_btn.disabled = True
        Clock.schedule_once(lambda dt: self.exit_battle(None), 2)
    
    def battle_defeat(self):
        self.add_battle_log(f"\nВЫ ПОВЕРЖЕНЫ!")
        self.attack_btn.disabled = True
        Clock.schedule_once(lambda dt: self.exit_battle(None), 2)
    
    def exit_battle(self, instance):
        self.in_battle = False
        self.battle_layout.opacity = 0
        self.battle_layout.disabled = True
        for child in self.main_layout.children:
            if child != self.battle_layout:
                child.opacity = 1
                child.disabled = False
        self.update_ui()
    
    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.7, 0.3))
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 1.5)
    
    def on_stop(self):
        self.save_system.save_game(self.character.to_dict())

if __name__ == '__main__':
    RPGApp().run()