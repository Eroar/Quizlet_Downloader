from gtts import gTTS
import sys

def getTtsFromString(string, lang):
    '''
    fileName with no extension
    '''
    return gTTS(string, lang)

def main():
    lang = sys.argv[1]
    with open("text2mp3Input.txt", "r") as f:
        s = f.read()
    
    tts = getTtsFromString(s, lang)
    fileName = "text2mp3Output.mp3"
    tts.save(fileName)

if __name__ == "__main__":
    main()