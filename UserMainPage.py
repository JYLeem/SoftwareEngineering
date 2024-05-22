import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
from PIL import Image, ImageTk
import sys
import os

class UserMainPage(tk.Tk):
    def __init__(self, userID):
        super().__init__()

        self.title("유저 메인 페이지")
        self.geometry("800x600")
        self.userID = userID
        self.configure(bg="#023F94")  # 남색 배경
        self.resizable(False, False)
        
        # 전역 폰트 설정
        self.set_global_font()

        # 배경 이미지 로드
        self.background_image = Image.open("수뭉이배경.jpg")
        self.background_image = self.background_image.resize((800, 500), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.background_image)

        # 배경 이미지 라벨 생성
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(x=-2, y=50, anchor="nw")

        # 사용자 사진 로드
        self.user_image = Image.open("사용자사진.png")
        self.user_photo = ImageTk.PhotoImage(self.user_image)
        self.user_image_label = tk.Label(self, image=self.user_photo, bg="#023F94")
        self.user_image_label.place(x=500, y=6)

        # 닉네임 표시
        self.nickname = self.get_user_nickname()
        self.nickname_font = tkFont.Font(family="메이플스토리", size=14)
        self.nickname_label = tk.Label(self, text=self.nickname, bg="#023F94", fg="#FFFFFF", font=self.nickname_font)
        self.nickname_label.place(x=550, y=12)

        # ttk 스타일 설정
        style = ttk.Style()
        style.configure("TButton", background="#FFFFFF", foreground="#000000", font=("메이플스토리", 10), padding=10)
        style.configure("Logout.TButton", background="#000080", foreground="#000000", font=("메이플스토리", 8), padding=5)
        style.map("TButton", background=[("active", "#f0f0f0")], foreground=[("active", "#000000")])
        style.map("Logout.TButton", background=[("active", "#000080")], foreground=[("active", "#FFFFFF")])

        # Progress bars
        self.progress1 = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress1.place(x=280, y=174)

        self.progress2 = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress2.place(x=280, y=224)

        # Labels
        self.label_font = tkFont.Font(family="메이플스토리", size=14)
        self.label1 = tk.Label(self, text="일별 학습률", bg="#FFFFFF", fg="#000000", font=self.label_font)
        self.label1.place(x=180, y=170)

        self.level = self.get_user_level()  # Level 값 가져오기
        self.label2 = tk.Label(self, text=f"Level {self.level // 100}", bg="#FFFFFF", fg="#000000", font=self.label_font)
        self.label2.place(x=200, y=220)

        # Buttons
        self.button1 = ttk.Button(self, text="일자별 학습", width=12, style="TButton", command=self.SwitchToDayStudy)
        self.button1.place(x=160, y=300)

        self.button2 = ttk.Button(self, text="일자별 시험", width=12, style="TButton", command=self.SwitchToDayExam)
        self.button2.place(x=340, y=300)

        self.button3 = ttk.Button(self, text="수뭉이 게임", width=12, style="TButton", command=self.SwitchToGamePage)
        self.button3.place(x=520, y=300)

        self.button4 = ttk.Button(self, text="수준별 학습", width=12, style="TButton", command=self.SwitchToLevelStudy)
        self.button4.place(x=160, y=400)

        self.button5 = ttk.Button(self, text="수준별 시험", width=12, style="TButton", command=self.SwitchToLevelExam)
        self.button5.place(x=340, y=400)

        # Logout Button with transparent background
        self.logout_button = ttk.Button(self, text="로그아웃", width=7, style="Logout.TButton", command=self.SwitchToLoginPage)
        self.logout_button.place(x=725, y=10)

        # Update progress bars with data from the database
        self.update_progress1_bars()
        self.update_progress2_bars()

    def set_global_font(self):
        # Maplestory Light 폰트 설정
        font_path = "Maplestory Light.ttf"
        
        if "메이플스토리" not in tkFont.families():
            print("Font '메이플스토리' not found. Attempting to load from local file.")
            if os.path.exists(font_path):
                # Load the font using tkFont
                maplestory_font = tkFont.Font(family="메이플스토리", size=12)
                
                # Register the font
                self.option_add("*TButton.Font", maplestory_font)
                self.option_add("*Font", maplestory_font)
            else:
                print(f"Font file '{font_path}' not found.")
        else:
            maplestory_font = tkFont.Font(family="메이플스토리", size=12)
            # Register the font
            self.option_add("*TButton.Font", maplestory_font)
            self.option_add("*Font", maplestory_font)

    def get_user_nickname(self):
        # 데이터베이스 연결
        conn = mysql.connector.connect(
            host='ystdb.cl260eouqhjz.ap-northeast-2.rds.amazonaws.com',
            user='admin',
            password='seat0323',
            database='wordbook'
        )
        cursor = conn.cursor()

        # 쿼리 실행
        cursor.execute("SELECT nickname FROM user WHERE id = %s", (self.userID,))
        nickname = cursor.fetchone()[0]

        # 연결 종료
        conn.close()

        return nickname
    
    def get_user_level(self):
        # 데이터베이스 연결
        conn = mysql.connector.connect(
            host='ystdb.cl260eouqhjz.ap-northeast-2.rds.amazonaws.com',
            user='admin',
            password='seat0323',
            database='wordbook'
        )
        cursor = conn.cursor()

        # 쿼리 실행
        cursor.execute("SELECT level FROM user WHERE id = %s", (self.userID,))
        level = cursor.fetchone()[0]

        # 연결 종료
        conn.close()

        return level

    def get_progress1_data(self):
        # 데이터베이스 연결
        conn = mysql.connector.connect(
            host='ystdb.cl260eouqhjz.ap-northeast-2.rds.amazonaws.com',
            user='admin',
            password='seat0323',
            database='wordbook'
        )
        cursor = conn.cursor()

        # 쿼리 실행
        cursor.execute("SELECT wordday FROM user WHERE id = %s", (self.userID,))
        wordday = cursor.fetchone()[0]

        cursor.execute("SELECT MAX(Day) FROM toeicword")
        total_day = cursor.fetchone()[0]

        # 연결 종료
        conn.close()

        # 진행도 계산
        progress1_value = (wordday / total_day) * 100
        return progress1_value

    def get_progress2_data(self):
        # 데이터베이스 연결
        conn = mysql.connector.connect(
            host='ystdb.cl260eouqhjz.ap-northeast-2.rds.amazonaws.com',
            user='admin',
            password='seat0323',
            database='wordbook'
        )
        cursor = conn.cursor()

        # 쿼리 실행
        cursor.execute("SELECT level FROM user WHERE id = %s", (self.userID,))
        level = cursor.fetchone()[0]

        # 연결 종료
        conn.close()

        # 진행도 계산
        progress2_value = (level % 100)
        return progress2_value

    def update_progress1_bars(self):
        progress1_value = self.get_progress1_data()
        self.progress1['value'] = progress1_value

    def update_progress2_bars(self):
        progress2_value = self.get_progress2_data()
        self.progress2['value'] = progress2_value

    def SwitchToDayStudy(self):
        from userstudy import DayStudy
        self.destroy()
        app = DayStudy(self.userID)
        app.mainloop()
        
    def SwitchToDayExam(self):
        from UserExamDayPage import DayExam
        self.destroy()
        app = DayExam(self.userID)
        app.mainloop()
        
    def SwitchToLevelExam(self):
        from UserExamLevelPage import LevelExam
        self.destroy()
        app = LevelExam(self.userID)
        app.mainloop()
        
    def SwitchToLevelStudy(self):
        from UserStudyLevelPage import LevelStudy
        self.destroy()
        app = LevelStudy(self.userID)
        app.mainloop()
    
    def SwitchToGamePage(self):
        from game import GameApp
        self.destroy()
        app = GameApp(self.userID)
        app.mainloop()
            
    def SwitchToLoginPage(self):
        from LoginPage import LoginPage
        self.destroy()
        app = LoginPage()
        app.mainloop()

if __name__ == "__main__":
    userID = sys.argv[1] if len(sys.argv) > 1 else 'default_user'
    app = UserMainPage(userID)
    app.mainloop()

