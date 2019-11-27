import os
import shutil

import requests
from bs4 import BeautifulSoup
from pydub import AudioSegment

from .Term import Term

class Quizlet:
    def __init__(self, quizletsUrl, langLeft, langRight, debug=False):
        self._debug = debug
        self._quizletsUrl = quizletsUrl
        if self._debug:
            print("Downloading soup")
        soup = self._getSoup(quizletsUrl)
        if self._debug:
            print("Soup downloaded")
        self._langLeft = langLeft
        self._langRight = langRight
        self._leftTerms = self._getTermsFromLeftSide(soup)
        self._rightTerms = self._getTermsFromRightSide(soup)
        if self._debug:
            print("leftTerms length:", len(self._leftTerms))
            print("rightTerms length:", len(self._rightTerms))

    
    def __str__(self):
        return f"Quizlet, lang:{self._langLeft}:{self._langRight}, size:{len(self._leftTerms)}"

    def getUrl(self):
        return self._quizletsUrl
    
    def getLeftTerms(self):
        return self._leftTerms

    def getRightTerms(self):
        return self._rightTerms

    def createMp3(self, fileName, pauseBW=700, pauseAW=1000, first="left"):
        '''
        pauseBW - pause between words in milliseconds
        pauseAW - pause after words in milliseconds
        '''
        self._createMp3WordsFiles(first=first)
        tmpPath = os.path.join(os.getcwd(), "tmp")
        print(f"Creating the final file \"{fileName}\".mp3")
        finalMp3 = AudioSegment.empty()
        for i in range(len(self._leftTerms)):
            filePath = os.path.join(tmpPath, f"l_{i}") + ".mp3"
            left = AudioSegment.from_file(filePath, format="mp3")
            finalMp3 += left + AudioSegment.silent(pauseBW)

            filePath = os.path.join(tmpPath, f"r_{i}") + ".mp3"
            right = AudioSegment.from_file(filePath, format="mp3")
            finalMp3 += right + AudioSegment.silent(pauseBW)
            if self._debug:
                numOfBlocks = int(100*(i+1)/len(self._leftTerms))
                numOfSpaces = 100 - numOfBlocks
                blocks = u"\u2588" *  numOfBlocks
                spaces = " " * numOfSpaces
                print("[" + blocks +  spaces + "]", end="\r", flush=True)
        print("[" + blocks +  spaces + "]")

        finalMp3.export(f"{fileName}.mp3", format="mp3")
        path = os.path.join(os.getcwd(), "tmp")
        shutil.rmtree(path)
            

    def _createMp3WordsFiles(self, first="left"):
        if first == "left":
            leftRightTerms = zip(self._leftTerms, self._rightTerms, range(len(self._leftTerms)))
        elif first == "right":
            leftRightTerms = zip(self._rightTerms, self._leftTerms, range(len(self._leftTerms)))
        else:
            raise Exception(f"Invalid argument \"first\"={first}, should be \"left\" or \"right\"")
        
        if self._debug:
            print("Creating tts for left Terms")
        self._createTtsForTerms("left")
        if self._debug:
            print("Creating tts for right Terms")
        self._createTtsForTerms("right")

        tmpPath = os.getcwd()
        tmpPath = os.path.join(tmpPath, "tmp")
        os.mkdir(tmpPath)
        if self._debug:
            print("Generating mp3 files for words")

        for left, right, i in leftRightTerms:
            left.saveTts(os.path.join(tmpPath, f"l_{i}") +".mp3")
            right.saveTts(os.path.join(tmpPath, f"r_{i}")+".mp3")

            if self._debug:
                numOfBlocks = int(100*(i+1)/len(self._leftTerms))
                numOfSpaces = 100 - numOfBlocks
                blocks = u"\u2588" *  numOfBlocks
                spaces = " " * numOfSpaces
                print("[" + blocks +  spaces + "]", end="\r", flush=True)
        if self._debug:
            print("[" + blocks +  spaces + "]")

    def _createTtsForTerms(self, side):
        if side == "left":
            for i, term in enumerate(self._leftTerms):

                term.createTts()
                if self._debug:
                    numOfBlocks = int(100*(i+1)/len(self._leftTerms))
                    numOfSpaces = 100 - numOfBlocks
                    blocks = u"\u2588" *  numOfBlocks
                    spaces = " " * numOfSpaces
                    print("[" + blocks +  spaces + "]", end="\r", flush=True)
            print("[" + blocks +  spaces + "]")

        elif side == "right":

            for i, term in enumerate(self._rightTerms):

                term.createTts()
                if self._debug:
                    numOfBlocks = int(100*(i+1)/len(self._leftTerms))
                    numOfSpaces = 100 - numOfBlocks
                    blocks = u"\u2588" *  numOfBlocks
                    spaces = " " * numOfSpaces
                    print("[" + blocks +  spaces + "]", end="\r", flush=True)
            print("[" + blocks +  spaces + "]")

        else:
            raise Exception(f"Invalid argument \"side\"={side}, should be \"left\" or \"right\"")

    def _getSoup(self, url):
        response = requests.get(url)
        return BeautifulSoup(response.text, "html.parser")

    def _getTermsFromLeftSide(self, soup):
        termsClasses = soup.find_all("div", {"class": "SetPageTerm-content"})
        leftSides = []
        for termClass in termsClasses:
            a = termClass.find("a", {"class": "SetPageTerm-wordText"})
            if a != None:
                term = Term(a.text, self._langLeft, False)
                leftSides.append(term)
        return leftSides

    def _getTermsFromRightSide(self, soup):
        termsClasses = soup.find_all("div", {"class": "SetPageTerm-content"})
        rightSide = []
        for termClass in termsClasses:
            a = termClass.find("a", {"class": "SetPageTerm-definitionText"})
            if a != None:
                span = a.find("span")
                if span != None:
                    term = Term(span.text, self._langRight, False)
                    rightSide.append(term)
        return rightSide

    def convertToString(self, leftTerms, rightTerms, between=" - ", firstTermsSide="left", end="\n"):
        outString = ""
        if len(leftTerms) != len(rightTerms):
            raise Exception("left and right terms are not equal sizes")

        if firstTermsSide == "left":
            for i in range(len(leftTerms)):
                outString += leftTerms[i] + between + rightTerms[i]  + end
        
        elif firstTermsSide == "right":
            for i in range(len(leftTerms)):
                outString += rightTerms[i] + between + leftTerms[i] + end
        else:
            raise Exception("\"firstTermsSide\" argument should be \"left\" or \"right\"")

        return outString