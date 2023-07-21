OPEN_AI_API_KEY='<your key>'
ACCOUNT_EMAIL='<your email>'
ACCOUNT_PASSWORD='<your password>'

import os
from character import *

IMAGES_FOLDER = os.path.expanduser(r"~\Downloads\images")
CHARACTER = Character(
    Character.Anatomy(
        sex=False, # True for male, False for female
        age=80,
        height=Height.SHORT,
        body=Body.FAT,
        eye_color='brown',
        hair_color='brown',
        skin_color='dark',
        race='black',
        hair=Hair.SHORT,
        beard=Hair.NONE
    ),
    Location(
        name='Washington DC',
        physical_features=['dense city']
    ),
    {
        'playing sports': -0.8,
        'cooking': 0.9
    },
    picture_presence=1.0,
    outside_preference=1.0,
    login_frequency=1.0,
    post_interaction_count=6,
    writing_chance=0.8
)