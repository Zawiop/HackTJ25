import requests
from bs4 import BeautifulSoup
from playsound import playsound

API_KEY = "93722cd5a89646998698ba31feb17bb1"

# Get text from a webpage
URL = "https://example.com"
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

# Extract visible text from webpage (modify as needed)
text = soup.get_text()
text = text.strip().replace("\n", " ")  # Remove excessive whitespace

# Generate speech using VoiceRSS
tts_url = f"http://api.voicerss.org/?key={API_KEY}&hl=en-us&src={text}"
audio_response = requests.get(tts_url)

# Save and play the audio
with open("output.mp3", "wb") as file:
    file.write(audio_response.content)

playsound("output.mp3")