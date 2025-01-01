# %%
import time
import random
from datetime import datetime
import sounddevice as sd
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from utils import load_config
from pathlib import Path
from scipy.io.wavfile import write
import requests

config = load_config()

client_openai = OpenAI(api_key=config['openai_api_key'])

# Twitch API Details
CLIENT_ID = "sy1kxf9t94bmdwo8n4eha8kjfa04pg"
BROADCASTER_ID = "708264432"  # SpaceBar


# Fanfetin
# ACCESS_TOKEN = "3h992et9zwzjq8gqv413zoibqyly7h"
# SENDER_ID = "1224177800"

# Greentortoise
ACCESS_TOKEN = "xwlfli2on0d6cnap46plg9vwsn5udz"
SENDER_ID = "1224192737"

output_path = Path(config['output_path'])

# Function to send chat message
def send_chat_message(broadcaster_id, sender_id, message, access_token, client_id, reply_parent_message_id=None):
    """
    Sends a chat message to a Twitch channel.
    """
    url = 'https://api.twitch.tv/helix/chat/messages'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Client-Id': client_id,
        'Content-Type': 'application/json'
    }
    data = {
        "broadcaster_id": broadcaster_id,
        "sender_id": sender_id,
        "message": message
    }
    if reply_parent_message_id:
        data["reply_parent_message_id"] = reply_parent_message_id

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Main loop
while True:
    # Random sleep interval between 10 and 15 minutes
    sleep_time = random.randint(240, 420)
    print(f"Sleeping for {sleep_time} seconds")
    time.sleep(sleep_time)

    # Recording audio
    freq = 44100
    duration = 30
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    print("Recording...")
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)
    sd.wait()
    print("Recording finished")
    write(output_path / f"user_recording_{timestamp}.wav", freq, recording)

    # Transcribe the recording
    audio_file = open(output_path / f"user_recording_{timestamp}.wav", "rb")

    transcription = client_openai.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text",
        language="es"
    )
    print(f"Transcription: {transcription}")

    with open(output_path / f"user_recording_{timestamp}.txt", "w") as file:
        file.write(transcription)

    # Generate response from OpenAI
    response = client_openai.chat.completions.create(
        model=config['openai_model'],
        messages=[
            {
                "role": "system",
                "content": 
                """
                You're an entertaining gen-z or alpha chatter, you use gen-z slang from Latin American communities,
                you do not use any emotes or emojis,
                you do not use hashtags,
                the year is 2024,
                you speak in a natural language,
                you write in a really casual, conversational tone,
                you always write in lowercase,
                you can have wrong spelling,
                you dont use accents (tildes),
                you never use commas,
                you sometimes only use one emote as a response, including: DinoDance, PopNemo, GlitchCat, PopCorn, StinkyCheese
                CoolCat, DxCat, SplashTail, GoldPLZ, FallWinning, FallHalp, BegWan
                you are prohibited to use other emotes or emojis besides those,
                BloodTrail, you can also use emotes in your messages, only two in 10 messages can have an emote, 
                you do not use proper grammar or punctuation, and you're
                always ready with a quip or comment to keep the Twitch chat lively or slightly mock the streamer, you are slightly annoying.
                Today, you're watching a unique Elden Ring stream where both streamers are trying to get to speedrun through ,
                and the streamer space and streamer mulberry are trying to finish the game, no matter what chaos unfolds (you can mention their names).
                Your job is to make the chat laugh, cheer, and stay engaged with witty remarks, memes,
                and encouraging words tailored to the wild unpredictability of this stream.
                The message has to be short (between 1 and 7 words), if you use only one word, then you use an emote. You speak purely in Spanish.
                """
            },
            {
                "role": "user",
                "content": f"Make an hilarious comment to streamer based on what he's saying: {transcription}"
            }
        ]
    )

    response_text = response.choices[0].message.content.strip()
    print(f"Generated Chat Message: {response_text}")

    with open(output_path / f"llm_response_{timestamp}.txt", "w") as file:
        file.write(response_text)

    # Send chat message to Twitch
    chat_response = send_chat_message(
        broadcaster_id=BROADCASTER_ID,
        sender_id=SENDER_ID,
        message=response_text,
        access_token=ACCESS_TOKEN,
        client_id=CLIENT_ID
    )
    print(f"Chat Response: {chat_response}")
# %%
