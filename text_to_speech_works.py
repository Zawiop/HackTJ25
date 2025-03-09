import requests
from pydub import AudioSegment
from pydub.playback import play
from google import genai
import os

# Ensure ffmpeg is installed (adjust path if needed)
AudioSegment.converter = "/opt/homebrew/bin/ffmpeg"

# Set up Gemini AI
client = genai.Client(api_key="AIzaSyDzGSAgR6R7T6T0PJeMy6xCuPCVFdHtXHA")
chat = client.chats.create(model="gemini-2.0-flash")


# Function to send messages to Gemini
def send_message(message):
    ai_response = chat.send_message(message)
    return ai_response.text.strip()  # Strip spaces & newlines


# Function to convert text to speech and play it
def text_to_speech(text):
    API_KEY = "93722cd5a89646998698ba31feb17bb1"

    # Limit text length to avoid URL length issues
    if len(text) > 1000:
        text = text[:1000] + "..."

    # Create the URL for the VoiceRSS API (using the same format as your working example)
    tts_url = f"http://api.voicerss.org/?key={API_KEY}&hl=en-us&v=1&r=0&c=MP3&src={text}"

    # Fetch the TTS response
    response = requests.get(tts_url)

    # Save the audio file
    with open("output.mp3", "wb") as file:
        file.write(response.content)

    # Check if the file was created
    if os.path.exists("output.mp3") and os.path.getsize("output.mp3") > 0:
        print("Playing audio response...")
        audio = AudioSegment.from_mp3("output.mp3")
        play(audio)
        return True
    else:
        print("Error: Audio file was not created or is empty.")
        return False


# Start conversation
orig_prompt = ("You will be asking multiple choice questions to determine the best career for a high school or college "
               "student based on personality, course load, interests, etc. Ask questions one at a time until you can "
               "provide 3-4 career choices that fit perfectly with the information given from the answers.")

# Get the first response
response = send_message(orig_prompt)
print("AI:", response)

# Convert first response to speech
text_to_speech(response)

# Main conversation loop
conversation_active = True
while conversation_active:
    user_input = input("You (type 'exit' to quit): ")

    # Exit condition
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("Ending conversation.")
        conversation_active = False
        break

    # Get AI response
    response = send_message(user_input)
    print("AI:", response)

    # Convert response to speech and play it
    text_to_speech(response)

print("Career advisor session completed.")
