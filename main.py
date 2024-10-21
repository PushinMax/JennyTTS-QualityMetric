import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf
import speech_recognition as sr
from jiwer import wer
import numpy as np
import librosa
import string


def speech_generation(prompt: str, description: str, file_path: str):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model_name = "parler-tts/parler-tts-mini-jenny-30H"

    model = ParlerTTSForConditionalGeneration.from_pretrained(model_name).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # prompt = "Hey, how are you doing today? My name is Jenny, and I'm here to help you with any questions you have."
    # description = "Jenny speaks at an average pace with an animated delivery in a very confined sounding environment with clear audio quality."

    input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
    prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

    generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    audio_arr = generation.cpu().numpy().squeeze()
    sf.write(file_path, audio_arr, model.config.sampling_rate)

def get_transcription(file_path: str):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return text

def get_references():
    file_path = "prompts.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    return [[lines[i], lines[i+1]] for i in range(0, len(lines), 2)]

def generate_group(references, group_name: str = "simple"):
    for index, prompt in enumerate(references):
        speech_generation(prompt[0], prompt[1], group_name + str(index + 1) + ".wav")

def filter_sent(sentence: str):
    return ''.join(char.lower() for char in sentence if char not in string.punctuation)

def word_error_rate(references, group_name: str = "simple", cycles: int = 5):
    average = 0
    for _ in range(cycles):
        rates = []
        for index, reference in enumerate(references):
            hypothesis = get_transcription(group_name + str(index + 1) + ".wav")
            rates.append(wer(filter_sent(reference[0]), filter_sent(hypothesis)))
        average += np.array(rates).sum() / len(rates)
    return average / cycles

def mcd(reference_file, synthesized_file):
    ref_signal, _ = librosa.load(reference_file, sr=None)
    synth_signal, _ = librosa.load(synthesized_file, sr=None)

    ref_mel = librosa.feature.melspectrogram(ref_signal)
    synth_mel = librosa.feature.melspectrogram(synth_signal)

    return np.sqrt(np.sum((ref_mel - synth_mel) ** 2))


prompt = ("I, Jude Duarte, high Queen of Elf haman exile, "
    "spend most mornings dozing in front of daytime television")
description = ("The speaker reads slowly, measuredly, "
               "pauses at commas, and emphasizes his position",
               "In the second part put emphasis on the word:most,  and on the word: daytime")
file_name = "parler4.wav"
speech_generation(prompt, description, file_path=file_name)

speech_generation(
    "I, Jude Duarte, high Queen of Elf haman exile, "
    "spend most mornings dozing in front of daytime television",
    "The speaker reads slowly, measuredly, pauses at commas, and emphasizes his position"
    ".",
    "parler3.wav")

# "he speaks slowly, with pauses"
#  In the second part put emphasis on the word:most,  and on the word: daytime



