from tkinter import Tk, Canvas, Button
import tkinter as tk
import sys
from Util import Util
from LoginPage import LoginPage

class UserMainPage(tk.Tk):
    def __init__(self, userID):
        super().__init__()
        self.geometry("747x531")
        self.configure(bg="#FFFFFF")
        self.resizable(False, False)
        self.userID = userID
        self.connection = Util.ConnectMysql()
        self.canvas = Canvas(
            bg="#FFFFFF",
            height=531,
            width=747,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        
        self.UserIDLabel = tk.Label(self, text=userID)
        self.UserIDLabel.place(x=300, y=0, width=100, height=30)
        
        self.studyDayBtn = tk.Button(text="단어 학습", command=lambda: Util.SwitchPage("UserStudyDayPage", self.userID))
        self.studyDayBtn.place(x=283, y=100, width=180, height=80)

        self.manageUserBtn = tk.Button(text="단어 시험", command=lambda: Util.SwitchPage("UserExamDayPage", self.userID))
        self.manageUserBtn.place(x=283, y=200, width=180, height=80)

        self.gameBtn = tk.Button(text="게임", command=lambda: Util.SwitchPage("game", self.userID))
        self.gameBtn.place(x=283, y=300, width=180, height=80)

        self.logOutBtn = tk.Button(text="로그아웃", command=self.SwitchToLoginPage)
        self.logOutBtn.place(x=283, y=400, width=180, height=80)
        
    def SwitchToLoginPage(self):
            self.cursor = self.connection.cursor()
            self.cursor.execute("UPDATE user SET isaccess = 0 WHERE id = %s",(userID,))
            self.connection.commit()  # 커밋을 수행하여 변경 사항을 DB에 적용
            self.cursor.close()  # 커서 닫기 
            self.destroy()
            app = LoginPage(self)
            app.mainloop()
if __name__ == "__main__":
    userID = sys.argv[1] if len(sys.argv) > 1 else 'default_user'
    app = UserMainPage(userID)
    app.mainloop()