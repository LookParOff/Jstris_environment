import io
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service


def change_mode(driver, mode):
    mode_xpaths = {"Practice": '//*[@id="plD"]'}
    play_btn = driver.find_element(By.XPATH, '//*[@id="mnav"]/li[1]/a')
    play_btn.click()
    mode_btn = driver.find_element(By.XPATH, mode_xpaths[mode])
    mode_btn.click()
    change_settings(driver, mode)


def change_settings(driver, mode):
    setting_btn = driver.find_element(By.XPATH, '//*[@id="settings"]')
    setting_btn.click()
    choose_stat = driver.find_element(By.XPATH, '//*[@id="tabsMenu"]/li[5]/a')
    choose_stat.click()
    select = Select(driver.find_element(By.XPATH, '//*[@id="statGameModeSelect"]'))
    select.select_by_visible_text(mode)
    score_checkbox = driver.find_element(By.XPATH, '//*[@id="stat2"]')
    score_checkbox.click()
    save_btn = driver.find_element(By.XPATH, '//*[@id="settingsSave"]')
    save_btn.click()
    game_screen = driver.find_element(By.XPATH, '//*[@id="myCanvas"]')
    game_screen.send_keys(Keys.F4)


def load_page(mode="Practice"):
    ser = Service(r"C:\Program Files (x86)\Google\chromedriver.exe")
    op = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ser, options=op)
    driver.set_window_position(-1200, 0)
    driver.maximize_window()
    page_link = 'https://jstris.jezevec10.com/?langSwitch=en'
    driver.get(page_link)
    change_mode(driver, mode)
    return driver


def generator_of_page():
    driver = load_page()
    while True:
        main_canvas = driver.find_element(By.XPATH, '//*[@id="myCanvas"]')
        main_canvas = main_canvas.screenshot_as_png
        buffer = io.BytesIO(main_canvas)
        main_canvas = Image.open(buffer)
        queue_canvas = driver.find_element(By.XPATH, '//*[@id="queueCanvas"]')
        queue_canvas = queue_canvas.screenshot_as_png
        buffer = io.BytesIO(queue_canvas)
        queue_canvas = Image.open(buffer)
        stats_canvas = driver.find_element(By.XPATH, '//*[@id="glstats"]')
        stats_canvas = stats_canvas.screenshot_as_png
        buffer = io.BytesIO(stats_canvas)
        stats_canvas = Image.open(buffer)
        yield main_canvas, queue_canvas, stats_canvas


smth = []
get_images = generator_of_page()
time.sleep(1)
for indd in range(3):
    time.sleep(5)
    game_frame = next(get_images)
    game_frame[0].save(f"canvas{indd}.png")
    smth.append(game_frame)

del get_images
print(smth)
