from browser import Browser
from dotenv import load_dotenv

load_dotenv()

browser = Browser(target_account='puppys.heaven')
browser.login()
browser.load_target_account()
