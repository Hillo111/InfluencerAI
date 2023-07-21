import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
from dataclasses import dataclass
from enum import Enum
import random
from time import sleep
import openai
from detector import get_objects
import os

OPEN_AI_API_KEY = '<your key>'
openai.api_key = OPEN_AI_API_KEY
if OPEN_AI_API_KEY == '<your key>':
    openai.api_key = os.environ['OPEN_API_KEY']

from bs4 import BeautifulSoup

SD_URL = "http://127.0.0.1:7860"
IMAGE_ENDPOINT = 'sdapi/v1/txt2img'
OPTIONS_ENDPOINT = 'sdapi/v1/options'

def ask_gpt(q):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=q,
        max_tokens=1024
    )
    return 'yes' in response['choices'][0]['text'].lower()

# Takes a time in string form and converts it to a number from 0-86399 (number of seconds in a day -1)
def time2int(time: str):
    time = time.lower()
    if time.endswith('m'):
        m = time.split(' ')[1][0] == 'p'
    else:
        m = False

    ntime = time.split(' ')[0]
    t = 0
    for i, v in enumerate(ntime.split(':')):
        if not (i == 0 and v == '12'):
            t += float(v) * 60 ** (2 - i)
    if m:
        t += 12 * 3600
    return int(t)

class Location:
    def __init__(self, name: str, physical_features=[]):
        self.loc_name = name
        self.physical_features = physical_features

    def get_location_description(self):
        search_loc_name = self.loc_name.lower().replace(" ", "+")
        soup = BeautifulSoup(requests.get(f'https://www.google.com/search?q=current+weather+in+{search_loc_name}').text, features="html.parser")
        weather_desc = soup.find_all(attrs={'class': 'BNeawe tAd8D AP7Wnd'})[1].text.split('\n')[1].lower()
        
        if 'storm' in weather_desc or 'shower' in weather_desc:
            weather_desc = 'rainy'

        # find city on the website. time can actually be accessed here but going deeper shows the sunset and sunrise
        soup = BeautifulSoup(requests.get(f'https://www.timeanddate.com/worldclock/?query={search_loc_name}').text, features="html.parser")
        city_link = 'https://www.timeanddate.com/' + soup.find_all('tr')[1].find('td').find('a').attrs['href']
        soup = BeautifulSoup(requests.get(city_link).text, features="html.parser")
        time = soup.find('span', {'id': 'ct'}).text
        sunrise = soup.find('div', {'id': 'tl-sr-i'}).text
        sunrise = sunrise[:sunrise.index('↑')]
        sunset = soup.find('div', {'id': 'tl-ss-i'}).text
        sunset = sunset[:sunset.index('↑')]

        nt, nsr, nss = time2int(time), time2int(sunrise), time2int(sunset)
        if abs(nt - nsr) < 1800:
            time_desc = 'sunrise'
        elif abs(nt - nss) < 1800:
            time_desc = 'sunset'
        elif nt < nsr or nt > nss:
            time_desc = 'night time'
        else:
            time_desc = 'day time'
        
        return f'{time_desc},{weather_desc} weather,{random.choice(self.physical_features)} in background'
    
    def __str__(self) -> str:
        return self.get_location_description()
    
class Count(Enum):
    NONE, FEW, MANY = range(0, 3)

class Height(Enum):
    SHORT, AVERAGE, TALL = range(0, 3)

class Body(Enum):
    FAT, SKINNY, MUSCULAR, AVERAGE = range(0, 4)

class Hair(Enum):
    SHORT, LONG, NONE = range(3)

