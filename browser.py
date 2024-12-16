import selenium.common.exceptions
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import requests
import time
import os


class Browser:

    def __init__(self, target_account):
        self.url = 'https://www.instagram.com'
        self.account = target_account

        # setup selenium
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get('https://www.google.com/')

        self.driver.get(self.url)

    def accept_cookies(self):
        # wait for cookies warning
        cookies_advise = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located(
            (By.CSS_SELECTOR,  'body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe.x5yr21d.x19onx9a > div > button._a9--._ap36._a9_0')
        ))
        cookies_advise.click()

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

    def load_image_links(self):
        html = self.driver.find_element(By.TAG_NAME, value='html')

        # find div container of image post.
        container_1 = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div'
        container_2 = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/div[2]'

        try:
            image_container = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((
                By.XPATH, container_1
            )))
        except selenium.common.exceptions.TimeoutException:
            image_container = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((
                By.XPATH, container_2
            )))

        try:
            with open(f'downloads/{self.account}/{self.account}_info_posts.txt', mode='r') as posts_info:
                last_post = int(posts_info.read())
                post_number = last_post + 3
                last_post = post_number
        except FileNotFoundError:
            post_number = 4
            last_post = 0

        image_links = self.get_links(post_number, image_container, html, last_post)
        return image_links


    def get_links(self, post_number, image_container, html, last_post):
        image_links = []
        scroll = 0

        while scroll <= post_number:
            if last_post == 0 and scroll == 0:
                divs_per_load = 0
                time.sleep(3)
            else:
                divs_per_load = 4
            if scroll >= last_post - 12:
                image_row = image_container.find_elements(By.CLASS_NAME, value="_ac7v")
                for row in image_row[-divs_per_load:]:
                    time.sleep(0.2)
                    anchor_tags = row.find_elements(By.TAG_NAME, value='a')
                    for anchor in anchor_tags:
                        href = anchor.get_attribute('href')
                        image_links.append(href)
            html.send_keys(Keys.END)

            scroll += 12
            time.sleep(2.5)

        try:
            with open(f'downloads/{self.account}/{self.account}_info_posts.txt', mode='w') as file:
                file.write(str(scroll))
        except FileNotFoundError:
            os.mkdir(f'downloads/{self.account}')
            with open(f'downloads/{self.account}/{self.account}_info_posts.txt', mode='w') as file:
                file.write(str(scroll))

        return image_links

    def get_img_src(self, links):
        images_links = []

        for link in links:
            self.driver.get(link)
            #Ensure that get only images post
            time.sleep(1.93)
            try:
                div_image = self.driver.find_element(By.XPATH, value='/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div[2]/div[1]/article/div/div[1]/div/div/div/div[1]/div[1]')

                img_tag = div_image.find_element(By.TAG_NAME, value='img')

            except selenium.common.exceptions.NoSuchElementException:
                try:
                    time.sleep(1)
                    div_image = self.driver.find_element(By.XPATH,
                    value='/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[1]/div/div/div/div/div[1]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div/div[1]/div[1]')

                    img_tag = div_image.find_element(By.TAG_NAME, value='img')

                except selenium.common.exceptions.NoSuchElementException:
                    print("No image post! pass")
                    pass
                else:
                    images_links.append(img_tag.get_attribute('src'))

            else:
                images_links.append(img_tag.get_attribute('src'))

        return images_links



    def download_images(self, image_links):

        try:
            os.mkdir(f"downloads/{self.account}/posts")

        except FileExistsError:
            pass

        try:
            with open(f'downloads/{self.account}/{self.account}_info_posts.txt', mode='r') as post_info:
                image_number = int(post_info.read())
        except FileNotFoundError:
                image_number = 1

        for link in image_links:
            self.driver.get(link)
            response = requests.get(link)

            with open(f'downloads/{self.account}/posts/{image_number}.jpg', mode='wb') as file:
                file.write(response.content)
                print('saving image')
                image_number += 1
                time.sleep(1.5)


        self.driver.quit()