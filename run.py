import os
import pyaudio
import wave
import requests
import time
from openai import OpenAI
from elevenlabs import Voice, VoiceSettings,stream
from elevenlabs.client import ElevenLabs
open_api_key="" #Use your ChatGPT API Key here
os.environ["OPENAI_API_KEY"]=open_api_key
client2 = OpenAI()

client = ElevenLabs(
  api_key="26eb00f9e99a7f45ed9fdbdb96b4a8a7", # Defaults to ELEVEN_API_KEY
)

API_URL = "" #AWS Server Endpoint URL, Currently Unavailable

headers = {
    "Accept" : "application/json",
    "Authorization": "Bearer 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",
    "Content-Type": "application/json"
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def stream_text_in_words(text):
    words = text.split()
    for word in words:
        print(word, end=" ", flush=True)
        time.sleep(0.05)
    print("\n")

def truncate_at_token(string, tokens):
    min_index = len(string)
    for token in tokens:
        index = string.rfind(token)  # Start searching from the end of the string
        if index != -1:
            min_index = min(min_index, index)
    new_string = string[:min_index]

    # Find the last occurrence of ".", "?", or "!" and truncate the string there
    last_punctuation_index = max(new_string.rfind("."), new_string.rfind("?"), new_string.rfind("!"))
    if last_punctuation_index != -1:
        new_string = new_string[:last_punctuation_index + 1]  # Include the punctuation mark

    return new_string

def record_audio(filename, duration=8):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    print("Recording started. Speak now...")

    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording stopped.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def recognize_speech():
    record_audio("temp_audio.wav")

    if os.path.exists("temp_audio.wav"):
        with open("temp_audio.wav", "rb") as f:
            transcript = client2.audio.transcriptions.create(
            model="whisper-1", 
            file=f, 
            response_format="text")

        os.remove("temp_audio.wav")

        if transcript:
            print("You said:", transcript)
            return transcript
        else:
            print("Sorry, I couldn't understand what you said.")
            return ""
    else:
        print("Error: Audio file not found.")
        return ""
    
def chat_with_model(user_input, conv):
      conv += "User: " + user_input + "\n" + "Assistant: "
      start_time = time.time()
      output_stream = query({
        "inputs": conv,
        "parameters": {
        "top_k": 50,
        "top_p": 0.95,
        "temperature": 1,
        "max_new_tokens": 64,
      "return_full_text" : False,
        "do_sample": True
  }
    }
)
      response = output_stream[0]["generated_text"]
      response = truncate_at_token(response,["[//]","[/]",'User'," [/]","[/] "," [/] "])
      stream_text_in_words(response)
      end_time = time.time()
      
      audio = client.generate(
      text=response,
      voice=Voice(
      voice_id='XrExE9yKIg1WjnnlVkGX',
      settings=VoiceSettings(stability=0.35, similarity_boost=0.5, style=0.0, use_speaker_boost=False)
    ),
    
    stream = True,
    optimize_streaming_latency = 4,
    model="eleven_monolingual_v1"
)
      stream(audio)

      generation_time = end_time - start_time
      print("Generation Time:", generation_time)  # Print generation time
      conv += response + "\n"
      return response

if __name__ == "__main__":
    conv = "You are a helpful and joyous mental therapy assistant. Always answer as helpfully and cheerfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information. Also, don't mention your name or you being an AI or assistant or an app, anywhere ever. Also generate one response only. Keep the response brief and concise. Talk in a human manner. \n"
    user_input = recognize_speech()
    conv = chat_with_model(user_input, conv)
    time.sleep(2)
