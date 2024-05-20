from PIL import Image, ImageTk  # PIL 라이브러리 추가
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from Util import Util
#rom UserExamDayPage import ExamApp



class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("로그인")
        self.geometry("747x531")
        self.configure(bg="#FFFFFF")
        self.connection = Util.ConnectMysql()
        
        # 스타일 설정
        self.style = ttk.Style(self)
        self.style.configure("TEntry", foreground="#000716", background="#CCCCCC")
        self.style.configure("TButton", foreground="#000716", background="white", font=("Arial", 10))
        
        self.create_widgets()
        self.resizable(False, False)  
    def create_widgets(self):
        self.canvas = tk.Canvas(
            self,
            bg="#FFFFFF",
            height=531,
            width=747,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.IDEntry = ttk.Entry(self, style="TEntry")
        self.IDEntry.place(x=128.0, y=218.0, width=520, height=34)

        self.PasswordEntry = ttk.Entry(self, style="TEntry", show='*')
        self.PasswordEntry.place(x=128.0, y=279.0, width=520, height=34)

        self.canvas.create_text(110.0, 233.0, text="ID", font=("Arial-BoldMT", int(13.0)), anchor="w")
        self.canvas.create_text(98.0, 294.0, text="PW", font=("Arial-BoldMT", int(13.0)), anchor="w")
        self.canvas.create_text(126.0, 72.0, anchor="nw", text="TOEIC 영단어 학습 프로그램", fill="#000000", font=("Inter", 30 * -1))

        self.SignUpBtn = ttk.Button(self, text="회원가입", style="TButton", command=self.SwitchToSignUpPage)
        self.SignUpBtn.place(x=374, y=350, width=133, height=33)
        
        self.LoginBtn = ttk.Button(self, text="로그인", style="TButton", command=self.login)
        self.LoginBtn.place(x=530, y=350, width=133, height=33)
        
        self.resizable(False, False)
        

    def load_image(self, image_path):
        # 캔버스 설정
        self.canvas = tk.Canvas(self, width=300, height=200,bg='white', borderwidth=0, highlightthickness=0)
        self.canvas.place(x=25, y=25)  # 이미지 위치 지정

        # 이미지 파일 열기
        image = Image.open(image_path)
            
        # 캔버스 크기에 맞게 이미지 크기 조정
        resized_image = image.resize((300, 200), Image.Resampling.LANCZOS)  # 이미지를 300x200 크기로 조정
        photo = ImageTk.PhotoImage(resized_image)

        # 캔버스에 이미지 배치, 위치는 캔버스 중앙
        self.canvas.create_image(150, 100, image=photo)
            
        # 이미지 객체 참조를 유지해야 이미지가 화면에 나타남
        self.canvas.image = photo
    
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
