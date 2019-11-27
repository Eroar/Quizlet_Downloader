from gtts import gTTS

class Term:
    def __init__(self, word, lang, ttsAtInstant=True):
        self._word = word
        self._lang = lang
        self._tts = None

        if ttsAtInstant:
            self._tts = self.getTts()
        
    def __str__(self):
        return self._word
    
    def isTtsCreated(self):
        if self._tts == None:
            return False
        else:
            return True

    def createTts(self):
        if self._tts == None:
            self._tts = gTTS(self._word, self._lang)
        else:
            return self._tts

    def getLang(self):
        return self._lang
    
    def getString(self):
        return self._word

    def getTts(self):
        '''
        fileName with no extension
        '''
        if self._tts == None:
            return gTTS(self._word, self._lang)
        else:
            return self._tts
    
    def saveTts(self, fileName=None):
        if fileName == None:
            fileName = f"{self._word}.mp3"
        if self._tts != None:
            self._tts.save(fileName)
        else:
            raise Exception("tts doesn't exist")
