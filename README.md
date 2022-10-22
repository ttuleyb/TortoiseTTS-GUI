# TortoiseTTS GUI
## What is this?
This is a gradio GUI to make it easier to use [Tortoise TTS](https://github.com/neonbjb/tortoise-tts) **Check it out for more information such as cloning your own voice or others**

You can find guides and demo colab link in there. I've yet to make a colab to include the gui but it should be fairly easy.

## What does this repo include?
The gradioUI I've written in python and a simple middleman script I've created to make it easier to interact with the api.

## Installation
Follow the installation guide here [Tortoise Local Installation](https://github.com/neonbjb/tortoise-tts#local-installation) then simply put the files in the root directors, create a shell there and run gradeui.py

## WARNING
Don't use the --share option when launching gradio as it can be used to run arbitrary code on your machine. This is due to the longform implementation involving passing an argument to cmd which can be hijacked.

## What's up with the voice selections?
Those are just the voices I've made myself, unfortunately I don't want to be hold liable publishing anyone elses voice on GitHub so you need to find recordings of the voices of the people you want to use yourself. More info in the Tortoise TTS repo.
