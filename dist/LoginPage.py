from PIL import Image, ImageTk  # PIL 라이브러리 추가
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from Util import Util
# from UserExamDayPage import ExamApp

class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("로그인")
        self.geometry("900x600")
        self.configure(bg="#FFFFFF")
        self.connection = Util.ConnectMysql()
        
        # 스타일 설정
        self.style = ttk.Style(self)
        self.style.configure("TEntry", foreground="#000716", background="#CCCCCC")
        self.style.configure("TButton", foreground="#000716", background="white", font=("Arial", 10))
        
        self.create_widgets()
        self.resizable(False, False)
    
    def create_widgets(self):
        # 배경 이미지 로드
        self.background_image = Image.open("로그인수뭉이.png")
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

        # 위젯 생성
        self.IDEntry = ttk.Entry(self, style="TEntry")
        self.IDEntry.place(x=320.0, y=248.0, width=300, height=34)

        self.PasswordEntry = ttk.Entry(self, style="TEntry", show='*')
        self.PasswordEntry.place(x=320.0, y=309.0, width=300, height=34)

        # 더 굵고 진한 텍스트 설정
        self.canvas.create_text(270.0, 263.0, text="ID", font=("Arial Bold", 14), fill="#000000", anchor="w")
        self.canvas.create_text(270.0, 324.0, text="PW", font=("Arial Bold", 14), fill="#000000", anchor="w")
        self.canvas.create_text(250.0, 180.0, anchor="nw", text="TOEIC 영단어 학습 프로그램", fill="#000000", font=("Inter", 30 * -1))

        self.SignUpBtn = ttk.Button(self, text="회원가입", style="TButton", command=self.SwitchToSignUpPage)
        self.SignUpBtn.place(x=320, y=380, width=133, height=33)
        
        self.LoginBtn = ttk.Button(self, text="로그인", style="TButton", command=self.login)
        self.LoginBtn.place(x=476, y=380, width=133, height=33)
        
        self.resizable(False, False)
    
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
                        from UserMainPage import UserMainPage
                        self.cursor.execute("UPDATE user SET isaccess = 1 WHERE id = %s",(id,))
                        self.connection.commit()  # 커밋을 수행하여 변경 사항을 DB에 적용
                        self.cursor.close()  # 커서 닫기 
                        self.destroy()  # 로그인 창 닫기
                        app = UserMainPage(id)  # 시험 앱 초기화 및 실행
                        app.mainloop()
                    else:
                        messagebox.showinfo("로그인 실패", "로그인 실패. 사용자 이름 또는 비밀번호를 확인하세요.")

    def SwitchToSignUpPage(self):
        from SignUpPage import SignUpPage
        self.destroy()
        app = SignUpPage()
        app.mainloop()

if __name__ == "__main__":
    app = LoginPage()
    app.mainloop()
