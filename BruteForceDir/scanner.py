import argparse
from directory_bruteforcer import brute_force_directories
from wordlist_loader import load_default_wordlist, load_noisy_wordlist

def main():
    parser = argparse.ArgumentParser(description="Directory brute-forcer tool.")
    parser.add_argument("base_url", help="The base URL to scan")
    parser.add_argument("--noise", action="store_true", help="Use noisy wordlist")
    parser.add_argument("--wordlist_file", help="Path to a custom wordlist file")
    parser.add_argument("--test-subdirectories", action="store_true", help="Test subdirectories")
    parser.add_argument("--screenshots", action="store_true", help="Take screenshots")

    args = parser.parse_args()

    base_url = args.base_url
    use_noisy_wordlist = args.noise
    test_subdirectories = args.test_subdirectories
    take_screenshots = args.screenshots

    if use_noisy_wordlist:
        wordlist = load_noisy_wordlist()
    elif args.wordlist_file:
        with open(args.wordlist_file, 'r') as f:
            wordlist = f.read().splitlines()
    else:
        wordlist = load_default_wordlist()

    brute_force_directories(base_url, wordlist, test_subdirectories, take_screenshots)

if __name__ == "__main__":
    main()
