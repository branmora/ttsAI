# %%
import time
import random
from datetime import datetime
import sounddevice as sd
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings, play, save
from utils import load_config
from pathlib import Path
from scipy.io.wavfile import write

config = load_config()

client_eleven_labs = ElevenLabs(api_key = config['eleven_labs_api_key'])
client_openai = OpenAI(api_key = config['openai_api_key'])

output_path = Path(config['output_path'])

# %% Record audio
 
# Sampling frequency
freq = 44100
 
# Recording duration
duration = 20

# Main loop
while True:
    
    # Random sleep interval between 10 and 15 minutes
    # sleep_time = random.randint(600, 900)
    # print(f"Sleeping for {sleep_time} seconds")
    # time.sleep(sleep_time)
    
    # Create a timestamp for the recording
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Start recorder with the given values of duration and sample frequency
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

    with open(f"user_recording_{timestamp}.txt", "w") as file:
        file.write(transcription)

    # Generate response from OpenAI
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
          "content": f"Make an hilarious comment to streamer based on what he's saying: {transcription}"
        }
      ]
    )

    response_text = response.choices[0].message.content
    print(f"TTS Response: {response_text}")

    with open(output_path / f"llm_response_{timestamp}.txt", "w") as file:
        file.write(response_text)

    # Convert text response to speech
    response_audio = client_eleven_labs.generate(
        text=response_text,
        voice=Voice(
            model=config['eleven_labs_model'],
            voice_id=config['eleven_labs_voice_id'],
            settings=VoiceSettings(stability=0.31, similarity_boost=0.9, use_speaker_boost=True)
        )
    )

    play(response_audio)
    save(response_audio, output_path / f"llm_response_{timestamp}.wav")

    # %% get all voices
    client_eleven_labs.voices.get_all().voices
    # %%
