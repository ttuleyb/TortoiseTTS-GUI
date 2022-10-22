import os
import gradio as gr
# import utils
# import api
import scipy
# import tortoise_api
from tortoise_api import convert_text_to_speech
import torch

#Migrate API to a seperate script and use cls to access it for easy unloading

if not os.path.exists("desired_outputs/longform"):
    os.makedirs("desired_outputs/longform")

presetSymbols = {'ultra fast':'ultra_fast', 'fast':'fast', 'standard':'standard', 'high quality': 'high_quality'}
characterSymbols = {"Sam Harris": "SamH", "Jordan Peterson": "JordanP", "Donald Trump": "DTrump", "Kurzegesagt": "Kurzeg", "Adam Something": "AdamSo", "Bad Empanada": "BadEmp", "Ben Shapiro": "BenS", "Boris Johnson": "BorisJ", "Dennis Prager": "DennisP", "Freeman": "freeman", "Rick Sanchez": "RickS", "Two Minute Papers": "TwoMin"}

def fileFormatter(files):
    #Read each file and format to work with gradioUI
    for filen in range(len(files)): #Read all data's from the files
        files[filen] = scipy.io.wavfile.read(files[filen])

    if len(files) < 3: #Fill empty files to ensure fixed output size
      while len(files) < 3:
          files.append("desired_outputs\\empty.wav") #Add empty file to avoid list out of index error

    return files

def text_to_speech(text, voice, preset, readMode, numOfOutputs):
    #Use dictionary to convert strings into symbols readable by the api
    voiceSymbol = characterSymbols[voice]
    presetSymbol = presetSymbols[preset]

    if readMode == "longform":
        torch.cuda.empty_cache()
        with open("temporary_text.txt", "w") as f:
            f.write(text)

        arguments = f"--voice {voiceSymbol} --preset {presetSymbol} --textfile temporary_text.txt --output_path desired_outputs\\longform"

        files = [f"desired_outputs\\longform\\{voiceSymbol}\\combined.wav"]

        os.system(f"python tortoise\\read.py {arguments}")

        #format files
        files = fileFormatter(files)

        return files

    #Create and get files
    files = convert_text_to_speech(text, voiceSymbol, presetSymbol, numOfOutputs)

    #format files
    files = fileFormatter(files)

    return files

tripleOutput = gr.Interface(
    
    fn = text_to_speech, #Function
    inputs = [ #Inputs
        gr.Textbox(
            label="Text to speak",
            lines=3,
            value="Haha that's crazy bro",
        ),
        
        gr.Dropdown(["Sam Harris", "Jordan Peterson", "Donald Trump", "Kurzegesagt", "Adam Something", 
        "Bad Empanada", "Ben Shapiro", "Boris Johnson", "Dennis Prager", "Freeman", "Rick Sanchez", 
        "Two Minute Papers"], value="Sam Harris", label="Voice"),

        gr.Radio(["ultra fast", "fast", "standard", "high quality"], value="fast", label="Speed"),

        gr.Radio(["sentence", "longform"], value="sentence", label="Reading Mode"),

        gr.Slider(1, 3, value=3, step=1, label="How many generations do you want?"),
    ],
    outputs = ["audio", "audio", "audio"], #Outputs
    examples=[
        ["I tell them hell yeah! America is great", "Donald Trump", "fast", "sentence", 3],
        ["The universe's third eye is visible when you really look for it", "Sam Harris", "fast","sentence", 2],
        ["The woke liberals are overrunning our university campuses", "Ben Shapiro","sentence", "fast", 3],
        ["Liz Truss, absolute wanker", "Boris Johnson", "fast", "sentence", 3],
        ["Hello dear scholars, Today I'm showing the new sentient AI", "Two Minute Papers", "fast", "longform", 1]
    ],
)

demo = tripleOutput

if __name__ == "__main__":
    #Remove server_name="0.0.0.0" if you don't want to share with your entire wifi network
    demo.launch(server_name="0.0.0.0", share=False) #Keep share false unless you disable longform or fix the arbitary code execution
