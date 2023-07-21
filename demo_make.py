from character import *

character = Character(
    Character.Anatomy(
        sex=True, # True for male, False for female
        age=25,
        height=Height.AVERAGE,
        body=Body.AVERAGE,
        eye_color='brown',
        hair_color='grey',
        skin_color='light',
        race='white',
        hair=Hair.SHORT,
        beard=Hair.NONE
    ),
    Location(
        name='Los Angeles',
        physical_features=['beach', 'pier', 'dense city', 'sea']
    ),
    {
        'playing sports': -0.8,
        'cooking': 0.9
    },
    picture_presence=1.0,
    outside_preference=0.5,
    login_frequency=1.0,
    post_interaction_count=6,
    writing_chance=0.8
)