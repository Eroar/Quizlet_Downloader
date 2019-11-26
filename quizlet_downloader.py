import requests
import sys
from bs4 import BeautifulSoup
from pprint import pprint
import pyperclip

def getSoup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

def getTermsFromLeftSide(soup):
    termsClasses = soup.find_all("div", {"class": "SetPageTerm-content"})
    leftSides = []
    for termClass in termsClasses:
        a = termClass.find("a", {"class": "SetPageTerm-wordText"})
        if a != None:
            leftSides.append(a.text)
            # span = a.find("span")
            # if span != None:
            #     leftSides.append(span.text)

    return leftSides

def getTermsFromRightSide(soup):
    termsClasses = soup.find_all("div", {"class": "SetPageTerm-content"})
    rightSide = []
    for termClass in termsClasses:
        a = termClass.find("a", {"class": "SetPageTerm-definitionText"})
        if a != None:
            span = a.find("span")
            if span != None:
                rightSide.append(span.text)

    return rightSide

def convertToString(leftTerms, rightTerms, between=" - ", firstTermsSide="left", end="\n"):
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

if __name__ == "__main__":
    sysArgs = sys.argv
    link = sysArgs[1]
    soup = getSoup(link)
    leftTerms = getTermsFromLeftSide(soup)
    rightTerms = getTermsFromRightSide(soup)
    
    string2Copy = convertToString(leftTerms, rightTerms, between=" ", firstTermsSide="right", end="\n")

    # string2Copy = "\n".join(leftTerms)
    # string2Copy = "\n".join(rightTerms)
    pyperclip.copy(string2Copy)

    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(string2Copy)
