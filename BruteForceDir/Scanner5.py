import requests
import sys

DEFAULT_WORDLIST = "default_wordlist.txt"
NOISY_WORDLIST = "noisy_wordlist.txt"
YELLOW = '\033[33m'
RED = '\033[31m'
RESET='\033[0m'
BLUE='\033[34m'


def brute_force_directories(base_url, wordlist, test_subdirectories=False):
    print("")

    found_directories=[]
    for directory_name in wordlist:
        url = f"{base_url}/{directory_name}"
        response = requests.get(url, allow_redirects=False)  # Disable redirects

        

        # Check for redirection
        if response.status_code == 301 or response.status_code == 302:
            print(f" --> {url} \033[34m redirects to \033[0m {response.headers['Location']}")
            continue

        # Check for authentication required
        if response.status_code == 401:
            print(f" --> Directory at {url} requires authentication.")
            # You can also inspect the WWW-Authenticate header for more details
            authenticate_header = response.headers.get('WWW-Authenticate')
            if authenticate_header:
                print(f" --> Authentication methods supported: {authenticate_header}")
            continue

        # Check for other status codes
        
        if response.status_code == 403:
            print(f"\033[31m --> {url} \033[0mis \033[31m forbidden\033[0m.")
        if response.status_code == 200:
            print(f" --> {url}")
            found_directories.append(url)
        """
        else:
            print(f"Unexpected status code {response.status_code} for directory: {url}")
        """
    if test_subdirectories:
        print("\n")
        for directory in found_directories:
            print("")
            print(f" Testing subdirectories of {directory}:")
            brute_force_directories(directory,wordlist)

def load_default_wordlist():
    with open(DEFAULT_WORDLIST, 'r') as f:
        return f.read().splitlines()

def load_noisy_wordlist():
    with open(NOISY_WORDLIST, 'r') as f:
        return f.read().splitlines()
        
if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 5:
        print("Usage: python Scanner.py <base_url> [--noise] [<wordlist_file>] [--test-subdirectories]")
        sys.exit(1)
    
    base_url = sys.argv[1]
    use_noisy_wordlist = "--noise" in sys.argv
    test_subdirectories = "--test-subdirectories" in sys.argv

    custom_wordlist_index = sys.argv.index("<wordlist_file>") if "<wordlist_file>" in sys.argv else -1
    if use_noisy_wordlist:
        wordlist = load_noisy_wordlist()
    elif custom_wordlist_index != -1 and len(sys.argv) > custom_wordlist_index + 1:
        wordlist_file = sys.argv[custom_wordlist_index + 1]
        with open(wordlist_file, 'r') as f:
            wordlist = f.read().splitlines()
    else:
        wordlist = load_default_wordlist()


    brute_force_directories(base_url, wordlist, test_subdirectories)