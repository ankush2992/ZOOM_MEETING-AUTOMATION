# Zoom Meeting Automation Script

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Selenium](https://img.shields.io/badge/Selenium-Automation-brightgreen) ![WebDriver](https://img.shields.io/badge/WebDriver-Microsoft%20Edge-yellowgreen)

This script automates joining Zoom meetings using Selenium and the Microsoft Edge WebDriver. It's a helpful tool for automating repetitive Zoom meeting workflows, like entering your name and joining the meeting.

## Features

- Automates launching Zoom meetings from a browser.
- Automatically enters your name into the meeting.
- Keeps the session alive for a specified duration.
- Option to run in headless mode for background automation.

---

## Prerequisites

1. **Python**: Version 3.8 or higher.
2. **Selenium**: Install using `pip install selenium`.
3. **WebDriver Manager**: Install using `pip install webdriver-manager`.
4. **Microsoft Edge**: Ensure Edge browser is installed on your system.
5. **Edge WebDriver**: Automatically managed by the script via `webdriver-manager`.

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/zoom-meeting-automation.git
    cd zoom-meeting-automation
    ```

2. Install the required Python packages:
    ```bash
    pip install selenium webdriver-manager
    ```

---

## Usage

1. Run the script:
    ```bash
    python zoom_meeting_automation.py
    ```

2. Follow the prompts:
   - Enter the Zoom meeting link.
   - Specify the meeting duration (in minutes).
   - The script will open the Zoom link in the browser, enter your name, and join the meeting.

3. Example session:
   ```
   Enter the Zoom meeting link (or type 'exit' to quit): https://zoom.us/j/123456789
   Enter the meeting duration in minutes: 30
   Joining Zoom meeting for 30 minutes: https://zoom.us/j/123456789
   ```

---





## Disclaimer
This project is provided for educational and personal use only. The developer is not responsible for any misuse, compliance violations, or potential issues arising from the use of this tool. Please use responsibly and ensure adherence to Zoom's terms of service and privacy policies.
