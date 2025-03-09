import assemblyai as aai
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

# Replace with your API key
aai.settings.api_key = "971e871c17ba4246b3786122fb1f0760"

# Recording parameters
samplerate = 44100  # 44.1 kHz (CD Quality)
duration = 20  # Duration in seconds

print("Recording...")
audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=2, dtype='int16')
sd.wait()  # Wait until recording is finished
print("Recording finished!")

# Save as WAV file
wav.write("output.wav", samplerate, audio_data)
print("File saved as output.wav")

# URL of the file to transcribe
FILE_URL = "output.wav"

# You can change the model by setting the speech_model in the transcription config
config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.nano)

transcriber = aai.Transcriber(config=config)
transcript = transcriber.transcribe(FILE_URL)

if transcript.status == aai.TranscriptStatus.error:
    print(transcript.error)
else:
    print(transcript.text)

















#-----------------------------------------------------------------------------------------------------------------
# You can also transcribe a local file by passing in a file path
# FILE_URL = './path/to/file.mp3'

# transcriber = aai.Transcriber()
# transcript = transcriber.transcribe(FILE_URL)

# if transcript.status == aai.TranscriptStatus.error:
#     print(transcript.error)
# else:
#     print(transcript.text)
#-----------------------------------------------------------------------------------------------------------------
    # config = aai.TranscriptionConfig(speaker_labels=True)

    # transcriber = aai.Transcriber()
    # transcript = transcriber.transcribe(
    #   FILE_URL,
    #   config=config
    # )

    # for utterance in transcript.utterances:
    #   print(f"Speaker {utterance.speaker}: {utterance.text}")
#-----------------------------------------------------------------------------------------------------------------
