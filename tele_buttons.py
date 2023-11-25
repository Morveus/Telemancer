import json
from machine import Pin

class Button:
    def __init__(self, program, button_name, gpio, custom_name=None, repeatable=False, interval=50, longpress=0, url=None, longpress_url=None, token_id=None):
        self.program = program
        self.button_name = button_name
        self.custom_name = custom_name or button_name
        self.repeatable = repeatable
        self.interval = interval
        self.longpress = longpress
        self.url = url
        self.longpress_url = longpress_url
        self.token_id = token_id
        self.gpio = gpio
        
        # Do not ever store these values on the flash
        self.pin = False
        self.held = False

    def to_dict(self):
        return {
            "program": self.program,
            "button_name": self.button_name,
            "custom_name": self.custom_name,
            "repeatable": self.repeatable,
            "interval": self.interval,
            "longpress": self.longpress,
            "url": self.url,
            "longpress_url": self.longpress_url,
            "token_id": self.token_id,
            "gpio": self.gpio
        }

class ButtonConfig:
    def __init__(self, filename='button_config.json'):
        self.filename = filename
        self.buttons = []
        self.load_buttons()

    def load_buttons(self):
        try:
            with open(self.filename, 'r') as file:
                button_data = json.load(file)
                self.buttons = [Button(**data) for data in button_data]
                return self.buttons
        except Exception as e:
            print(e)
            print("We're going to create button config from scratch...")
            self.create_default_config()
            return self.buttons
        
    def init_buttons_pins(self):
        for btn in self.buttons:
            btn.pin = Pin(btn.gpio, Pin.IN, Pin.PULL_DOWN)
            
            if btn.program == 1:
                print("Enabling GPIO PULL_DOWN for button " + btn.button_name)

    def save_buttons(self):
        with open(self.filename, 'w') as file:
            json.dump([button.to_dict() for button in self.buttons], file)

    def add_button(self, button):
        # Check if a button with the same name and program already exists
        if not any(b.button_name == button.button_name and b.program == button.program for b in self.buttons):
            self.buttons.append(button)
            self.save_buttons()
        else:
            print(f"Button with name '{button.button_name}' and program '{button.program}' already exists.")

    def get_buttons(self, program):
        return [button for button in self.buttons if button.program == program]

    def update_button(self, program, button_name, **kwargs):
        for button in self.buttons:
            if button.button_name == button_name and button.program == program:
                for key, value in kwargs.items():
                    setattr(button, key, value)
                break
        self.save_buttons()
    
    def create_default_config(self):
        button_names = ["up", "down", "left", "right", "power", "wifi", "ok", "back", "home"]
        gpios = [12, 13, 14, 15, 16, 17, 18, 19, 21]
        repeatables = [True, True, True, True, False, False, False, False, False]
        custom_names = ["Up", "Down", "Left", "Right", "Power", "WiFi", "OK", "Back", "Home"]

        for program in range(1, 5):  # Programs 1 to 4
            for button_name, gpio, repeatable, custom_name in zip(button_names, gpios, repeatables, custom_names):
                button = Button(
                    program=program, 
                    button_name=button_name, 
                    custom_name=custom_name, 
                    gpio=gpio, 
                    repeatable=repeatable, 
                    interval=200, 
                    longpress=200, 
                    url="http://localhost/changeme", 
                    longpress_url="http://localhost/changeme", 
                    token_id=""
                )
                self.add_button(button)
        
        self.save_buttons()

