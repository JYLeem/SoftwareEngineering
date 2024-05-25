import importlib
from mysql.connector import Error
from tkinter import Canvas
from tkinter import messagebox
import tkinter as tk
from Util import Util
from PIL import Image, ImageTk
from tkinter import font as tkFont  # 폰트 모듈 추가
import datetime  # datetime 모듈 추가

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

        # 메이플스토리 폰트 로드
        self.maple_font = tkFont.Font(family="Maplestory", size=13, weight="bold")
        self.maple_font_large = tkFont.Font(family="Maplestory", size=40, weight="bold")

        self.load_additional_images()

        self.NicknameEntry = self.create_image_entry(122.0, 177.0, 522, 34)
        self.CheckNicknameExistenceBtn = self.create_image_button(
            "중복확인일반.png", "중복확인호버.png", self.CheckNicknameExistence
        )
        self.CheckNicknameExistenceBtn.place(x=650.0, y=177.0)

        self.IDEntry = self.create_image_entry(122.0, 240.0, 522, 34)
        self.CheckIDExistenceBtn = self.create_image_button(
            "중복확인일반.png", "중복확인호버.png", self.CheckIDExistence
        )
        self.CheckIDExistenceBtn.place(x=650.0, y=240.0)

        self.PasswordEntry = self.create_image_entry(122.0, 303.0, 522, 34, show='*')

        self.canvas.create_text(
            67.0, 194.0,
            text="닉네임",
            font=self.maple_font, anchor="w"
        )

        self.canvas.create_text(
            87.0, 257.0,
            text="ID",
            font=self.maple_font, anchor="w"
        )

        self.canvas.create_text(
            82.0, 320,
            text="PW",
            font=self.maple_font, anchor="w"
        )
        self.canvas.create_text(
            280.0,
            65.0,
            anchor="nw",
            text="회원가입",
            fill="#000000",
            font=self.maple_font_large
        )

        self.GoPrevPageBtn = self.create_image_button(
            "이전으로버튼일반.png", "이전으로버튼호버.png", self.SwitchToLoginPage
        )
        self.GoPrevPageBtn.place(x=356, y=367)

        self.SignUpBtn = self.create_image_button(
            "회원가입버튼일반.png", "회원가입버튼호버.png", self.SignUp
        )
        self.SignUpBtn.place(x=511, y=367)
        self.SignUpBtn.config(state="disabled")

        self.NicknameEntry.tkraise()
        self.IDEntry.tkraise()
        self.PasswordEntry.tkraise()
        self.GoPrevPageBtn.tkraise()
        self.SignUpBtn.tkraise()
        self.CheckIDExistenceBtn.tkraise()
        self.CheckNicknameExistenceBtn.tkraise()
        self.resizable(False, False)

    def create_image_entry(self, x, y, width, height, show=None):
        entry_canvas = tk.Canvas(self, width=width, height=height, bg="#FFFFFF", bd=0, highlightthickness=0)
        entry_canvas.place(x=x, y=y)

        entry_image = Image.open("입력필드.png")
        entry_image = entry_image.resize((int(width), int(height)), Image.Resampling.LANCZOS)
        entry_photo = ImageTk.PhotoImage(entry_image)

        entry_canvas.create_image(0, 0, image=entry_photo, anchor="nw")
        entry_canvas.image = entry_photo  # Keep a reference to avoid garbage collection

        entry = tk.Entry(entry_canvas, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, show=show, font=self.maple_font)
        entry_window = entry_canvas.create_window(10, 10, anchor="nw", window=entry, width=width-20, height=height-20)

        return entry

    def create_image_button(self, normal_image_path, hover_image_path, command):
        normal_image = Image.open(normal_image_path)
        hover_image = Image.open(hover_image_path)
        normal_photo = ImageTk.PhotoImage(normal_image)
        hover_photo = ImageTk.PhotoImage(hover_image)
        button = tk.Button(self, image=normal_photo, bg="#FFFFFF", borderwidth=0, highlightthickness=0, activebackground="#FFFFFF", command=command)
        button.bind("<Enter>", lambda e: button.config(image=hover_photo))
        button.bind("<Leave>", lambda e: button.config(image=normal_photo))
        button.image = normal_photo  # Keep a reference to the image to avoid garbage collection
        button.hover_image = hover_photo  # Keep a reference to the hover image
        return button

    def load_additional_images(self):
        left_image = Image.open("회원가입좌.png").resize((66, 102), Image.Resampling.LANCZOS)
        right_image = Image.open("회원가입우.png").resize((66, 93), Image.Resampling.LANCZOS)

        left_photo = ImageTk.PhotoImage(left_image)
        right_photo = ImageTk.PhotoImage(right_image)

        self.left_image_label = tk.Label(self, image=left_photo, bg="#FFFFFF")
        self.left_image_label.image = left_photo
        self.left_image_label.place(x=208, y=30)

        self.right_image_label = tk.Label(self, image=right_photo, bg="#FFFFFF")
        self.right_image_label.image = right_photo
        self.right_image_label.place(x=469, y=31)

    def CheckNicknameExistence(self):
        if self.connection:
            nickname = self.NicknameEntry.get()
            if len(nickname) == 0:
                messagebox.showinfo("닉네임 미기입", "닉네임이 입력되지 않았습니다.")
                return
            cursor = self.connection.cursor()
            cursor.execute("SELECT nickname FROM user WHERE id=%s", (nickname,))
            NicknameExistence = cursor.fetchall()
            if NicknameExistence:
                messagebox.showinfo("닉네임 중복", "이미 존재하는 닉네임이 있습니다.")
            else:
                messagebox.showinfo("닉네임 생성 가능", "사용 가능한 닉네임 입니다.")
                if self.ExistenceValues[0] == 0:
                    self.ExistenceValues[0] += 1
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
                messagebox.showinfo("아이디 생성 가능", "사용 가능한 아이디 입니다.")
                if self.ExistenceValues[1] == 0:
                    self.ExistenceValues[1] += 1
                if sum(self.ExistenceValues) == 2:
                    self.SignUpBtn.config(state="active")

    def SignUp(self):
        if self.connection:
            nickname = self.NicknameEntry.get()
            id = self.IDEntry.get()
            password = self.PasswordEntry.get()
            if len(password) == 0:
                messagebox.showinfo("비밀번호 미기입", "비밀번호를 입력해 주세요.")
                return
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO user (nickname, id, password) VALUES (%s, %s, %s)", (nickname, id, password,))
            self.connection.commit()  # 커밋을 수행하여 변경 사항을 DB에 적용

            # 현재 날짜를 gendate로 업데이트
            today = datetime.date.today()
            cursor.execute("UPDATE user SET gendate = %s WHERE id = %s", (today, id))
            self.connection.commit()

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
