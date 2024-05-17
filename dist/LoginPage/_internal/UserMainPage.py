from tkinter import Tk, Canvas, Button
import tkinter as tk
import sys
from Util import Util

class UserMainPage:
    def __init__(self, master):
        self.master = master
        self.master.geometry("747x531")
        self.master.configure(bg="#FFFFFF")
        self.master.resizable(False, False)

        self.userID = sys.argv[0]
        self.canvas = Canvas(
            master,
            bg="#FFFFFF",
            height=531,
            width=747,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.studyDayBtn = tk.Button(master, text="단어 학습", command=lambda: Util.SwitchPage(master, "UserStudyDayPage", self.userID))
        self.studyDayBtn.place(x=283, y=100, width=180, height=80)

        self.manageUserBtn = tk.Button(master, text="단어 시험", command=lambda: Util.SwitchPage(master, "UserExamDayPage", self.userID))
        self.manageUserBtn.place(x=283, y=200, width=180, height=80)

        self.gameBtn = tk.Button(master, text="게임", command=lambda: Util.SwitchPage(master, "game", self.userID))
        self.gameBtn.place(x=283, y=300, width=180, height=80)

        self.logOutBtn = tk.Button(master, text="로그아웃")
        self.logOutBtn.place(x=283, y=400, width=180, height=80)

        print(self.userID)

    def run(self):
        self.master.mainloop()

if __name__ == "__main__":
    root = Tk()
    app = UserMainPage(root)
    app.run()