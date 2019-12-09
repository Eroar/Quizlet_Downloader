from Quizletpy.Quizlet import Quizlet
import sys


ILLEGAL_CHARS = set(["<", ">", ":", "\"", "/", "\\", "|", "?", "*"])

def main(args):
    url = ""
    outfile = ""
    langL = ""
    langR = ""
    first = "left"
    pauseBW = 500
    pauseAW = 1200

    if len(args) == 4:
        url = args[0]
        langL = args[1]
        langR = args[2]
        outfile = args[3]
    else:
        for i, arg in enumerate(args):
            if arg == "-url":
                url = args[i+1]

            elif arg == "-langs":
                langL = args[i+1]
                langR = args[i+2]

            elif arg == "-outfile":
                for iChar in ILLEGAL_CHARS:
                    if iChar in args[i+1]:
                        print(f"Illegal character \"{iChar}\" in folder name")
                        return
                outfile = args[i+1]
            
            elif arg == "-first":
                first = args[i+1]

            elif arg == "-pauseBW":
                pauseBW = args[i+1]
            
            elif arg == "-pauseAW":
                pauseAW = args[i+1]

    q = Quizlet(url, langL, langR, debug=True)
    q.createMp3(outfile, pauseBW=pauseBW, pauseAW=pauseAW, first=first)

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
