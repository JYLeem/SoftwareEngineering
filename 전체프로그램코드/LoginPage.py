from PIL import Image, ImageTk  # PIL 라이브러리 추가
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from Util import Util
import datetime
from tkinter import font as tkFont  # 폰트 모듈 추가
import os
import sys
import tempfile
import shutil
import ctypes

class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("로그인")
        self.geometry("900x600")
        self.configure(bg="#FFFFFF")
        self.connection = Util.ConnectMysql()

        # 실행 파일 경로 설정
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(__file__)

        # 폰트 파일 경로 설정
        bold_font_path = os.path.join(application_path, 'Maplestory Bold.ttf')
        light_font_path = os.path.join(application_path, 'Maplestory Light.ttf')

        # 폰트 설치
        self.install_font(bold_font_path)
        self.install_font(light_font_path)

        # 폰트 등록
        self.maple_font = tkFont.Font(family="Maplestory", size=14, weight="bold")

        self.create_widgets(application_path)
        self.resizable(False, False)

    def install_font(self, font_path):
        if os.path.exists(font_path):
            # 시스템에 폰트를 설치
            FR_PRIVATE = 0x10
            FR_NOT_ENUM = 0x20
            ctypes.windll.gdi32.AddFontResourceExW(ctypes.c_wchar_p(font_path), FR_PRIVATE, 0)
            # 폰트 캐시 갱신
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x001D, 0, 0)

    def create_widgets(self, application_path):
        # 배경 이미지 로드
        self.background_image = Image.open(os.path.join(application_path, "로그인수뭉이.png"))
        self.background_image = self.background_image.resize((900, 600), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.background_image)

        # 배경 이미지 캔버스에 배치
        self.canvas = tk.Canvas(
            self,
            bg="#FFFFFF",
            height=600,
            width=900,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        self.canvas.create_image(450, 300, image=self.bg_image, anchor="center")

        # 로고 이미지 로드 및 배치
        self.logo_image = Image.open(os.path.join(application_path, "로고.png"))
        self.logo_image = self.logo_image.resize((300, 180), Image.Resampling.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        self.canvas.create_image(490, 190, image=self.logo_photo, anchor="center")

        # 위젯 생성
        self.IDEntry = ttk.Entry(self, style="TEntry")
        self.IDEntry.place(x=340.0, y=280.0, width=300, height=34)

        self.PasswordEntry = ttk.Entry(self, style="TEntry", show='*')
        self.PasswordEntry.place(x=340.0, y=335.0, width=300, height=34)

        # 더 굵고 진한 텍스트 설정
        self.canvas.create_text(305.0, 297.0, text="ID", font=self.maple_font, fill="#000000", anchor="w")
        self.canvas.create_text(300.0, 352.0, text="PW", font=self.maple_font, fill="#000000", anchor="w")

        # 로그인 버튼 이미지 로드 및 설정
        self.login_normal_image = Image.open(os.path.join(application_path, "로그인일반.png"))
        self.login_hover_image = Image.open(os.path.join(application_path, "로그인호버.png"))
        self.login_normal_photo = ImageTk.PhotoImage(self.login_normal_image)
        self.login_hover_photo = ImageTk.PhotoImage(self.login_hover_image)

        self.LoginBtn = tk.Button(self, image=self.login_normal_photo, command=self.login, borderwidth=0, bg="#FFFFFF", activebackground="#FFFFFF")
        self.LoginBtn.place(x=510, y=390)
        self.LoginBtn.bind("<Enter>", self.on_login_enter)
        self.LoginBtn.bind("<Leave>", self.on_login_leave)

        # 회원가입 버튼 이미지 로드 및 설정
        self.signup_normal_image = Image.open(os.path.join(application_path, "회원가입일반.png"))
        self.signup_hover_image = Image.open(os.path.join(application_path, "회원가입호버.png"))
        self.signup_normal_photo = ImageTk.PhotoImage(self.signup_normal_image)
        self.signup_hover_photo = ImageTk.PhotoImage(self.signup_hover_image)

        self.SignUpBtn = tk.Button(self, image=self.signup_normal_photo, command=self.SwitchToSignUpPage, borderwidth=0, bg="#FFFFFF", activebackground="#FFFFFF")
        self.SignUpBtn.place(x=370, y=390)
        self.SignUpBtn.bind("<Enter>", self.on_signup_enter)
        self.SignUpBtn.bind("<Leave>", self.on_signup_leave)

        self.resizable(False, False)

    def on_login_enter(self, event):
        self.LoginBtn.config(image=self.login_hover_photo)

    def on_login_leave(self, event):
        self.LoginBtn.config(image=self.login_normal_photo)

    def on_signup_enter(self, event):
        self.SignUpBtn.config(image=self.signup_hover_photo)

    def on_signup_leave(self, event):
        self.SignUpBtn.config(image=self.signup_normal_photo)

    def login(self):
        if self.connection:  # 연결 확인
            id = self.IDEntry.get()
            password = self.PasswordEntry.get()

            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                self.cursor.execute("SELECT * FROM admin WHERE id=%s AND password=%s", (id, password))
                IsAdmin = self.cursor.fetchone()

                if IsAdmin:
                    from AdminMainPage import AdminMainPage
                    self.destroy()
                    app = AdminMainPage(id)
                    app.mainloop()
                else:
                    self.cursor.execute("SELECT * FROM user WHERE id=%s AND password=%s", (id, password))
                    IsUser = self.cursor.fetchone()
                    if IsUser:
                        self.update_last_login(id)
                        from UserMainPage import UserMainPage
                        self.cursor.execute("UPDATE user SET isaccess = 1 WHERE id = %s",(id,))
                        self.connection.commit()  # 커밋을 수행하여 변경 사항을 DB에 적용
                        self.cursor.close()  # 커서 닫기
                        self.destroy()  # 로그인 창 닫기
                        app = UserMainPage(id)  # 시험 앱 초기화 및 실행
                        app.mainloop()
                    else:
                        messagebox.showinfo("로그인 실패", "로그인 실패. 사용자 이름 또는 비밀번호를 확인하세요.")

    def update_last_login(self, user_id):
        today = datetime.date.today()
        self.cursor.execute("UPDATE user SET last_login = %s WHERE id = %s", (today, user_id))
        self.connection.commit()

    def SwitchToSignUpPage(self):
        from SignUpPage import SignUpPage
        self.destroy()
        app = SignUpPage()
        app.mainloop()

if __name__ == "__main__":
    app = LoginPage()
    app.mainloop()
