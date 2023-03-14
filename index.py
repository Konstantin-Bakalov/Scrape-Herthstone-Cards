import time
import requests
import io
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, 'wb') as f:
            image.save(f, 'PNG')

    except Exception as e: 
        print('Downloading failed', e)

def scroll_down(driver):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight - 2500);')

def get_images(driver):
    driver.get('https://hearthstone.blizzard.com/en-us/cards?set=classic-cards')
    scroll_down(driver)
    time.sleep(5)

    images_url = []
    images = driver.find_elements(By.CLASS_NAME, 'CardImage')
    for image in images:
         img_src = image.get_attribute('src')
         images_url.append(img_src)

    return images_url
    
images_url = get_images(driver)

for index, url in enumerate(images_url):
    download_image('', url, f'{index}.png')