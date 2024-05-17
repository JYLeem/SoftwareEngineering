import tkinter as tk
from tkinter import Canvas, messagebox
import mysql.connector
from Util import Util


class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("로그인")
        self.geometry("747x531")
        self.configure(bg="#FFFFFF")
        self.connection = Util.ConnectMysql()
        self.create_widgets()

    def create_widgets(self):
        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=531,
            width=747,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.IDEntry = tk.Entry(self, bd=0, bg="#CCCCCC", fg="#000716", highlightthickness=0)
        self.IDEntry.place(x=128.0, y=218.0, width=520, height=34)

        self.PasswordEntry = tk.Entry(self, bd=0, bg="#CCCCCC", fg="#000716", highlightthickness=0, show='*')
        self.PasswordEntry.place(x=128.0, y=279.0, width=520, height=34)

        self.canvas.create_text(110.0, 233.0, text="ID", font=("Arial-BoldMT", int(13.0)), anchor="w")
        self.canvas.create_text(98.0, 294.0, text="PW", font=("Arial-BoldMT", int(13.0)), anchor="w")
        self.canvas.create_text(126.0, 72.0, anchor="nw", text="TOEIC 영단어 학습 프로그램", fill="#000000", font=("Inter", 40 * -1))

        self.SignUpBtn = tk.Button(self, text="회원가입", command=lambda: Util.SwitchPage(self, "SignUpPage"))
        self.SignUpBtn.place(x=374, y=350, width=133, height=33)
        
        self.LoginBtn = tk.Button(self, text="로그인", command=self.login)
        self.LoginBtn.place(x=530, y=350, width=133, height=33)
        
        self.resizable(False, False)
        

    def login(self):
        if self.connection:  # 연결 확인
            id = self.IDEntry.get()
            password = self.PasswordEntry.get()

            if self.connection.is_connected():
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM admin WHERE id=%s AND password=%s", (id, password))
                IsAdmin = cursor.fetchone()

                if IsAdmin:
                    messagebox.showinfo("로그인 성공", "관리자로 로그인 성공!")
                    Util.SwitchPage(self, "AdminMainPage", id)
                else:
                    cursor.execute("SELECT * FROM user WHERE id=%s AND password=%s", (id, password))
                    IsUser = cursor.fetchone()
                    if IsUser:
                        messagebox.showinfo("로그인 성공", "사용자로 로그인 성공!")
                        Util.SwitchPage(self, "UserMainPage", id)
                    else:
                        messagebox.showinfo("로그인 실패", "로그인 실패. 사용자 이름 또는 비밀번호를 확인하세요.")

if __name__ == "__main__":
    app = LoginPage()
    app.mainloop()
