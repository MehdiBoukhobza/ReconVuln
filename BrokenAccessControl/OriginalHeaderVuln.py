import requests
import argparse

def check_x_original_url(url):
    try:
        modified_path = "/nonexistent-page"
        headers = {'X-Original-URL': modified_path}
        response = requests.get(url, headers=headers)

        if response.status_code == 404:
            print(f"Testing '{url}' with X-Original-URL header set to '{modified_path}' resulted in 404 Not Found. This indicates a potential vulnerability.")
        elif response.status_code == 200:
            print(f"Testing '{url}' with X-Original-URL header set to '{modified_path}' resulted in 200 OK. The page exists, and it might be accessible.")
        else:
            print(f"Testing '{url}' with X-Original-URL header set to '{modified_path}' resulted in an unexpected response status code: {response.status_code}.")
    except Exception as e:
        print(f"An error occurred while testing the URL: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check X-Original-URL vulnerability.")
    parser.add_argument("url", help="The URL to test")

    args = parser.parse_args()

    check_x_original_url(args.url)
