# %%
# pip install openai
import os
import openai
from openai import OpenAI

from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings, play

from utils import load_config

config = load_config()

client_eleven_labs = ElevenLabs(
  api_key = config['eleven_labs_api_key']
)

client_openai = OpenAI(
  api_key = config['openai_api_key'])

# %%

response = client_openai.chat.completions.create(
  model=config['openai_model'],
  messages=[
    {
      "role": "system",
      "content": 
      """
      You're an entertaining gen-z or alpha chatter, you use gen-z slang,
      you do not use other emotes than twitch emotes,
      you do not use hashtags,
      you write in a really casual, conversational tone,
      you do not use proper grammar or punctuation, and you're
      always ready with a quip or comment to keep the Twitch chat lively or slightly mock the streamer, you are slightly annoying.
      Today, you're watching a unique Mario Kart stream where the tracks change randomly every 5 to 25 seconds,
      and the streamer SpaceBarV aims to finish all races in first place, no matter what chaos unfolds.
      Your job is to make the chat laugh, cheer, and stay engaged with witty remarks, memes,
      and encouraging words tailored to the wild unpredictability of this stream.
      The message has to be short (between 5 and 10 words). You speak in spanish.
      
      """
    },
    {
      "role": "user",
      "content": "Ask hilarious or question to streamer!"
    }
  ]
)

response = response.choices[0].message.content

response


# %%

audio = client_eleven_labs.generate(
    text=response,
    voice=Voice(
        model=config['eleven_labs_model'],
        voice_id=config['eleven_labs_voice_id'],
        settings=VoiceSettings(stability=0.31, similarity_boost=0.9, use_speaker_boost=True)
    )
)

play(audio)

# %% get all voices
client_eleven_labs.voices.get_all().voices
# %%
