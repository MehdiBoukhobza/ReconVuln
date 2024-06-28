import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from screenshot_taker import take_screenshot
import os

YELLOW = '\033[33m'
RED = '\033[31m'
RESET = '\033[0m'
BLUE = '\033[34m'

def check_directory(url, take_screenshots, screenshots_folder):
    try:
        response = requests.get(url, allow_redirects=False)  # Disable redirects

        # Check for redirection
        if response.status_code == 301 or response.status_code == 302:
            print(f" --> {url} {BLUE} redirects to {RESET} {response.headers['Location']}")
            return None

        # Check for authentication required
        if response.status_code == 401:
            print(f" --> Directory at {url} requires authentication.")
            authenticate_header = response.headers.get('WWW-Authenticate')
            if authenticate_header:
                print(f" --> Authentication methods supported: {authenticate_header}")
            return None

        # Check for other status codes
        if response.status_code == 403:
            print(f"{RED} --> {url} {RESET}is {RED}forbidden{RESET}.")
            return None

        if response.status_code == 200:
            print(f" --> {url}")
            if take_screenshots:
                take_screenshot(url, screenshots_folder)
            return url

        return None
    except Exception as e:
        print(f"Error checking {url}: {e}")
        return None

def brute_force_directories(base_url, wordlist, test_subdirectories=False, take_screenshots=False):
    print("")
    found_directories = []
    screenshots_folder = "screenshots"

    if take_screenshots and not os.path.exists(screenshots_folder):
        os.makedirs(screenshots_folder)

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(check_directory, f"{base_url}/{directory_name}", take_screenshots, screenshots_folder): directory_name for directory_name in wordlist}
        for future in as_completed(future_to_url):
            result = future.result()
            if result:
                found_directories.append(result)
        
    if test_subdirectories:
        print("\n")
        for directory in found_directories:
            print("")
            print(f" Testing subdirectories of {directory}:")
            brute_force_directories(directory, wordlist, test_subdirectories, take_screenshots)
