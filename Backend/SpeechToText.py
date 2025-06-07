from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt

# Load environment variables from the ,env file.
env_vars = dotenv_values('.env')

# Get the imput laguage setting from the environtment varriables.
InputLanguage = env_vars.get("InputLanguage")

# Define the HTML code for the speech recognition interface.
HtmlCode = """"""

# Replace the language setting in the HTML code with the value from the environment variables.
HtmlCode = str(HtmlCode).replace("recognition.lang = ' ';", f"recognition.lang = '{InputLanguage}';")

# Write the modified HTML code to a file.
with open(r"Data\Voice.html", "w") as f:
    f.write(HtmlCode)

# Get the current working directory.
current_dir = os.getcwd()

# Generate the file path for the HTML file.
Link = f"{current_dir}/Data/Voice.html"

#Set CHrome options for the WebDriver.
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.3"
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")

#Inialize the Chrome WebDriver using the chrome .
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define the path for temporary files.
TempDirPath = rf'{current_dir}/Frontens/Files'
