from browser import Browser
from dotenv import load_dotenv

load_dotenv()

browser = Browser(target_account='kodox.m4c')
browser.accept_cookies()
browser.login()
browser.load_target_account()
image_links = browser.get_img_src(links=browser.load_image_links())
if image_links:
    browser.download_images(image_links)
