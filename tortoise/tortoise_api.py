from pathlib import Path
import api
from tortoise import utils
import torchaudio
import os
import random

if not os.path.exists("desired_outputs"):
    os.makedirs("desired_outputs")

#Cache things for faster access
characterSymbols = {"Sam Harris": "SamH", "Jordan Peterson": "JordanP", "Donald Trump": "DTrump", "Kurzegesagt": "Kurzeg", "Adam Something": "AdamSo", "Bad Empanada": "BadEmp", "Ben Shapiro": "BenS", "Boris Johnson": "BorisJ", "Dennis Prager": "DennisP", "Freeman": "freeman", "Rick Sanchez": "RickS", "Two Minute Papers": "Two Min"}
characters = dict.values(characterSymbols)

characterCachedVoices = {}

#Load each listed characters voice into memory
for character in characters:
    clips_paths = Path(f"tortoise/voices/{character}").glob("**/*.wav")
    reference_clips = [utils.audio.load_audio(p.absolute().__str__(), 22050) for p in clips_paths]
    characterCachedVoices[character] = reference_clips

#Initialise tts api
tts = api.TextToSpeech()
print("Done caching voices")

def convert_text_to_speech(text, voice, preset, numOfOutputs):    
    reference_clips = characterCachedVoices[voice] #Immediately load voice samples from RAM

    gen = tts.tts_with_preset(text, voice_samples=reference_clips, preset=preset, k=numOfOutputs) #Generate speech

    randomNum = str(random.randint(1,1000000))
    files = []

    if isinstance(gen, list): #If multiple outputs save each
        for j, g in enumerate(gen):
            filename = os.path.join("desired_outputs", f'{randomNum}{j}.wav')
            torchaudio.save(filename, g.squeeze(0).cpu(), 24000)
            files.append(filename)
    else: #Or just save the single output
        filename = os.path.join("desired_outputs", f'{randomNum}.wav')
        torchaudio.save(filename, gen.squeeze(0).cpu(), 24000)
        files.append(filename)

    return files
