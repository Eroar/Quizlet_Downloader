import requests
import sys
from bs4 import BeautifulSoup
from pprint import pprint
import pyperclip

def getSoup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

def getTermsFromLeftSide(soup):
    termsClasses = soup.find_all("div", {"class": "SetPageTerms-term"})
    leftSides = []
    for termClass in termsClasses:
        text = termClass.find("span", {"class": "TermText notranslate lang-de"}).text
        leftSides.append(text)
    return leftSides

if __name__ == "__main__":
    sysArgs = sys.argv
    link = sysArgs[1]
    soup = getSoup(link)
    leftTerms = getTermsFromLeftSide(soup)
    pprint(leftTerms)

    string2Copy = "\n".join(leftTerms)

    pyperclip.copy(string2Copy)