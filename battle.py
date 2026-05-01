from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.app import App
from kivy.core.text import LabelBase
import random
from config import *

# Регистрируем шрифт (если ещё не зарегистрирован)
LabelBase.register(name='GameFont', fn_regular='seguiemj.ttf')

class BattleScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.add_widget(self.layout)
        self.character = None
        self.game_logic = None
        self.enemy_hp = 0
        self.enemy_power = 0
        self.battle_log = []
    
    def start_battle(self, character, game_logic):
        self.character = character
        self.game_logic = game_logic
        self.enemy_hp = ENEMY_HP_BASE + character.level * ENEMY_HP_PER_LEVEL
        self.enemy_power = ENEMY_POWER_BASE + character.level * ENEMY_POWER_PER_LEVEL
        self.battle_log = []
        self.setup_ui()
    
    def setup_ui(self):
        self.layout.clear_widgets()
        
        self.layout.add_widget(Label(
            text="БИТВА!",
            font_name='GameFont',
            font_size='24sp',
            size_hint_y=None,
            height=60
        ))
        
        stats_layout = BoxLayout(size_hint_y=0.3, spacing=20)
        
        player_text = f"ВЫ\n❤️ {self.character.hp}/{self.character.max_hp}\n⚔️ {self.character.get_attack_power()}"
        player_label = Label(text=player_text, font_name='GameFont')
        
        vs_label = Label(text="VS", font_name='GameFont', font_size='30sp', color=[1,0,0,1])
        
        enemy_text = f"ВРАГ\n❤️ {self.enemy_hp}\n⚔️ {self.enemy_power}"
        self.enemy_label = Label(text=enemy_text, font_name='GameFont')
        
        stats_layout.add_widget(player_label)
        stats_layout.add_widget(vs_label)
        stats_layout.add_widget(self.enemy_label)
        self.layout.add_widget(stats_layout)
        
        self.log_scroll = ScrollView(size_hint_y=0.4)
        self.log_label = Label(
            text="",
            font_name='GameFont',
            size_hint_y=None,
            valign='top'
        )
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        self.log_scroll.add_widget(self.log_label)
        self.layout.add_widget(self.log_scroll)
        
        self.attack_btn = Button(
            text="АТАКОВАТЬ",
            font_name='GameFont',
            size_hint_y=None,
            height=50
        )
        self.attack_btn.bind(on_press=self.attack)
        self.layout.add_widget(self.attack_btn)
        
        self.update_log()
    
    def add_log(self, text):
        self.battle_log.append(text)
        self.update_log()
    
    def update_log(self):
        self.log_label.text = "\n".join(self.battle_log[-20:])
    
    def attack(self, instance):
        damage = random.randint(self.character.get_attack_power() - 5, self.character.get_attack_power() + 5)
        damage = max(1, damage)
        self.enemy_hp -= damage
        self.add_log(f"Вы нанесли {damage} урона! Осталось HP врага: {self.enemy_hp}")
        self.enemy_label.text = f"ВРАГ\n❤️ {self.enemy_hp}\n⚔️ {self.enemy_power}"
        
        if self.enemy_hp <= 0:
            self.victory()
            return
        
        enemy_damage = random.randint(self.enemy_power - 3, self.enemy_power + 3)
        self.character.take_damage(enemy_damage)
        self.add_log(f"Враг нанес {enemy_damage} урона! Ваше HP: {self.character.hp}")
        
        if self.character.hp <= 0:
            self.defeat()
        else:
            self.game_logic.update_callback()
    
    def victory(self):
        reward_gold = random.randint(BATTLE_GOLD_MIN, BATTLE_GOLD_MAX) * self.character.level
        reward_xp = random.randint(BATTLE_XP_MIN, BATTLE_XP_MAX) * self.character.level
        self.character.add_gold(reward_gold)
        self.character.add_xp(reward_xp)
        self.add_log(f"\nПОБЕДА! Получено: {reward_gold} золота, {reward_xp} опыта!")
        self.game_logic.check_level_up()
        self.game_logic.update_callback()
        self.attack_btn.disabled = True
        Clock.schedule_once(lambda dt: self.back_to_city(), 2)
    
    def defeat(self):
        self.add_log(f"\nВЫ ПОВЕРЖЕНЫ! Игра окончена...")
        self.attack_btn.disabled = True
        Clock.schedule_once(lambda dt: self.back_to_city(), 2)
    
    def back_to_city(self):
        App.get_running_app().sm.current = 'main'