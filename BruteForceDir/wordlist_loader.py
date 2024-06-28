DEFAULT_WORDLIST = "BruteForceDir/default_wordlist.txt"
NOISY_WORDLIST = "BruteForceDir/noisy_wordlist.txt"

def load_default_wordlist():
    with open(DEFAULT_WORDLIST, 'r') as f:
        return f.read().splitlines()

def load_noisy_wordlist():
    with open(NOISY_WORDLIST, 'r') as f:
        return f.read().splitlines()
