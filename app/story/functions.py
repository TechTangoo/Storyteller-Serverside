import pyttsx3

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Get list of available voices
voices = engine.getProperty('voices')

# Print information about each voice
for idx, voice in enumerate(voices):
    print(f"Voice {idx}:")
    print(f" - Name: {voice.name}")
    print(f" - ID: {voice.id}")
    print(f" - Languages: {voice.languages}")
    print(f" - Gender: {voice.gender}")
    print(f" - Age: {voice.age}")
    print(f" - Rate: {voice.age}")
    print(f" - Volume: {voice.volume}")
    print(" ")
