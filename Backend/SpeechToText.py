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
HtmlCode = str(HtmlCode).replace("recognition.lang + ' ';", f"recognition.lang")
