import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
from dataclasses import dataclass
from enum import Enum
import random
import time

IMAGE_URL = "http://127.0.0.1:7860"
IMAGE_ENDPOINT = 'sdapi/v1/txt2img'

TEXT_URL = 'http://localhost:5000'
TEXT_ENDPOINT = 'api/v1/generate'

@dataclass
class Environment:
    indoors: bool
    class Temperature(Enum):
        FREEZING, COOL, WARM, HOT = range(0, 4)
    temperature: Temperature
    class Weather(Enum):
        SNOWING, RAINING, CLOUDY, SUNNY = range(0, 4)
    weather: Weather
    location: str
    class Time(Enum):
        MORNING, AFTERNOON, EVENING, NIGHT = range(0, 4)
    time: Time

    def get_prompt_text(self):
        return ','.join([
            'inside' if self.indoors else "outside",
            self.weather.name.lower() if not self.indoors else "",
            "at " + self.location,
            self.time.name.lower()
        ])
    
class Count(Enum):
    NONE, FEW, MANY = range(0, 3)
    
@dataclass 
class Outfit:
    parts: list[str] # include descriptions if relevant - "t-shirt" vs "green t-shirt"

class Character:
    @dataclass
    # Unchanging physical properties
    class Anatomy:
        sex: bool # False for female, True for male
        age: int
        class Height(Enum):
            SHORT, AVERAGE, TALL = range(0, 3)
        height: Height
        class Body(Enum):
            FAT, SKINNY, MUSCULAR, AVERAGE = range(0, 4)
        body: Body
        eye_color: str
        hair_color: str
        skin_color: str
        race: str # absolutely no fucking way im making an enum for this one bro
        def get_prompt_text(self):
            return ','.join([
                self.race + ' ' + ("man" if self.sex else "woman"),
                self.skin_color + " skin",
                f'{self.age} year old',
                self.height.name.lower() + " height",
                self.body.name.lower() + " body",
                self.eye_color + " eyes",
                self.hair_color + " hair"
            ])

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
        color: str
        hobbies: list[str]

    @dataclass
    # Changing properties
    class State:
        environment: Environment
        position: str # "sitting" or "standing"
        emotion: str
        clothing: Outfit

    @dataclass
    # Place in the world
    class Description:
        job: str
        wealth: str
        friends: Count

    # For str fields, give qualitative descriptions, not quantitative. So instead of "65 inches", say "short". 
    def __init__(self, anatomy: Anatomy, personality: Personality, preferences: Preferences, description: Description) -> None:
        self.anatomy = anatomy
        self.personality = personality
        self.preferences = preferences
        self.state = Character.State(
            Environment(
                True, 
                Environment.Temperature.WARM, 
                Environment.Weather.SUNNY, 
                'home', 
                Environment.Time.AFTERNOON
            ), 
            "sitting", 
            self.preferences.emotion, 
            self.preferences.clothing
        )
        self.description = description
        
    def get_picture(self):
        prompt = ', '.join([
            "masterpiece, best quality, masterpiece",
            self.anatomy.get_prompt_text(),
            self.preferences.hair_style + " hair",
            self.personality.picture_presence + " appearance",
            self.state.environment.get_prompt_text(),
            self.state.position + " position",
            self.state.emotion + " expression",
            ', '.join("wearing " + p for p in self.preferences.clothing.parts),
            "detailed background"
        ])
        print('getting picture with following prompt:\n', prompt)
        payload = {
            "prompt": prompt,
            # the nsfw token as a negative just doesnt work?? at least not by itself. 
            # you need to specify some details about the character in the prompt to *hopefully* prevent nsfw. 
            # thankfully you don't need to specify a full outfit or anything, just any detail
            "negative_prompt": "nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name",
            "steps": 28,
            "width": 362,
            "height": 724,
            "sampler_index": "Euler",
            "cfg_scale": 11,
            "seed": -1
        }

        response = requests.post(url=f'{IMAGE_URL}/{IMAGE_ENDPOINT}', json=payload)

        r = response.json()

        if 'images' not in r:
            raise KeyError(f"No images received from server. Response status code: {response.status_code}")

        return Image.open(io.BytesIO(base64.b64decode(r['images'][0].split(",",1)[0])))
    
@dataclass
class Message:
    sender: int
    content: str

class Conversation:
    def __init__(self, character: Character) -> None:
        self.character = character
        self.chat_history : list[Message] = []

    def get_description(self):
        return f'You are a {self.character.anatomy.age} year old {"man" if self.character.anatomy.sex else "woman"}. \
        You have a {self.character.personality.writing_style} writing style. You tend to be {self.character.preferences.emotion}. \
        Your hobbies are {", ".join(self.character.preferences.hobbies)}. You are currently {self.character.state.emotion}. \
        You are in a {self.character.state.environment.temperature.name} environment. You are {"inside" if self.character.state.environment.indoors else "outside"}. \
        The weather is {self.character.state.environment.weather.name}. You are at {self.character.state.environment.location}. \
        It is the {self.character.state.environment.time.name}. Your job is {self.character.description.job}. You are {self.character.description.wealth} \
        You have {self.character.description.friends} friends. You are not a robot. You are not an AI. You are real.'
    
    def talk(self):
        prompt = self.get_description() + '\n' + 'Continue the following converstation:\n'
        prompt += "\n".join(("ME: " if msg.sender == -1 else "YOU: ") + msg.content for msg in self.chat_history)
        prompt += "\nYOU: "

        request = {
            'prompt': prompt,
            'max_new_tokens': 250,
            'do_sample': True,
            'temperature': 1.3,
            'top_p': 0.1,
            'typical_p': 1,
            'repetition_penalty': 1.18,
            'top_k': 40,
            'min_length': 0,
            'no_repeat_ngram_size': 0,
            'num_beams': 1,
            'penalty_alpha': 0,
            'length_penalty': 1,
            'early_stopping': False,
            'seed': -1,
            'add_bos_token': True,
            'truncation_length': 2048,
            'ban_eos_token': False,
            'skip_special_tokens': True,
            'stopping_strings': []
        }
        
        response = requests.post(f'{TEXT_URL}/{TEXT_ENDPOINT}', json=request)
        print(response.status_code)
        assert response.status_code == 200
        result = response.json()['results'][0]['text']
        self.chat_history.append(Message(0, result))

        return result
