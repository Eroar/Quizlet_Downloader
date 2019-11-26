from gtts import gTTS
import sys

def main():
    lang = sys.argv[1]
    with open("text2mp3Input.txt", "r") as f:
        s = f.read()

    file = "text2mp3Output.mp3"

    # initialize tts, create mp3 and play
    tts = gTTS(s, lang)
    tts.save(file)

if __name__ == "__main__":
    main()