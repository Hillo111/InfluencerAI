from time import sleep, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import keyboard

def get_when_exists(driver, class_name, timeout=3):
    return WebDriverWait(driver, timeout).until(
    EC.presence_of_element_located((By.CLASS_NAME, class_name))
    )

# EMAIL = 'fysoru@lyft.live' # need to be more careful with these, it looks like with excessive attempts instagram flags the ip and any signups from it get insta blocked
# or not ? if the login starts failing just wait a bit i guess and it starts working again?
# PASSWORD = 'theppmaster'

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
        self.login()
    
    def login(self):
        get_when_exists(self.driver, "_aa4b._add6._ac4d", 15)
        # log in
        es = self.driver.find_elements(By.CLASS_NAME, "_aa4b._add6._ac4d")
        es[0].clear()
        es[0].send_keys(self.email)
        es[1].clear()
        es[1].send_keys(self.password)
        self.driver.find_element(By.CLASS_NAME, "_acan._acap._acas._aj1-").click()
        btn_class = "x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1i0vuye xwhw2v2 xl56j7k x17ydfre x1f6kntn x2b8uid xlyipyv x87ps6o x14atkfc x1d5wrs8 x972fbf xcfux6l x1qhh985 xm0m39n xm3z3ea x1x8b98j x131883w x16mih1h xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 xjbqb8w x1n5bzlp x173jzuc x1yc6y37".replace(" ", '.')
        self.driver.find_element(By.CLASS_NAME, btn_class).click()
        btn_class = "_a9--._a9_1"
        self.driver.find_element(By.CLASS_NAME, btn_class).click()
        
    def make_post(self, img_path: str):
        if img_path.startswith('/'): # it already enters a slash by default, and extra ones mess it up 
            img_path = img_path[1:]
        
        # click on + button
        btn_class = "x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1".replace(" ", '.')
        self.driver.find_elements(By.CLASS_NAME, btn_class)[7].click()
        # Upload image
        btn_class = "_acan _acap _acas _aj1-".replace(" ", ".")
        es = self.driver.find_elements(By.CLASS_NAME, btn_class)
        while len(es) < 9:
            es = self.driver.find_elements(By.CLASS_NAME, btn_class)
        sleep(1)
        es[8].click()
        sleep(1)
        keyboard.press_and_release('/')
        sleep(1)
        keyboard.write(img_path)
        keyboard.press_and_release('enter')
        keyboard.press_and_release('enter')
        sleep(1.5)
        keyboard.press_and_release('enter')
        # Click through posting sequence
        btn_class = 'x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1i0vuye xwhw2v2 xl56j7k x17ydfre x1f6kntn x2b8uid xlyipyv x87ps6o x14atkfc x1d5wrs8 x972fbf xcfux6l x1qhh985 xm0m39n xm3z3ea x1x8b98j x131883w x16mih1h xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 xjbqb8w x1n5bzlp x173jzuc x1yc6y37'.replace(" ", ".")
        self.driver.find_element(By.CLASS_NAME, btn_class).click()
        self.driver.find_element(By.CLASS_NAME, btn_class).click()
        self.driver.find_element(By.CLASS_NAME, btn_class).click()
        get_when_exists(self.driver, 'x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye x1ms8i2q xo1l8bm x5n08af x2b8uid x4zkp8e xw06pyt x10wh9bi x1wdrske x8viiok x18hxmgj'.replace(' ', '.'), 20)

if __name__ == "__main__":
    session = InstaSession('fysoru@lyft.live', 'theppmaster')
    # session.make_post('/Users/Stas/Downloads/croc.jpeg')