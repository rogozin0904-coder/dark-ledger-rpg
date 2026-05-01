from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from config import BUILDINGS, CHARACTER, EFFECTS, DEBUG
import random

class CityView(Widget):
    def __init__(self, character, on_task_complete, **kwargs):
        super().__init__(**kwargs)
        self.character = character
        self.on_task_complete = on_task_complete
        self.animation_running = False
        self.buildings = BUILDINGS
        self.char_x = 0
        self.char_y = 0
        
        with self.canvas.before:
            Color(0.2, 0.3, 0.4, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        self.create_character()
    
    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
    
    def create_character(self):
        icons = CHARACTER["icons"]
        icon = icons.get(self.character.hero_class, icons["default"])
        start = self.buildings[0]
        self.char_x = start["x"] + start["w"]//2 - 10
        self.char_y = start["y"] + start["h"] - 35
        
        self.char_label = Label(
            text=icon,
            font_size=f"{CHARACTER['font_size']}sp",
            color=CHARACTER['color'],
            size_hint=(None, None),
            size=(40, 40),
            pos=(self.char_x, self.char_y)
        )
        self.add_widget(self.char_label)
    
    def move_to_building(self, building_index, effect_type=None):
        if self.animation_running:
            return
        self.animation_running = True
        
        target = self.buildings[building_index]
        target_x = target["x"] + target["w"]//2 - 10
        target_y = target["y"] + target["h"] - 35
        
        start_x = self.char_x
        start_y = self.char_y
        steps = 15
        
        def animate(step):
            if step < 0:
                self.char_label.pos = (target_x, target_y)
                self.char_x = target_x
                self.char_y = target_y
                self.animation_running = False
                if effect_type:
                    self.show_effect(effect_type, target_x + 10, target_y - 10)
                icons = CHARACTER["icons"]
                self.char_label.text = icons.get(self.character.hero_class, icons["default"])
                return
            
            t = step / steps
            new_x = start_x * (1 - t) + target_x * t
            new_y = start_y * (1 - t) + target_y * t
            self.char_label.pos = (new_x, new_y)
            
            walk_icons = CHARACTER["walk_icons"]
            icons = walk_icons.get(self.character.hero_class, walk_icons["default"])
            self.char_label.text = icons[step % 2]
            
            Clock.schedule_once(lambda dt, s=step-1: animate(s), 0.03)
        
        animate(steps)
    
    def show_effect(self, effect_type, x, y):
        effects = EFFECTS
        icons = effects.get(effect_type, {}).get(self.character.hero_class,
                                                 effects.get(effect_type, {}).get("default", ["✨", "⭐"]))
        items = []
        for i, icon in enumerate(icons[:2]):
            label = Label(
                text=icon,
                font_size=f"{18 + i * 4}sp",
                pos=(x + random.randint(-15, 15), y - i * 12)
            )
            self.add_widget(label)
            items.append(label)
        
        def fade(step=10):
            if step <= 0:
                for item in items:
                    self.remove_widget(item)
                return
            for item in items:
                item.pos = (item.x + random.randint(-3, 3), item.y + random.randint(-5, -1))
                item.font_size = f"{step + 5}sp"
            Clock.schedule_once(lambda dt: fade(step - 1), 0.04)
        
        fade()
    
    def update_character_icon(self):
        icons = CHARACTER["icons"]
        icon = icons.get(self.character.hero_class, icons["default"])
        self.char_label.text = icon