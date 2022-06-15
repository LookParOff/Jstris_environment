import io
import base64
from PIL import Image
from PIL import ImageEnhance
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service


class Jstris:
    def __init__(self, path_to_chrome_driver, mode_of_game, headless, grayscale):
        self.grayscale = grayscale
        ser = Service(path_to_chrome_driver)
        op = webdriver.ChromeOptions()
        if headless:
            op.add_argument("--headless")
        op.add_argument("--window_position=-1200, 0")
        op.add_argument("--window-size=1920,1080")
        op.add_argument("--start-maximized")
        self.__driver = webdriver.Chrome(service=ser, options=op)
        page_link = 'https://jstris.jezevec10.com/?langSwitch=en'
        self.__driver.get(page_link)
        try:
            self.__change_game_mode(mode_of_game)
        except Exception as e:
            print("I catch some exception while initial parsing")
            print(e)
            self.__driver.close()
            quit()
        self.__game = self.__generator_of_page()
        self.__game_main_screen = self.__driver.find_element(By.XPATH, '//*[@id="myCanvas"]')
        self.available_keys = {0: Keys.ARROW_LEFT, 1: Keys.ARROW_RIGHT,  # left and right moves
                               2: Keys.ARROW_DOWN, 3: Keys.SPACE,  # soft drop, hard drop
                               4: "z", 5: Keys.ARROW_UP,  # rotate left, rotate right
                               6: "a",  # rotate 180
                               7: "c",  # hold
                               8: ""}  # do nothing

    def get_frame_of_game(self):
        try:
            return next(self.__game)
        except Exception as e:
            print("I catch some exception while getting game state")
            print(e)
            self.__driver.close()
            quit()

    def perform_action(self, action):
        self.__game_main_screen.send_keys(self.available_keys[action])

    def close(self):
        self.__driver.close()
        self.__game.close()

    def reset(self):
        self.__game_main_screen.send_keys(Keys.F4)

    def __change_game_mode(self, mode):
        mode_xpaths = {"Practice": '//*[@id="plD"]'}
        play_btn = self.__driver.find_element(By.XPATH, '//*[@id="mnav"]/li[1]/a')
        play_btn.click()
        mode_btn = self.__driver.find_element(By.XPATH, mode_xpaths[mode])
        mode_btn.click()
        self.__change_settings(mode)

    def __change_settings(self, mode):
        setting_btn = self.__driver.find_element(By.XPATH, '//*[@id="settings"]')
        setting_btn.click()
        choose_stat = self.__driver.find_element(By.XPATH, '//*[@id="tabsMenu"]/li[5]/a')
        choose_stat.click()
        select = Select(self.__driver.find_element(By.XPATH, '//*[@id="statGameModeSelect"]'))
        select.select_by_visible_text(mode)
        score_checkbox = self.__driver.find_element(By.XPATH, '//*[@id="stat2"]')
        score_checkbox.click()
        save_btn = self.__driver.find_element(By.XPATH, '//*[@id="settingsSave"]')
        save_btn.click()
        game_screen = self.__driver.find_element(By.XPATH, '//*[@id="myCanvas"]')
        game_screen.send_keys(Keys.F4)

    def __generator_of_page(self):
        while True:
            # base64_image = self.__driver.execute_script(
            #     "return document.getElementById('myCanvas').toDataURL('image/png');")
            # output_image = base64.b64decode(base64_image)
            # img = Image.open(io.BytesIO(output_image))
            # img.save("imimi.png")

            main_canvas = self.__driver.find_element(By.XPATH, '//*[@id="myCanvas"]')
            main_canvas = main_canvas.screenshot_as_png
            main_canvas = Image.open(io.BytesIO(main_canvas))

            # queue_canvas = self.__driver.find_element(By.XPATH, '//*[@id="queueCanvas"]')
            # queue_canvas = queue_canvas.screenshot_as_png
            # queue_canvas = Image.open(io.BytesIO(queue_canvas))

            # hold_canvas = self.__driver.find_element(By.XPATH, '//*[@id="holdCanvas"]')
            # hold_canvas = hold_canvas.screenshot_as_png
            # hold_canvas = Image.open(io.BytesIO(hold_canvas))

            stats_canvas = self.__driver.find_element(By.XPATH, '//*[@id="glstats"]')
            stats_canvas = stats_canvas.screenshot_as_png
            stats_canvas = Image.open(io.BytesIO(stats_canvas))

            if self.grayscale:
                ImageEnhance.Color(main_canvas).enhance(0)
                main_canvas = ImageEnhance.Color(main_canvas).enhance(0)
                # queue_canvas = ImageEnhance.Color(queue_canvas).enhance(0)
                # hold_canvas = ImageEnhance.Color(hold_canvas).enhance(0)
                stats_canvas = ImageEnhance.Color(stats_canvas).enhance(0)
            # yield main_canvas, queue_canvas, hold_canvas, stats_canvas
            yield main_canvas, stats_canvas
