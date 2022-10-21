from symbol import single_input
import gradio as gr
import utils
import api
import scipy
from api import *
import subprocess
import tortoise_api
from tortoise_api import convert_text_to_speech

presetSymbols = {'ultra fast':'ultra_fast', 'fast':'fast', 'standard':'standard', 'high quality': 'high_quality'}
characterSymbols = {"Sam Harris": "SamH", "Jordan Peterson": "JordanP", "Donald Trump": "DTrump", "Kurzegesagt": "Kurzeg", "Adam Something": "AdamSo", "Bad Empanada": "BadEmp", "Ben Shapiro": "BenS", "Boris Johnson": "BorisJ", "Dennis Prager": "DennisP", "Freeman": "freeman", "Rick Sanchez": "RickS", "Two Minute Papers": "Two Min"}

def text_to_speech(text, voice, preset, numOfOutputs):
    #Use dictionary to convert strings into symbols readable by the api
    voiceSymbol = characterSymbols[voice]
    presetSymbol = presetSymbols[preset]

    #Create and get files
    files = convert_text_to_speech(text, voiceSymbol, presetSymbol, numOfOutputs)

    #Read each file
    for filen in range(len(files)):
        files[filen] = scipy.io.wavfile.read(files[filen])

    if len(files) < 3:
      while len(files) < 3:
          files.append("desired_outputs\\empty.wav") #Add empty file to avoid list out of index error

    print(files)

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

        gr.Slider(1, 3, value=3, step=1, label="How many generations do you want?"),
    ],
    outputs = ["audio", "audio", "audio"], #Outputs
    examples=[
        ["I tell them hell yeah! America is great", "Donald Trump", "fast", 3],
        ["The universe's third eye is visible when you really look for it", "Sam Harris", "fast", 2],
        ["The woke liberals are overrunning our university campuses", "Ben Shapiro", "fast", 3],
        ["Liz Truss, absolute wanker", "Boris Johnson", "fast", 3]
    ],
)

demo = tripleOutput

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", share=True) #secret, 44IQUFmIQWOAZGJ
