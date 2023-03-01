from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import requests
import time


class Instagram(webdriver.Chrome):
    def __init__(self, ID, username, password, target_page:str=None):
        self.target_page = target_page
        self.ID = ID
        self.username = username
        self.password = password
        self.is_login = False
        self.main_div = None
        super().__init__('chromedriver.exe')

    def get_main_div(self):
        """It returns the main div of the page."""
        if not self.main_div:
            self.main_div = self.find_element_by_tag_name('div').get_attribute('id')

        return self.main_div

    def not_now_button(self):
        """Click the not now button when we logging in."""
        try:    
            not_now = WebDriverWait(self, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button')))
            not_now.click()
        except Exception as exp:
            pass

    def get_(self, url:str):
        """It goes to the target page."""
        self.main_div = None # the page main div is updated now and main_div should be updated
        self.get(url)

    def another_not_now_button(self):
        """Click the 2nd not now button."""
        WebDriverWait(self, 20).until_not(EC.presence_of_element_located((By.ID, 'react-root')))
        webdriver.ActionChains(self).key_down(Keys.TAB).key_up(Keys.TAB).perform()
        webdriver.ActionChains(self).key_down(Keys.TAB).key_up(Keys.TAB).perform()
        webdriver.ActionChains(self).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()

    def get_instagram(self):
        """It goes to the instagram site."""
        self.get_('https://www.instagram.com/')
    
    def login(self):
        """Sign in to the account"""
        username_input = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')))
        username_input.send_keys(self.username + Keys.TAB + self.password + Keys.ENTER)
        self.is_login = True

    def search_a_page(self, page_id:str):
        """It searches the given page_id and goes to the first result."""
        self.target_page = page_id
        search_input = WebDriverWait(self, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search input"]')))
        search_input.send_keys(page_id)

        first_res = WebDriverWait(self, 20).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{self.get_main_div()}"]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a')))
        first_res.click()

    def go_to_our_page(self):
        """It goes to our page."""
        home_btn = self.find_element_by_xpath(f'//*[@id="{self.get_main_div()}"]'
        '/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[1]/span/img')
        home_btn.click()
        time.sleep(0.2)
        webdriver.ActionChains(self).key_down(Keys.TAB).key_up(Keys.TAB).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()

    def get_info(self):
        """It returns the [posts, followers, followings] of the page"""
        info = WebDriverWait(self, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul._aa_7')))
        pure_info = info.text # for example ['101', 'posts', '48.4K', 'followers', '244', 'following']
        print("pure_info: ", pure_info)
        res = pure_info.lstrip('[').rstrip(']').split()
        print("res: ", res)
        return res[::2] # for example ['101', '48.4K', '244']

    def get_bio(self):
        """It returns the bio of the page"""
        bio = self.find_element_by_css_selector('div[class="_aa_c"]')
        
        return bio.text

    def get_profile_pic(self) -> bytes:
        """It returns the profile pic of the current page."""
        profile_pic = WebDriverWait(self, 20).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{self.get_main_div()}"]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/header/div/div/div/button/img')))
        
        return requests.get(profile_pic.get_attribute('src')).content

    def get_stories(self, from_:str=None) -> list[bytes]:
        """Returns the images of the stories of the page."""
        if from_:
            self.search_a_page(from_)

        time.sleep(5)

        prof = WebDriverWait(self, 30).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{self.get_main_div()}"]'
        '/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/header/div/div/span/img')))

        results = []

        # click on profile to show stories
        prof.click()

        # opens stories and get the picture of them one by one.
        while True:
            try:
                # stop and get the current story
                webdriver.ActionChains(self).key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                story = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img._aa63')))
                link = story.get_attribute('srcset').split(',')[-1].split()[0] # [[link1, quality1], ...] --> -1 is the worst quality
                image = requests.get(link, timeout=10)
                if image:
                    results.append(image.content)
                else:
                    print('Download failed.')
                
                # start story to play
                webdriver.ActionChains(self).key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                time.sleep(0.2)
                # go to the next story
                webdriver.ActionChains(self).key_down(Keys.RIGHT).key_up(Keys.RIGHT).perform()
            
            except StaleElementReferenceException as exp:
                print('done !!!')
                return results
            except TimeoutException as exp:
                print('Time out !!!')
                return results
            except Exception as exp:
                raise exp
    
    def send_direct(self, message:str, to:str):
        """Sends direct message to the specified target_page"""
        
        self.get_('https://www.instagram.com/direct/new/') # got to the direct page

        to_input = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{self.get_main_div()}"]'
        '/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[1]/div/div[2]/input')))
        
        to_input.send_keys(to)
 
        WebDriverWait(self, 20).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{self.get_main_div()}"]'
        '/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div[1]/div/div[1]/span/img'))).click()
        
        time.sleep(5)
        webdriver.ActionChains(self).key_down(Keys.LEFT_SHIFT).key_down(Keys.TAB).key_up(Keys.TAB).key_down(Keys.TAB).key_up(Keys.TAB)\
            .key_down(Keys.TAB).key_up(Keys.TAB).key_up(Keys.LEFT_SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
        
        message_box_text = WebDriverWait(self, 15).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{self.get_main_div()}"]'
        '/div/div[1]/div/div[1]/div/div/div[1]/div[1]/div/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')))
        
        message_box_text.send_keys(message + Keys.ENTER)
