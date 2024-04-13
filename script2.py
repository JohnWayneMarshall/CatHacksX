import os
from dotenv import load_dotenv
import openai
from pydub import AudioSegment
from pydub.playback import play
import io

load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')

client = openai.OpenAI(api_key=API_KEY)

text_to_speak = ""

response = client.audio.speech.create(
    model="tts-1",
    voice="onyx",
    input=text_to_speak
)

print(response)
print(dir(response))

audio_data = response.content

audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")

play(audio_segment)