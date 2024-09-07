# BrokenAccessControl

## Overview
ReconVuln is a robust security testing tool designed for web applications. It aims to assist developers and security professionals by identifying and addressing a variety of security vulnerabilities, including broken access control, brute force attacks, and multiple injection types.

## Features
### Security Tests
- **Broken Access Control Tests**:
  - Original Header Vulnerability
  - Scrape Web Content
  - Test Robots.txt for Admin Paths
- **Brute Force Directory Attack**:
  - Utilizes customizable wordlists
  - Supports optional noise generation and subdirectory testing
  - Captures screenshots of identified endpoints
- **Injection Vulnerabilities**:
  - SQL Injection, Cross-Site Scripting (XSS), and Command Injection
  - Directory Traversal, Remote and Local File Inclusion (RFI/LFI)
  - Cross-Site Request Forgery (CSRF)

### Detailed Scanning
- Detects insecure server configurations and open redirects among others, providing comprehensive vulnerability assessments.

## Getting Started
### Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/BrokenAccessControl.git
   cd BrokenAccessControl

2. **Set Up Remote Repository**:
   ```bash
   git remote add origin https://github.com/yourusername/BrokenAccessControl.git
   ```

## Usage

- **Run the Main Script**:
  ```bash
  python main.py
  ```

- **Run Specific Tests**:
  - **Broken Access Control**:
    ```bash
    python BrokenAccessControl/OriginalHeaderVuln.py <url>
    ```
  - **Brute Force Directory**:
    ```bash
    python BruteForceDir/scanner.py <url> [--noise] [--wordlist_file <path>] [--test-subdirectories] [--screenshots]
    ```
  - **Multiple Injections**:
    ```bash
    python MultipleInjections.py <url>
    ```

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`.
3. Make your changes.
4. Commit your changes: `git commit -am 'Add some feature'`.
5. Push to the branch: `git push origin feature-branch`.
6. Submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- This tool was developed by Boukhbza El Mehdi, ElMardi Moad, Hourairi Lilya under the guidance of Orange Cyberdefense and Mister Boukhari.
- Special thanks to all contributors and open-source projects that make this project possible.


