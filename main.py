import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
from dataclasses import dataclass
from enum import Enum

url = "http://127.0.0.1:7860"

@dataclass
class Environment:
    indoors: bool
    temperature: str
    weather: str
    location: str
    time: str

    def get_prompt_text(self):
        return ','.join([
            'inside' if self.indoors else "outside",
            self.weather if not self.indoors else "",
            "at " + self.location,
            self.time
        ])
    
@dataclass 
class Outfit:
    tightness: str # "tight" or "loose"
    parts: str

class Character:
    @dataclass
    # Unchanging physical properties
    class Anatomy:
        sex: bool # False for female, True for male
        age: int
        height: str
        fat_to_muscle_ratio: str
        eye_color: str
        hair_color: str
        skin_color: str
        race: str

    @dataclass
    # Unchanging behavioral properties
    class Personality:
        writing_style: str
        sociability: str # "Shy" vs "open"
        picture_presence: str # "shy" vs "confident" vs "casual"

    @dataclass
    # Defaults or targets/trends for propeties that are subject to change based on context
    class Preferences:
        emotion: str
        hair_style: str
        clothing: Outfit

    @dataclass
    # Changing properties
    class State:
        environment: Environment
        position: str # "sitting" or "standing"
        emotion: str
        clothing: Outfit

    # For str fields, give qualitative descriptions, not quantitative. So instead of "65 inches", say "short"
    def __init__(self, anatomy: Anatomy, personality: Personality, preferences: Preferences) -> None:
        self.anatomy = anatomy
        self.personality = personality
        self.preferences = preferences
        self.state = Character.State(Environment(True, 'warm', 'raining', 'home', 'evening'), "sitting", "happy", self.preferences.clothing)
        
    def get_picture(self):
        prompt = ','.join([
            "masterpiece, best quality, masterpiece",
            self.anatomy.race + ' ' + ("man" if self.anatomy.sex else "woman"),
            self.anatomy.skin_color + " skin",
            f'{self.anatomy.age} years old',
            self.anatomy.height,
            self.anatomy.fat_to_muscle_ratio,
            self.anatomy.eye_color + " eyes",
            self.anatomy.hair_color + " hair",
            self.preferences.hair_style + " hair",
            self.personality.picture_presence + " appearance",
            self.state.environment.get_prompt_text(),
            self.state.position,
            self.state.emotion,
            ','.join(self.preferences.clothing.parts),
            self.preferences.clothing.tightness + " clothing"
        ])
        print('getting picture with following prompt:\n', prompt)
        payload = {
            "prompt": prompt,
            "negative_prompt": "nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name",
            "steps": 28,
            "width": 362,
            "height": 724,
            "sampler_index": "Euler",
            "cfg_scale": 11,
            "seed": -1
        }

        response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

        r = response.json()

        return Image.open(io.BytesIO(base64.b64decode(r['images'][0].split(",",1)[0])))


c = Character(Character.Anatomy(False, 20, "short", "skinny", "green", "brown", "white", "white"),Character.Personality("", "", "casual"), Character.Preferences("angry", "short", Outfit("loose", ["shorts"])))
c.get_picture().show()