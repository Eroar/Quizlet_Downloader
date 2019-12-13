from Quizletpy.Quizlet import Quizlet
import sys


ILLEGAL_CHARS = set(["<", ">", ":", "\"", "/", "\\", "|", "?", "*"])

def getIllegalChars(stringT):
    for iChar in ILLEGAL_CHARS:
        if iChar in stringT:
            return iChar
    return ""

def main(args):
    url = ""
    outfileName = "mp3Output"
    langL = ""
    langR = ""
    first = "left"
    pauseBW = 500
    pauseAW = 1200
    createMp3 = False
    createTxt = False
    between=" - "
    firstTermsSide="left", 
    end="\n"

    if len(args)==0:
        print("No arguments")
        return
    if len(args) == 4:
        url = args[0]
        langL = args[1]
        langR = args[2]
        outfileName = args[3]
    else:
        for i, arg in enumerate(args):
            if arg == "-url":
                url = args[i+1]
            
            elif arg== "-help":
                with open("help.txt", "r") as f:
                    print(f.read())
                    return
            elif arg == "-langs":
                langL = args[i+1]
                langR = args[i+2]
            
            elif arg == "-text":
                createTxt = True
                illegalChar = getIllegalChars(args[i+1])
                if illegalChar != "":
                    print(f"Illegal character \"{illegalChar}\" in file name")
                    return
                else:
                    txtOutFile = args[i+1]

            elif arg == "-mp3":
                createMp3 = True
                illegalChar = getIllegalChars(args[i+1])
                if illegalChar != "":
                    print(f"Illegal character \"{illegalChar}\" in file name")
                    return
                else:
                    mp3OutFile = args[i+1]
            
            elif arg == "-first":
                first = args[i+1]

            elif arg == "-pauseBW":
                pauseBW = args[i+1]
            
            elif arg == "-pauseAW":
                pauseAW = args[i+1]

    quizlet = Quizlet(url, langL, langR, debug=True)
    if createMp3:
        quizlet.createMp3(mp3OutFile, pauseBW=pauseBW, pauseAW=pauseAW, first=first)
    if createTxt:
        quizlet.words2TextFile(txtOutFile)

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
