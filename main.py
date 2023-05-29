from instagram import InstaSession
from character import Character, Conversation

c = Conversation(Character.make_from_archetype(Character.Archetype.AVERAGE))

img_fp = "/Users/Stas/Documents/degeneracy/pic.png"
c.character.get_picture().save(img_fp)
session = InstaSession('fysoru@lyft.live', 'theppmaster')
session.make_post(img_fp)