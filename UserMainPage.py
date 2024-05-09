from tkinter import Tk, Canvas, Text, Button
import tkinter as tk
import subprocess
import sys  
import time
from Util import Util

connection = Util.ConnectMysql()
window = Tk()
window.geometry("747x531")
window.configure(bg = "#FFFFFF")

userID = sys.argv[1]

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 531,
    width = 747,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
StudyDayBtn = tk.Button(text = "단어 학습", command=lambda:Util.SwitchPage(window, "UserStudyDayPage", userID))
StudyDayBtn.place(x=283, y=100, width=180, height=80)

ManageUserBtn = tk.Button(text="단어 시험", command=lambda:Util.SwitchPage(window, "UserExamDayPage", userID))
ManageUserBtn.place(x=283, y=200, width=180, height=80)

StudyDayBtn = tk.Button(text = "게임", command=lambda:Util.SwitchPage(window, "game", userID))
StudyDayBtn.place(x=283, y=300, width=180, height=80)

LogOutBtn = tk.Button(text = "로그아웃")
LogOutBtn.place(x=283, y=400, width=180, height=80)



window.resizable(False, False)
window.mainloop()
