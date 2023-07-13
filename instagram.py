from time import sleep, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import keyboard
import mouse
from utils import *
import pygetwindow as gw
import mss
import mss.tools
import time
import random
from PIL import Image
from enum import Enum
from character import Character

def get_when_exists(driver, class_name, timeout=3):
    return WebDriverWait(driver, timeout).until(
    EC.presence_of_element_located((By.CLASS_NAME, class_name))
    )

class PostType(Enum):
    VIDEO, IMAGE, MULTI_IMAGE = range(3)

class Post:
    class_name = ' _ab6k _ab6m _aggc _aatb _aatc _aatd _aatf'.replace(' ', '.')
    def __init__(self, images: list, caption: str) -> None:
        self.images = images
        self.caption = caption

    def __repr__(self):
        return f'Post({len(self.images)} images; caption: "{self.caption.split(chr(10))[0]}" + {len(self.caption.split(chr(10))) - 1} more lines)'

class InstaSession:
    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password
        self.driver = None
        self.reset()

    def reset(self):
        if self.driver:
            self.driver.close()
        self.driver = webdriver.Chrome()
        self.driver.get('https://instagram.com/')
        self.driver.implicitly_wait(10)
        tries = 0
        while True:
            try:
                self.login()
            except:
                if tries < 5:
                    tries += 1
                    print(f'Attempt {tries}/5 Failed login, trying again')
                else:
                    raise Exception('Failed login attempt too many times')
            else:
                break
    
    def login(self):
        get_when_exists(self.driver, "_aa4b._add6._ac4d", 15)
        # log in
        es = self.driver.find_elements(By.CLASS_NAME, "_aa4b._add6._ac4d")
        es[0].clear()
        es[0].send_keys(self.email)
        es[1].clear()
        es[1].send_keys(self.password)
        self.driver.find_element(By.CLASS_NAME, "_acan._acap._acas._aj1-").click()
        sleep(2)
        self.driver.implicitly_wait(3)
        try:
            self.driver.find_elements(By.CLASS_NAME, '_ab2z')[0].find_elements(By.TAG_NAME, 'p')[0]
        except:
            pass
        else:            
            raise KeyError('Instagram rejecting un/pass, wait a couple of minutes and retry')
        self.driver.implicitly_wait(10)

        btn_class = "x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1i0vuye xwhw2v2 xl56j7k x17ydfre x1f6kntn x2b8uid xlyipyv x87ps6o x14atkfc x1d5wrs8 x972fbf xcfux6l x1qhh985 xm0m39n xm3z3ea x1x8b98j x131883w x16mih1h xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 xjbqb8w x1n5bzlp x173jzuc x1yc6y37".replace(" ", '.')
        self.driver.find_element(By.CLASS_NAME, btn_class).click()
        btn_class = "_a9--._a9_1"
        self.driver.find_element(By.CLASS_NAME, btn_class).click()
        
    def make_post(self, img_path: str, caption):
        if not is_windows():
            if img_path.startswith('/'): # it already enters a slash by default, and extra ones mess it up 
                img_path = img_path[1:]
        
        # click on + button
        btn_class = "x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1".replace(" ", '.')
        self.driver.find_elements(By.CLASS_NAME, btn_class)[7].click()
        # Upload image
        btn_class = "_acan _acap _acas _aj1-".replace(" ", ".")
        get_when_exists(self.driver, btn_class)
        sleep(1)
        es = self.driver.find_elements(By.CLASS_NAME, btn_class)
        if is_windows():
            es[-1].click()
            sleep(1)
            keyboard.write(img_path)
            keyboard.press_and_release('enter')
        else:
            es[8].click()
            sleep(1)
            keyboard.press_and_release('/')
            sleep(1)
            keyboard.write(img_path)
            keyboard.press_and_release('enter')
            keyboard.press_and_release('enter')
            sleep(1.5)
            keyboard.press_and_release('enter')
        # sleep(100)
        # Click through posting sequence
        btn_class = 'x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1i0vuye x1f6kntn xwhw2v2 xl56j7k x17ydfre x2b8uid xlyipyv x87ps6o x14atkfc x1d5wrs8 xjbqb8w xm3z3ea x1x8b98j x131883w x16mih1h x972fbf xcfux6l x1qhh985 xm0m39n xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1n5bzlp x173jzuc x1yc6y37'.replace(" ", ".")
        sleep(2)
        self.driver.find_elements(By.CLASS_NAME, btn_class)[-1].click()
        sleep(1)
        self.driver.find_elements(By.CLASS_NAME, btn_class)[-1].click()
        sleep(1)
        e = self.driver.find_element(By.CLASS_NAME, 'xw2csxc x1odjw0f x1n2onr6 x1hnll1o xpqswwc xl565be x5dp1im xdj266r x11i5rnm xat24cr x1mh8g0r x1w2wdq1 xen30ot x1swvt13 x1pi30zi xh8yej3 x5n08af notranslate'.replace(' ', '.'))
        e.click()
        e.clear()
        keyboard.write(caption) # simply sending the keys is not an option, chromium only supports bmp chars
        sleep(1)
        self.driver.find_elements(By.CLASS_NAME, btn_class)[-1].click()
        get_when_exists(self.driver, 'x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye x1ms8i2q xo1l8bm x5n08af x2b8uid x4zkp8e xw06pyt x10wh9bi x1wdrske x8viiok x18hxmgj'.replace(' ', '.'), 20)
        print('detected post got sent')
        sleep(2)
        self.driver.find_element(By.CLASS_NAME, 'x160vmok x10l6tqk x1eu8d0j x1vjfegm'.replace(' ', '.')).find_elements(By.TAG_NAME, 'div')[0].click()
        print('closed out of thing')

    def scrape_posts(self, char: Character = None, n: int = 20, ):
        posts = []
        instagram_window = gw.getActiveWindow()
        # sleep(100)
        for i in range(n):
            post_elem = self.driver.find_elements(By.TAG_NAME, 'article'.replace(' ', '.'))[min(i, 4)]
            
            self.driver.implicitly_wait(0.1)
            caption_expand_class = 'x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm x1roi4f4 x1yc453h x10wh9bi x1wdrske x8viiok x18hxmgj'.replace(' ', '.')
            if len(post_elem.find_elements(By.CLASS_NAME, caption_expand_class)) != 0:
                post_elem.find_element(By.CLASS_NAME, caption_expand_class).click()
            caption_class = '_aacl _aaco _aacu _aacx _aad7 _aade'.replace(' ', '.')
            if len(post_elem.find_elements(By.CLASS_NAME, caption_class)) != 0:
                caption = post_elem.find_elements(By.CLASS_NAME, caption_class)[0].text
            else:
                caption = ''
            self.driver.implicitly_wait(10)

            # self.driver.execute_script('arguments[0].scrollIntoView(true);', post_elem)
            # sleep(1000)
            content_elem = post_elem.find_element(By.CLASS_NAME, 'x6s0dn4 xyzq4qe x78zum5 xdt5ytf x2lah0s xl56j7k x6ikm8r x10wlt62 x1n2onr6'.replace(' ', '.'))
            # this little dance causes posts to sometimes get skipped... or maybe im grabbing the wrong post element
            self.driver.execute_script('arguments[0].scrollIntoView(true);', content_elem)
            sleep(0.5)
            self.driver.execute_script('arguments[0].scrollIntoView(false);', content_elem)
            sleep(0.5)
            self.driver.execute_script('arguments[0].scrollIntoView(true);', content_elem)
            sleep(1)

            count = 0
            self.driver.implicitly_wait(0.1)

            wait_time = 1
            post_type = -1
            
            # multiple images
            if len(post_elem.find_elements(By.CLASS_NAME, '_9zm2')) != 0:
                def condition():
                    nonlocal wait_time
                    # jank and bad
                    if wait_time == 0:
                        return True
                    if len(post_elem.find_elements(By.CLASS_NAME, '_9zm2')) == 0:
                        wait_time = 0
                wait_time = 0.5
                post_type = 1
            # video
            elif len(post_elem.find_elements(By.CLASS_NAME, 'x9f619 x78zum5 x14yjl9h xudhj91 x18nykt9 xww2gxu x1yztbdb xktsk01 x1y1aw1k x1sxyh0 xwib8y2 xurb0ha x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1 x1wunsqr'.replace(' ', '.'))) != 0:
                watch_time = max(random.random() ** 3 * 4, 1) # weighs it to lean towards lower watch times
                wait_time = 1
                condition = lambda : count >= watch_time // wait_time
                post_type = 0
            else:
                condition = lambda : count >= 1
                wait_time = 0
                post_type = -1
            
            images = []
            while not condition():
                wx, wy = instagram_window.box[0:2]
                x, y, width, height = self.driver.execute_script('rect = arguments[0].getBoundingClientRect(); return [rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top]', content_elem)
                width *= 1.743
                height *= 1.706
                # this shit is ultra jank. TODO: properly get content from instagram
                with mss.mss() as sct:
                    sct_img = sct.grab({'left': int(wx + x + 254), 'top': int(wy + y + 228), 'width': int(width), 'height': int(height)})
                    images.append(Image.frombytes('RGB', sct_img.size, sct_img.rgb))
                if post_type == 1 and len(post_elem.find_elements(By.CLASS_NAME, '_9zm2')) != 0:
                    post_elem.find_element(By.CLASS_NAME, '_9zm2').click()
                count += 1
                sleep(wait_time)
            self.driver.implicitly_wait(10)
            post = Post(images, caption)
            if char is not None:
                resp = char.get_response(post)
                print(post)
                interact_buttons = post_elem.find_elements(By.CLASS_NAME, 'x1i10hfl x6umtig x1b1mbwd xaqea5y xav7gou x9f619 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x6s0dn4 xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x1ypdohk x78zum5 xl56j7k x1y1aw1k x1sxyh0 xwib8y2 xurb0ha'.replace(' ', '.'))
                if resp['like']:
                    interact_buttons[0].click()
                    sleep(1)
                else:
                    pass
                if 'comment' in resp and len(interact_buttons) > 1: 
                    interact_buttons[1].click()
                    post_window = self.driver.find_element(By.CLASS_NAME, '_aatb _aate _aatg _aati'.replace(' ', '.'))
                    comment_entry = post_window.find_element(By.TAG_NAME, 'textarea')
                    x, y, width, height = self.driver.execute_script('rect = arguments[0].getBoundingClientRect(); return [rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top]', comment_entry)
                    x += width / 2 + 254 + wx
                    y += height / 2 + 219 + wy + 465
                    mouse.move(int(x), int(y))
                    print('moved into position')
                    sleep(2)
                    mouse.click()
                    keyboard.write(resp['comment'])
                    # comment_entry.send_keys(resp['comment'])
                    sleep(1)
                    commnet_send = post_window.find_element(By.CLASS_NAME, 'x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1i0vuye x1f6kntn xwhw2v2 xl56j7k x17ydfre x2b8uid xlyipyv x87ps6o x14atkfc x1d5wrs8 xjbqb8w xm3z3ea x1x8b98j x131883w x16mih1h x972fbf xcfux6l x1qhh985 xm0m39n xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1n5bzlp x173jzuc x1yc6y37'.replace(' ', '.'))
                    commnet_send.click()
                    sleep(5)
                    self.driver.find_element(By.CLASS_NAME, 'x160vmok x10l6tqk x1eu8d0j x1vjfegm'.replace(' ', '.')).find_elements(By.TAG_NAME, 'div')[0].click()
            posts.append(post)
        
        return posts

if __name__ == "__main__":
    session = InstaSession('reknedilte@gufum.com', 'ploder')
    sleep(10000)
    # session.make_post('C:\\Users\\Max\\Documents\\degeneracy\\set0\\0.png', 'i am cooking....')
    # while True:
    #     sleep(1)