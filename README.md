# lc-demo
This is a demo for a way to have a real time voice conversation with a bot by using Speech To Text (STT), Large Language Models (LLM), and Text To Speech (TTS) to handle every part of the conversation.

LC stands for Live Chat

The models we're using are 

https://replicate.com/vaibhavs10/incredibly-fast-whisper


https://replicate.com/meta/llama-2-13b-chat


https://replicate.com/awerks/neon-tts

To run the demo, use poetry to install the dependencies:

```bash
poetry install
```

And then simply:

```bash
poetry run python lcdemo.py
```

The app will prompt you to hit enter to record a 10 second message, then the app will use Whisper to translate that into text. Then it will feed that output to Llama to generate a response. Then it will pass that response to neon-tts to read it out loud to the user. At which point the user can record another message. There is currently no memory, so the bot won't remember previous parts of the conversation.

## Next Steps

As this is a demo, and the objective is to have a real time conversation, the next step must involve optimising the project for speed. For that we can do things like make use of models with streaming output and input, such that the models can begin processing the conversation whilst the user is still talking without interrupting. 

Multithreading and parallelisation are also worth considering.




