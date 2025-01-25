# used Edge Browser for automation . 
import re
import random
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def is_link(message):
    link_pattern = r'https?://\S+'
    return re.search(link_pattern, message) is not None

def extract_link(message_text):
    link_pattern = r'https?://\S+'
    match = re.search(link_pattern, message_text)
    if match:
        return match.group(0)
    else:
        return None

def open_link_with_selenium(link, meeting_duration, user_name, headless=False):#+
    edge_options = webdriver.EdgeOptions()
    if headless:
        print("Running in headless mode")
        edge_options.add_argument('--headless')  # Enable headless mode
        edge_options.add_argument('window-size=1920x1080')  # Configure your desired window size
    else:
        print("Running in visible mode")

    edge_options.add_argument('--disable-gpu')  # Disable GPU for compatibility
    edge_options.add_argument('--disable-blink-features=AutomationControlled')  # Avoid detection (your automation script wont be visible)
    edge_options.add_argument('--no-sandbox')  # Useful for VPS environments (if you used to host code in there)

    # Custom user-agent string (denotes you as a user)
    edge_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.902.67 Safari/537.36 Edg/92.0.902.67")

    # Initialize Edge WebDriver with options
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=edge_options)

    
    # ---> Processes the web automation on browser . everything is automatic (may get error if website changes its interface)
    try:
        driver.get(link)
        print(f"Opened link in Edge: {link}")

        print("Waiting for 'Launch Meeting' button...")               # initial link opening (landing page)
        launch_meeting_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mbTuDeF1"))    # (locater for the button)
        )
        driver.execute_script("arguments[0].click();", launch_meeting_button)       # stimulate a mouse click , similar to your manual Left Click
        print("Clicked the 'Launch Meeting' button")                                     # confirmation for the link opening (on terminal)

        print("Waiting for 'Join from your browser' button...")         #  --->>  same setup as above (for next buttons)  <<-----
        join_from_browser_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id=\"zoom-ui-frame\"]/div[2]/div/div[2]/h3[2]/span/a'))             # used xpath as a locator element (get these vis inspect elements on the zoom website)
        )
        driver.execute_script("arguments[0].click();", join_from_browser_button)
        print("Clicked the 'Join from your browser' button")

        time.sleep(5)

        print("Entering name in the name input field...")
        iframe = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(iframe)

        name_input_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="input-for-name"]'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", name_input_field)
        name_input_field.click()
        name_input_field.clear()

        name_input_field.send_keys(user_name)                               # entering your name (name to apppear on the meeting)
        print(f"Name entered successfully: {user_name}")
        driver.switch_to.default_content()
        ActionChains(driver).send_keys(Keys.ENTER).perform()
        print("Pressed the Enter key to join the meeting")

        # Convert meeting duration from minutes to seconds
        duration = meeting_duration * 60
        elapsed = 0
        interval = 60  # check every 60 seconds and notify it
        print(f"Keeping the session alive for {meeting_duration} minutes...")
        while elapsed < duration:
            time.sleep(interval)
            elapsed += interval
            print(f"Elapsed time: {elapsed // 60} minutes")

        print(f"{meeting_duration} minutes completed. Closing the browser...")        # your time compleates and the meeting will end from your side . (not from the host side)

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot("error_screenshot.png")  # Save a screenshot for debugging (necessaey for Headless mode as you cant see a visible browser)  [no need for visible browser (there you can track the error)]

    finally:
        driver.quit()




if __name__ == '__main__':
    while True:
        try:
            user_input = input("Enter the Zoom meeting link (or type 'exit' to quit): ")
            if user_input.lower() == 'exit':
                print("Terminating the script. bye bye!")
                break

            if is_link(user_input):
                zoom_link = extract_link(user_input)
                if zoom_link:
                    while True:
                        try:
                            meeting_duration = int(input("Enter the meeting duration in minutes: "))
                            if meeting_duration > 0:
                                break
                            else:
                                print("Duration must be a positive integer. Please try again.")
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")

                    print(f"Joining your meeting for {meeting_duration} minutes: {zoom_link}")
                    open_link_with_selenium(zoom_link, meeting_duration)
                else:
                    print("Invalid link format. Please try again. if link is correct change the link extraction code in the code")
            else:
                print("No valid link detected. Please enter a valid Zoom meeting link.")

        except KeyboardInterrupt:
            print("\ni see , you ,must have pressed CTRL+C  . Exiting the code now as you command...")
            break
        except Exception as e:
            print(f"some error happened: {e}")
