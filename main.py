import subprocess
import argparse


def display_banner():
    banner = """

    ██████╗  ███████╗  ██████╗    ███████╗ ███╗   ███╗  ██╗  ██╗     
    ██╔══██╗ ██╔════╝ ██╔════╝    ██╔════╝ ████╗ ████║  ██║  ██║     
    ██████╔╝ █████╗   ██║         █████╗   ██╔████╔██║  ██║  ██║     
    ██╔══██╗ ██╔══╝   ██║   ██║   ██╔══╝   ██║╚██╔╝██║  ██║  ██║     
    ██║  ██║ ███████╗ ╚██████╔╝   ███████╗ ██║ ╚═╝ ██║  ██║  ███████╗
    ╚═╝  ╚═╝ ╚══════╝  ╚═════╝    ╚══════╝ ╚═╝     ╚═╝  ╚═╝  ╚══════╝

    """
    print(banner)


def run_broken_access_control(url):
    print("\nChoose the Broken Access Control test to run:")
    print("1. Original Header Vulnerability")
    print("2. Scrape Web")
    print("3. Test Robots for Admin")
    print("4. Run All Tests")

    choice = input("\nEnter the number of the Broken Access Control test you want to run: ").strip()

    if choice == "1":
        subprocess.run(["python", "BrokenAccessControl/OriginalHeaderVuln.py", url])
    elif choice == "2":
        subprocess.run(["python", "BrokenAccessControl/ScrapeWeb.py", url])
    elif choice == "3":
        subprocess.run(["python", "BrokenAccessControl/TestRobotsForAdmin.py", url])
    elif choice == "4":
        subprocess.run(["python", "BrokenAccessControl/OriginalHeaderVuln.py", url])
        subprocess.run(["python", "BrokenAccessControl/ScrapeWeb.py", url])
        subprocess.run(["python", "BrokenAccessControl/TestRobotsForAdmin.py", url])
    else:
        print("\nInvalid choice. Please run the script again and select a valid test.")


def run_brute_force_dir(url):
    print("\nChoose additional options for Brute Force Directory test:")
    noise = input("Use noisy wordlist? (yes/no): ").strip().lower() == "yes"
    wordlist_file = input("Enter the path to a custom wordlist file (leave empty for default): ").strip()
    test_subdirectories = input("Test subdirectories? (yes/no): ").strip().lower() == "yes"
    take_screenshots = input("Take screenshots? (yes/no): ").strip().lower() == "yes"

    command = ["python", "BruteForceDir/scanner.py", url]
    if noise:
        command.append("--noise")
    if wordlist_file:
        command.extend(["--wordlist_file", wordlist_file])
    if test_subdirectories:
        command.append("--test-subdirectories")
    if take_screenshots:
        command.append("--screenshots")

    subprocess.run(command)


def run_multiple_injections(url):
    subprocess.run(["python", "MultipleInjections.py", url])


def main():
    display_banner()

    parser = argparse.ArgumentParser(description="Choose the vulnerability test to run")
    parser.add_argument("url", nargs='?', help="The URL to test for vulnerabilities")

    args = parser.parse_args()

    # Prompt for URL if not provided
    url = args.url or input("Enter the URL to test for vulnerabilities: ").strip()

    print("\nChoose the vulnerability test to run:")
    print("1. Broken Access Control")
    print("2. Brute Force Directory")
    print("3. Multiple Injections")

    choice = input("\nEnter the number of the test you want to run: ").strip()

    if choice == "1":
        run_broken_access_control(url)
    elif choice == "2":
        run_brute_force_dir(url)
    elif choice == "3":
        run_multiple_injections(url)
    else:
        print("\nInvalid choice. Please run the script again and select a valid test.")


if __name__ == "__main__":
    main()
