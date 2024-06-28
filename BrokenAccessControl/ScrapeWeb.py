import requests
from bs4 import BeautifulSoup
import re
import argparse

def extract_urls_from_source(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            anchor_tags = soup.find_all('a', href=True)
            urls = [link['href'] for link in anchor_tags if link.get('href')]

            script_tags = soup.find_all('script')
            for script in script_tags:
                js_code = script.get_text()
                js_urls = re.findall(r"(?:href=|setAttribute\('href',\s*['\"])([^'\"\)]*)", js_code)
                urls.extend(js_urls)

            if urls:
                print(f"Extracted URLs from '{url}':")
                for extracted_url in urls:
                    print(extracted_url)
            else:
                print(f"No URLs found in the source of '{url}'.")
        else:
            print(f"Failed to retrieve the page '{url}'. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while trying to scrape the URL '{url}': {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract URLs from a web page source.")
    parser.add_argument("url", help="The URL of the web page to scrape")

    args = parser.parse_args()

    extract_urls_from_source(args.url)
