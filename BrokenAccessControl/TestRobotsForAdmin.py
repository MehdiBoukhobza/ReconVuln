import requests
import urllib3
from urllib.parse import urljoin
import argparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_admin_paths(url):
    robots_url = urljoin(url, "/robots.txt")
    response = requests.get(robots_url, verify=False)
    if response.status_code == 200:
        disallowed_paths = [line.split(": ", 1)[1] for line in response.text.split("\n") if line.startswith("Disallow")]
        admin_paths = [path for path in disallowed_paths if "admin" in path or "panel" in path]
        return admin_paths
    else:
        print("(-) Error retrieving robots.txt.")
        return []

def detect_admin_panel(url):
    admin_paths = get_admin_paths(url)
    if admin_paths:
        print("(+) Found admin paths in robots.txt:", admin_paths)
        for path in admin_paths:
            admin_panel_url = urljoin(url, path)
            print(f"(+) Testing admin panel: {admin_panel_url}")
            r = requests.get(admin_panel_url, verify=False)
            if r.status_code == 200:
                print('(+) Found the administrator panel!')
                break
        else:
            print("(-) No admin panel found.")
    else:
        print("(-) No admin paths found in robots.txt.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect admin panels by analyzing robots.txt.")
    parser.add_argument("url", help="The URL of the web page to analyze")

    args = parser.parse_args()
    url = args.url

    print("(+) Finding admin panel...")
    detect_admin_panel(url)
