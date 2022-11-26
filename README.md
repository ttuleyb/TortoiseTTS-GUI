# TortoiseTTS GUI
## What is this?
This is a gradio GUI to make it easier to use [Tortoise TTS](https://github.com/neonbjb/tortoise-tts) **Check it out for more information such as cloning your own voice or others**

You can find guides and demo colab link in there. I've yet to make a colab to include the gui but it should be fairly easy.

## What does this repo include?
The gradioUI I've written in python and a simple middleman script I've created to make it easier to interact with the api.

## Installation
Follow the installation guide here [Tortoise Local Installation](https://github.com/neonbjb/tortoise-tts#local-installation) then simply put the files in the root directors, create a shell there and run gradeui.py.
If you wanna use merger.py ensure that ffprobe is in the path or working directory, otherwise you might get file not found error.

## Sentence vs Longform
Sentence should be used when synthesizing one or two sentences whereas longform should be used for longer content. Sentence works like [do_tts.py](https://github.com/neonbjb/tortoise-tts#do_ttspy) whereas longform works like [read.py](https://github.com/neonbjb/tortoise-tts#readpy). Keep in mind that longform will only return a single clip regardless of selected numOfOutputs.

## WARNING - Update
I'm not a 100% sure if arbitary code can be executed because I'm using cmd while generating longform audio. All requests are checked against a dictionary except the text so the text is the only thing that could be a possible attack vector. However the text is written to a txt file then the read.py reads it from there so unless there is an exploit that can execute code using the read.py it should be safe.

## What's up with the voice selections?
Those are just the voices I've made myself, unfortunately I don't want to be hold liable publishing anyone elses voice on GitHub so you need to find recordings of the voices of the people you want to use yourself. More info in the Tortoise TTS repo.
