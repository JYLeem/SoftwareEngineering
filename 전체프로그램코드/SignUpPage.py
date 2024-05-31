import importlib
from mysql.connector import Error
from tkinter import Canvas
from tkinter import messagebox
import tkinter as tk
from Util import Util

class SignUpPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.connection = Util.ConnectMysql()
        self.ExistenceValues = [0, 0]
        self.title("회원가입")
        self.geometry("747x531")
        self.configure(bg="#FFFFFF")
        self.canvas = Canvas(
            bg="#FFFFFF",
            height=531,
            width=747,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)

        self.NicknameVar = tk.StringVar()
        self.NicknameVar.trace("w", self.on_nickname_change)
        self.NicknameEntry = tk.Entry(self, textvariable=self.NicknameVar, bd=0, bg="#CCCCCC", fg="#000716", highlightthickness=0)
        self.NicknameEntry.place(x=122.0, y=177.0, width=522, height=34)

        self.CheckNicknameExistenceBtn = tk.Button(self, text="중복 확인", command=self.CheckNicknameExistence)
        self.CheckNicknameExistenceBtn.place(x=650.0, y=177.0, width=60, height=34)

        self.IDVar = tk.StringVar()
        self.IDVar.trace("w", self.on_id_change)
        self.IDEntry = tk.Entry(self, textvariable=self.IDVar, bd=0, bg="#CCCCCC", fg="#000716", highlightthickness=0)
        self.IDEntry.place(x=122.0, y=240.0, width=522, height=34)

        self.CheckIDExistenceBtn = tk.Button(self, text="중복 확인", command=self.CheckIDExistence)
        self.CheckIDExistenceBtn.place(x=650.0, y=244.0, width=60, height=34)

        self.PasswordEntry = tk.Entry(self, bd=0, bg="#CCCCCC", fg="#000716", highlightthickness=0, show='*')
        self.PasswordEntry.place(x=122.0, y=303.0, width=520, height=34)

        self.canvas.create_text(
            70.0, 194.0,
            text="닉네임",
            font=("Arial-BoldMT", int(13.0)), anchor="w"
        )

        self.canvas.create_text(
            80.0, 257.0,
            text="ID",
            font=("Arial-BoldMT", int(13.0)), anchor="w"
        )

        self.canvas.create_text(
            80.0, 320,
            text="PW",
            font=("Arial-BoldMT", int(13.0)), anchor="w"
        )
        self.canvas.create_text(
            305.0,
            72.0,
            anchor="nw",
            text="회원가입",
            fill="#000000",
            font=("Inter", 40 * -1)
        )

        self.GoPrevPageBtn = tk.Button(self, text="이전으로", command=self.SwitchToLoginPage)
        self.GoPrevPageBtn.place(x=356, y=367, width=133, height=38)

        self.SignUpBtn = tk.Button(self, text="회원가입", command=self.SignUp)
        self.SignUpBtn.place(x=511, y=367, width=133, height=38)
        self.SignUpBtn.config(state="disabled")
        self.resizable(False, False)

    def on_nickname_change(self, *args):
        self.ExistenceValues[0] = 0
        self.SignUpBtn.config(state="disabled")

    def on_id_change(self, *args):
        self.ExistenceValues[1] = 0
        self.SignUpBtn.config(state="disabled")

    def CheckNicknameExistence(self):
        if self.connection:
            nickname = self.NicknameEntry.get()
            if len(nickname) == 0:
                messagebox.showinfo("닉네임 미기입", "닉네임이 입력되지 않았습니다.")
                return
            cursor = self.connection.cursor()
            cursor.execute("SELECT nickname FROM user WHERE nickname=%s", (nickname,))
            NicknameExistence = cursor.fetchall()
            if NicknameExistence:
                messagebox.showinfo("닉네임 중복", "이미 존재하는 닉네임이 있습니다.")
            else:
                messagebox.showinfo("닉네임 생성 가능", "사용 가능한 닉네임입니다.")
                self.ExistenceValues[0] = 1
                if sum(self.ExistenceValues) == 2:
                    self.SignUpBtn.config(state="active")

    def CheckIDExistence(self):
        if self.connection:
            id = self.IDEntry.get()
            if len(id) == 0:
                messagebox.showinfo("아이디 미기입", "아이디가 입력되지 않았습니다.")
                return
            cursor = self.connection.cursor()
            cursor.execute("SELECT id FROM user WHERE id=%s", (id,))
            IDExistence = cursor.fetchall()
            if IDExistence:
                messagebox.showinfo("아이디 중복", "이미 존재하는 아이디가 있습니다.")
            else:
                messagebox.showinfo("아이디 생성 가능", "사용 가능한 아이디입니다.")
                self.ExistenceValues[1] = 1
                if sum(self.ExistenceValues) == 2:
                    self.SignUpBtn.config(state="active")

    def SignUp(self):
        if self.connection:
            nickname = self.NicknameEntry.get()
            id = self.IDEntry.get()
            password = self.PasswordEntry.get()
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO user (nickname, id, password) VALUES (%s, %s, %s)", (nickname, id, password))
            self.connection.commit()  # 커밋을 수행하여 변경 사항을 DB에 적용
            cursor.close()  # 커서 닫기
            self.connection.close()  # 커넥션 닫기
            messagebox.showinfo("회원가입 성공", "회원가입이 완료되었습니다.")
            self.SwitchToLoginPage()

    def SwitchToLoginPage(self):
        from LoginPage import LoginPage
        self.destroy()
        app = LoginPage()
        app.mainloop()

if __name__ == "__main__":
    app = SignUpPage()
    app.mainloop()
