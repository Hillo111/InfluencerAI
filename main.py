import time
from scheduler import Scheduler
from character import *
from detector import get_objects
from instagram import InstaSession
from time import sleep
import logging
from requests.exceptions import ConnectionError
from config import *
import os
import time

logging.getLogger().setLevel(logging.INFO)

account_email = ACCOUNT_EMAIL
if ACCOUNT_EMAIL == '<your email>':
    account_email = os.environ['ACCOUNT_EMAIL']
account_password = ACCOUNT_PASSWORD
if ACCOUNT_PASSWORD == '<your password>':
    account_password = os.environ['ACCOUNT_PASSWORD']

def do_responses(character: Character):
    session = InstaSession(account_email, account_password)
    session.scrape_posts(character, n=character.post_interaction_count)
    session.driver.close()

def make_post(character: Character):
    prompt, neg_prompt = character.get_prompt()
    logging.info('generating image with prompt: ' + prompt)
    img = character.get_picture(prompt, neg_prompt)
    # img = Image.open('c:\\Users\\Max\\Downloads\\images\\2023-07-10 19-27-03.png')
    img_fn = os.path.join(IMAGES_FOLDER, time.strftime('%Y-%m-%d %H-%M-%S')).replace('/', '\\')
    with open(f"{img_fn}.txt", 'w') as f:
        f.write(prompt + '\n\n' + neg_prompt)
    img_fp = f"{img_fn}.png"
    img.save(img_fp)
    caption = character.get_caption(prompt)
    logging.info('wrote caption: ' + caption)
    
    session = InstaSession(account_email, account_password)
    session.make_post(img_fp, caption)
    session.driver.close()

def check_sd_server():
    try:
        x = requests.get(SD_URL + '/' + OPTIONS_ENDPOINT)
    except ConnectionError:
        raise Exception('SD server unstarted.')
    else:
        if x.status_code == 404:
            raise Exception('SD server returning a 404 response. Make sure you have --api specified in commandline args')
        logging.info('SD server started.')

def set_options(payload):
    return requests.post(url=f'{SD_URL}/{OPTIONS_ENDPOINT}', json=payload)

if __name__ == '__main__':
    character = CHARACTER
    check_sd_server()
    set_options(
        {
            "sd_model_checkpoint": 'realisticVisionV20_v20NoVAE.safetensors',
            'sd_vae': 'vae-ft-mse-840000-ema-pruned.safetensors'
        }
    )
    make_post(character)
    # do_responses(character)
    # posting_scheduler = Scheduler(lambda : make_post(character), (1 + 5 * (1 - character.login_frequency), 2 + 10 * (1 - character.login_frequency))) # min: 1 to 2 hours, max: 3 to 6 hours
    # scrolling_scheduler = Scheduler(lambda : do_responses(character), (0.25 + 0.75 * (1 - character.login_frequency), 0.5 + 1.5 * (1 - character.login_frequency))) # min: 15 to 30 minutes, max: 1 to 2 hours
    # while True:
    #     posting_scheduler.attempt_run()
    #     scrolling_scheduler.attempt_run()
    #     time.sleep(1)