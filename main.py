from Quizletpy.Quizlet import Quizlet

q = Quizlet("https://quizlet.com/pl/456649012/malec-pytel-2111-flash-cards/", "en", "pl", debug=True)
q.createMp3("malec_pytel", pauseBW=500, pauseAW=1200, first="right")