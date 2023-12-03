## This is a demo for a bot that uses TTS, SST, and LLM models to have a real time conversation with an user

import time
import logging
import replicate
import sounddevice as sd
from scipy.io.wavfile import write as scwrite
import vlc


# set up logging
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

if __name__ == "__main__":
    while(True):
        ## record the audio

        logging.info("starting program \n--------------------------------------------------")
        print("Record a message to start the conversation. When you press enter, you'll have 10 seconds to record your message.")
        input("Press enter to begin recording")
        logging.info("now recording")


        fs = 44100  # Sample rate
        seconds = 10  # Duration of recording

        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        logging.info("finished recording. Saving as recording.wav")
        scwrite('recording.wav', fs, myrecording)  # Save as WAV file

        ##put it through whispr
        logging.info("\n----------------interpreting recording with whispr------------\n")
        sttout = replicate.run(
            "vaibhavs10/incredibly-fast-whisper:65fa8e5a537c692838805dee5e8e845e4c8a70f909ba23b28434b7525b94020e",
            input={"audio": open("recording.wav", "rb"),}


        )

        logging.info(f"whisper output: {sttout}")

        ## put it through llama

        transcript= sttout["text"]
        system_prompt = ("You are a helpful, respectful and honest assistant. You are free to choose your own name and personality.\n"
                "The following is a conversation you had with an user. \n"
                )
        prompt=f"User: {transcript}"
        llmout = replicate.run(
         "meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d",
        input={
            "debug": False,
            "top_k": 50,
            "top_p": 1,
            "prompt": prompt,
            "temperature": 0.5,
            "system_prompt": system_prompt,
            "max_new_tokens": 200,
            "min_new_tokens": -1
            }
        )
        response = ''.join(llmout)

        logging.info(f"llama output: {response}")


        ## put it through neontts



        ttsout = replicate.run(
        "awerks/neon-tts:139606fe1536f85a9f07d87982400b8140c9a9673733d47913af96738894128f",
        input={
            "text": response ,
            "language": "en"
        }
        )

        logging.info(f"tts output url: {ttsout}")

        # ## Play back the audio 
        vlc_instance = vlc.Instance()
        player = vlc_instance.media_player_new()
        media = vlc_instance.media_new(ttsout)
        player.set_media(media)
        player.play()
        time.sleep(1.5)
        duration = player.get_length() / 1000
        time.sleep(duration)


