import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sys

class UserMainPage(tk.Tk):
    def __init__(self, userID):
        super().__init__()

        self.title("유저 메인 페이지")
        self.geometry("800x600")
        self.userID = userID
        self.configure(bg="#000080")  # 남색 배경
        self.resizable(False, False)
        
        # 배경 이미지 로드
        self.background_image = Image.open("수뭉이배경.jpg")
        self.background_image = self.background_image.resize((800, 500), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.background_image)

        # 배경 이미지 라벨 생성
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(x=-2, y=50, anchor="nw")

        # ttk 스타일 설정
        style = ttk.Style()
        style.configure("TLabel", background="#FFFFFF", foreground="#000000", font=("Arial", 14))
        style.configure("TButton", background="#FFFFFF", foreground="#000000", font=("Arial", 10), padding=10)
        style.map("TButton", background=[("active", "#f0f0f0")], foreground=[("active", "#000000")])

        # Custom style for logout button
        style.configure("Logout.TButton", background="#000080", foreground="#000000", font=("Arial", 8), padding=5)
        style.map("Logout.TButton", background=[("active", "#000080")], foreground=[("active", "#FFFFFF")])

        # Progress bars
        self.progress1 = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress1.place(x=280, y=174)
        self.progress1['value'] = 70

        self.progress2 = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress2.place(x=280, y=224)
        self.progress2['value'] = 50

        # Labels
        self.label1 = ttk.Label(self, text="진행도", style="TLabel")
        self.label1.place(x=210, y=170)

        self.label2 = ttk.Label(self, text="Level", style="TLabel")
        self.label2.place(x=210, y=220)

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
        self.logout_button.place(x=725, y=560)

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