class Character:
    @dataclass
    # Unchanging physical properties
    class Anatomy:
        sex: bool # False for female, True for male
        age: int
        height: Height
        body: Body
        eye_color: str
        hair_color: str
        skin_color: str
        race: str # absolutely no fucking way im making an enum for this one bro
        hair: Hair
        beard: Hair
        def get_prompt_text(self, action=''):
            prompt = f'{self.age} y.o. {self.race} {("man" if self.sex else "woman")}, {action},'
            prompt += '(' + ','.join([
                self.skin_color + " skin",
                self.height.name.lower() + " height",
                self.body.name.lower() + " body",
                self.eye_color + " eyes",
                'no tattoos',
            ]) + ':1.4),'
            if self.hair != Hair.NONE:
                prompt += f'{self.hair.name.lower()} {self.hair_color} hair,'
            else:
                prompt += f'(bald, no hair:1.2),'

            if self.beard != Hair.NONE:
                prompt += f'{self.beard.name.lower()} {self.hair_color} beard,'
            else:
                prompt += f'no beard,'
            return prompt

    @dataclass
    # Unchanging behavioral properties
    class Personality:
        writing_style: str
        sociability: str # "Shy" vs "open"
        picture_presence: str # "shy" vs "confident" vs "casual"

    # For str fields, give qualitative descriptions, not quantitative. So instead of "65 inches", say "short". 
    def __init__(self, anatomy: Anatomy, location: Location, topics: dict[str, float], picture_presence: float, outside_preference: float, login_frequency: float, post_interaction_count: int | tuple[int], writing_chance: float) -> None:
        self.anatomy = anatomy
        self.location = location
        self.topics = topics

        self.positive_topics = {}
        for k in self.topics:
            if self.topics[k] > 0:
                self.positive_topics[k] = self.topics[k]

        self.picture_presence = picture_presence
        self.outside_preference = outside_preference
        self.login_frequency = login_frequency
        self.post_interaction_count = post_interaction_count
        self.writing_chance = writing_chance

    def get_prompt(self):
        prompt = ''
        negative_prompt = "text, (deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime:1.4), text, close up, cropped, out of frame, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck,"
        add_topic = False
        add_self = False
        if random.random() < self.picture_presence:
            add_self = True
            if random.random() < 0.5:
                add_topic = True
        else:
            add_topic = True

        if add_topic:
            topic = f'({random.choice(list(self.positive_topics.keys()))}:1.4)'
        else:
            topic = ''
        if add_self:
            prompt += self.anatomy.get_prompt_text(topic) + '(high detailed skin:1.2), full body, fully clothed,'
        else:
            prompt += topic + ',no people,'
            negative_prompt += '(people:1.4),'

        if random.random() < self.outside_preference:
            prompt += f'outside,{self.location.get_location_description()},'
        else:
            prompt += '(inside of building),'

        prompt += '8k uhd, dslr, soft lighting, high quality, film grain, Fujifilm XT3'
        return prompt, negative_prompt

        
    def get_picture(self, prompt, negative_prompt):
        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "steps": 25,
            "width": 384,
            "height": 640,
            "sampler_index": "Euler a",
            "cfg_scale": 5,
            "seed": -1,
            'denoising_strength': 0.35,
            'enable_hr': True,
            'hr_scale': 1.1,
            'hr_upscaler': 'Latent',
            'hr_second_pass_steps': 0,
        }

        response = requests.post(url=f'{SD_URL}/{IMAGE_ENDPOINT}', json=payload)

        r = response.json()

        if 'images' not in r:
            raise KeyError(f"No images received from server. Response status code: {response.status_code}")

        return Image.open(io.BytesIO(base64.b64decode(r['images'][0].split(",",1)[0])))
    
    def get_caption(self, image_prompt):
        print(image_prompt)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"An AI image was generated with the following prompt: \"{image_prompt}\". Write a caption for this image for Instagram. Use emojis. Use at most 1-2 hashtags. Proper grammar is optional. Do not explicitly mention the quality of the image or the camera used. If there is a person depicted in the image, you are that person.",
            max_tokens=1024
        )
        return response['choices'][0]['text'].replace('\n', '').replace('  ', ' ').replace('"', '')
    
    def get_response(self, post):
        prompt = f'You are a {self.anatomy.age} year old {self.anatomy.race} {"male" if self.anatomy.sex else "female"} living in {self.location.loc_name}. '
        prompt += 'You ' + ', '.join(('strongly like' if self.topics[k] > 0.6 else 'like' if self.topics[k] > 0.2 else 'are neutral about' if self.topics[k] > -0.2 else 'dislike' if self.topics[k] > -0.6 else 'strongly dislike') + ' ' + k for k in self.topics) + '. '
        
        all_objects = {}
        for image in post.images:
            objects = get_objects(image)
            for obj in objects:
                if obj not in all_objects:
                    all_objects[obj] = objects[obj]
                else:
                    all_objects[obj] += objects[obj]

        if len(all_objects) > 0:
            prompt += 'An Instagram post has ' + ', '.join(f'{all_objects[k]} {k}(s)' for k in all_objects) + '. '
        if post.caption != '':
            prompt += f'The post has the following caption: "{post.caption}". '
        print(prompt)

        post_responses = {
            'like': ask_gpt(prompt + 'Would you like this post?')
        }
        
        if ask_gpt(prompt + f'You {"always" if self.writing_chance > 0.9 else "usually" if self.writing_chance > 0.7 else "sometimes" if self.writing_chance > 0.4 else "rarely" if self.writing_chance > 0.1 else "never"} write comments in response to posts. Do you write a comment in response in this case?'):
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt + 'Write a comment in response to this post. ',
                max_tokens=1024
            )
            post_responses['comment'] = response['choices'][0]['text'].replace('"', '')
        return post_responses

@dataclass
class Message:
    sender: int
    content: str

if __name__ == '__main__':
    character = Character(
        Character.Anatomy(
            sex=False,
            age=25,
            height=Height.AVERAGE,
            body=Body.AVERAGE,
            eye_color='brown',
            hair_color='black',
            skin_color='light',
            race='chinese',
            hair=Hair.SHORT,
            beard=Hair.NONE
        ),
        Location(
            'Los Angeles',
            ['beach', 'pier', 'dense city', 'sea']
        ),
        {
            'playing sports': -0.8,
            'cooking': 0.9
        },
        picture_presence=0.5,
        outside_preference=0.5,
        login_frequency=0.8,
        post_interaction_count=20,
        writing_chance=0.5
    )
    print(character.get_caption(character.get_prompt()[0]))