import requests
import pyperclip
from bs4 import BeautifulSoup

def getArtikel(word):
    response = requests.get("https://www.diki.pl/slownik-niemieckiego?q=" + word)
    soup = BeautifulSoup(response.text, "html.parser")
    entity = soup.find("div", {"class":"dictionaryEntity"})
    wordWA =  entity.find("a", {"class" : "plainLink"}).text
    return wordWA

wordsTT = pyperclip.paste().split("\n")
wordsWA = []
wordsNotFound = []

for word in wordsTT:
    try:
        wordsWA.append(getArtikel(word))
    except:
        print(word)
        wordsNotFound.append(word)

pyperclip.copy(".\n".join(wordsWA))
input("Enter to continue")
pyperclip.copy(".\n".join(wordsNotFound))
