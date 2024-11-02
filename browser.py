from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import os


class Browser:

    def __init__(self, target_account):
        self.url = 'https://www.instagram.com/'
        self.account = target_account

        # setup selenium
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(self.url)

    def login(self):
        # wait for login
        user_input = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located(
            (By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
        ))
        user_input.send_keys(os.environ.get('INSTAGRAM_USER'))
        user_password = self.driver.find_element(By.XPATH, value='//*[@id="loginForm"]/div/div[2]/div/label/input')
        user_password.send_keys(os.environ.get('INSTAGRAM_PASSWORD'))
        login_button  = self.driver.find_element(By.XPATH, value='//*[@id="loginForm"]/div/div[3]')
        login_button.click()
        time.sleep(10)

    def load_target_account(self):

        new_url = f'{self.url}/{self.account}'
        self.driver.get(new_url)