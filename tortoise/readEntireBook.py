# This file was created because:
# read.py gives up after around 90ish voice clips but many books are much longer than that.
# This file will allow client to paste an entire book or chapter and it will automatically split it into sections
# And automatically encode every 90 clip using read.py then use merger.py to merge them into a single audio book 
# chapter

# We will conservatively assume that the limit is 10000 characters (in actuality its more like 20000)
from utils.text import split_and_recombine_text
from tortoise_api import convert_text_to_speech
from merger import mergeFiles
from tqdm import tqdm
import os

with open("temporary_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

voice = "train_dotrice"

characterLimit = 10000
sentences = split_and_recombine_text(text)

# Split sentences into 10000 character clusters
clusters = []
cluster = []

elapsedCharCount = 0
for sentenceIndex in range(len(sentences)):
    sentence = sentences[sentenceIndex]
    elapsedCharCount += len(sentence)
    cluster.append(sentence)

    if elapsedCharCount > 10000:
        clusters.append(cluster)
        cluster = []
        elapsedCharCount = 0

arguments = f"--voice {voice} --preset fast --textfile temporary_text.txt --output_path desired_outputs\\longform"

tqdm(leave=False)

files = []
clusterFiles = []
readnum = 0
cluster = 0

for cluster in tqdm(clusters, desc="Clusers"): #Todo: add tqdm progress bar
    for sentence in tqdm(cluster, desc="Sentences"):
        generations = convert_text_to_speech(sentence, voice, "fast", 1, f"{voice}_{str(readnum)}") # Returns paths to generated files
        files.extend(generations)
        clusterFiles.extend(generations)
        readnum += 1
        
    mergeFiles(clusterFiles, f"cluster_{cluster}")
    clusterFiles = []
    cluster = cluster + 1

print("Almost done, merging files")
mergeFiles(files, "all_chapters_merged")
