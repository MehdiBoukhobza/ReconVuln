from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

def take_screenshot(url, folder):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        filename = os.path.join(folder, url.replace("://", "_").replace("/", "_") + ".png")
        driver.save_screenshot(filename)
        print(f"Screenshot saved to {filename}")
    except Exception as e:
        print(f"Failed to take screenshot of {url}: {e}")
    finally:
        driver.quit()
