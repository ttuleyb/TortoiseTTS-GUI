# Combine all wav files under the folder "voice_files" into a single file "combined.wav"

import os
import pydub
from tqdm import tqdm

# Get the list of all files in directory tree at given path
listOfFiles = list()
for (dirpath, dirnames, filenames) in os.walk(r"C:\Users\User\tortoise-tts\desired_outputs\longform\train_atkins"):
    listOfFiles += [os.path.join(dirpath, file) for file in filenames]

# Print the files
for elem in listOfFiles:
    print(elem)

# Create a single file "combined.wav"
combined = pydub.AudioSegment.empty()
for file in tqdm(listOfFiles):
    sound = pydub.AudioSegment.from_wav(file)
    combined += sound

combined.export("combined.wav", format="wav")
