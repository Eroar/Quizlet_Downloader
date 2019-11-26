from gtts import gTTS
import sys
from pydub import AudioSegment

def getTtsFromString(string, lang):
    '''
    fileName with no extension
    '''
    return gTTS(string, lang)

def main():
    lang = sys.argv[1]
    with open("text2mp3Input.txt", "r") as f:
        s = f.read()
    
    tts = getTtsFromString(s)
    fileName += ".mp3"
    tts.save(fileName)



if __name__ == "__main__":
    main()