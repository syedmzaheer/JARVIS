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
HtmlCode = HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

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
chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
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

# Function to set the assistant status by writing to a file.
def SetAssistantStatus(status):
    with open(rf"{TempDirPath}/Status.data", "w", encoding='utf-8') as file:
        file.write(status)

# Function to modify a query to ensure a proper punctuation and formating.
def QuerryModfier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = {"how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's", "can you"}
    
    # Check if the query is a aquestion and add a question mark if necessary.
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in [',', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        new_query += ". "

    return new_query.capitalize()

# Funtion to translate text into English using mtranslate library.
def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

# Function to perform speech recognition using the WebDriver.
def SpeechRecognition():
    # Navigate to the Voice HTML file.
    driver.get("file:///" + Link)
    # Start speech recognition by clicking the start button.
    driver.find_element(by=By.ID, value="start").click()
    
    while True:
        try:
            # Get the recognized text from the HTML output element.
            Text = driver.find_element(by=By.ID, value="output").text

            if Text:
                # Stop the recognition by clicking the stop button.
                driver.find_element(by=By.ID, value="end").click()
                
                #  If the input language is English, retun the modified query.
                if InputLanguage.lower() == "en" or"en" in InputLanguage.lower():
                    return QuerryModfier(Text)
                else:
                    # If the input language is not English, translate the text into English and return the modified query.
                    SetAssistantStatus("Translating ...")                    
                    return QuerryModfier(UniversalTranslator(Text))
        
        except Exception as e:
            pass

# Main execution block.
if __name__ == "__main__":
    while True:
        # Continously perform speech recognition and print the recognized text.
        Text = SpeechRecognition()
        print(Text)
