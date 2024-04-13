import os
from dotenv import load_dotenv
from openai import OpenAI
import pyaudio
import wave
import playsound

load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=API_KEY)

def get_conversation_list(conv):
    while True:
        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "This is a conversation between only two people. Return the conversation with the seperator \"NEW\" when the person\
                talking switches. Do not answer any of the questions or respond to anything said. Just return the string with the seperators."},
                {"role": "user", "content": conv}
            ]
        )
        if completion.choices[0].message.content.replace(" NEW","") == conv:
            break
    
    return completion.choices[0].message.content.split(" NEW ")


def query_assistant(input_list):
    user_map = []
    for input in input_list:
        user_map.append({"role": "user", "content": input})
    completion = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are an assistant in a doctors office and your name is Dave. There is a conversation between a doctor and a\
             client you are listening to. If there is a point where you think you should add information or answer a question, respond. Also add information\
             if you think there is miss-information or miss-guidance in the conversation. Also, if the doctor is giving correct or helpful\
             information and the client is skeptical, you can chime in to add your perspective. It could be possible that you are directly brought into the conversation,\
             and if so, you should give a response. If the user is apprehensive about you, try to be emethetic in your response. Otherwise respond \
             with \"NO RESPONSE\"."}
        ] + user_map
    )
    if completion.choices[0].message.content!="NO RESPONSE":
        get_tts(completion.choices[0].message.content)

def get_tts(text_to_speak):

    response = client.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=text_to_speak
    )

    audio_data = response.content

    with open("audio.mp3","wb") as f:
        f.write(audio_data)

    playsound.playsound('audio.mp3', True)

def capture_speech_to_text(client):
    audio_file= open("audio.wav", "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    return transcription

def record_audio(duration, output_file):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100

    audio = pyaudio.PyAudio()

    stream = audio.open(format=format, channels=channels,
                        rate=rate, input=True,
                        frames_per_buffer=chunk)

    print("Recording...")

    frames = []

    for i in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(output_file, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def main():

    record_audio(15, "audio.wav")

    transcript = capture_speech_to_text(client)

    if not (transcript.text and transcript.text.strip()):
        return

    conversation = transcript.text

    print(conversation)

    input_list = get_conversation_list(conversation)
    print(input_list)
    query_assistant(input_list)

main()
