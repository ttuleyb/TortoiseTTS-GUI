from pathlib import Path
import api
import tortoise
import torchaudio
import os
import random

if not os.path.exists("desired_outputs"):
    os.makedirs("desired_outputs")

#Cache things for faster access
characterSymbols = {"Sam Harris": "SamH",  "Ben S2": "Shapiro2", "Jordan Peterson": "JordanP", "Second Thought": "Second", "Donald Trump": "DTrump", "Kurzegesagt": "Kurzeg", "Hakim": "Hakim", "Adam Something": "AdamSo", "Bad Empanada": "BadEmp", "Ben Shapiro": "BenS", "Boris Johnson": "BorisJ", "Dennis Prager": "DennisP", "Freeman": "freeman", "Rick Sanchez": "RickS", "Two Minute Papers": "TwoMin"}
characters = dict.values(characterSymbols)

characterCachedVoices = {}

#Load each listed characters voice into memory
for character in characters:
    clips_paths = Path(f"tortoise/voices/{character}").glob("**/*.wav")
    reference_clips = [tortoise.utils.audio.load_audio(p.absolute().__str__(), 22050) for p in clips_paths]
    characterCachedVoices[character] = reference_clips

print("Done caching voices")

def convert_text_to_speech(text, voice, preset, numOfOutputs):    
    reference_clips = characterCachedVoices[voice] #Immediately load voice samples from RAM

    #Initialise tts api
    tts = api.TextToSpeech()
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

    del gen

    return files

print("Loaded middleman")