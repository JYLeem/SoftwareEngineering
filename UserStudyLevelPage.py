import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import sys
from Util import Util
from PIL import Image, ImageTk

class LearningApp(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.geometry("800x600")
        self.title("수준별 학습")
        self.configure(bg="#FFFFFF")
        self.connection = self.connect_database()
        self.create_widgets()
    
    def connect_database(self):
        # db연결 함수
        try:
            connection = mysql.connector.connect(
                host="ystdb.cl260eouqhjz.ap-northeast-2.rds.amazonaws.com",
                user="admin",
                password="seat0323",
                database="wordbook"
            )
            return connection
        except mysql.connector.Error as err:
            messagebox.showerror("Database Connection Error", f"An error occurred: {err}")
            self.destroy()
    
    def create_widgets(self):
        # 기본 요소 생성함수
        
        # 이전 버튼 추가, 좌표 지정
        self.back_button = tk.Button(self, text="이전으로", command=lambda: Util.SwitchPage(self, "UserMainPage", self.user), width=6, height=1, font=("Helvetica", 8))
        self.back_button.place(x=25, y=10)  # 좌표 (10, 10) 위치에 버튼 배치

        # 난이도 선택 레이블 및 드롭다운 메뉴 추가
        self.level_label = tk.Label(self, text="난이도를 선택하세요", font=("Helvetica", 20), bg="#FFFFFF")
        self.level_label.place(x=45, y=100)

        self.level_var = tk.StringVar(value="하")
        self.level_dropdown = ttk.Combobox(self, textvariable=self.level_var, values=["하", "중", "상"], state="readonly", font=("Helvetica", 12))
        self.level_dropdown.place(x=70, y=140)
        self.level_dropdown.bind("<<ComboboxSelected>>", self.load_words)
        
        self.bar_label = tk.Label(self, text="레벨", font=("Helvetica", 12), bg="#FFFFFF")
        self.bar_label.place(x=150, y=215)
        
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=300, mode='determinate', maximum=100)
        self.progress_bar.place(x=25, y=240)
        self.progress_bar['value'] = 0

        self.word_frame = tk.Frame(self, bg="#FFFFFF", highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.word_frame.place(x=350, y=35, width=425, height=515)

        self.canvas = tk.Canvas(self.word_frame, bg="#FFFFFF")
        self.scrollbar = ttk.Scrollbar(self.word_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFFFFF")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.load_image("시험진행도.png")  # 이미지 경로 지정
    
    def load_image(self, image_path):
        # 캔버스 설정
        self.canvas_img = tk.Canvas(self, width=300, height=200, bg='white', borderwidth=0, highlightthickness=0)
        self.canvas_img.place(x=25, y=275)  # 이미지 위치 지정

        # 이미지 파일 열기
        image = Image.open(image_path)
            
        # 캔버스 크기에 맞게 이미지 크기 조정
        resized_image = image.resize((300, 200), Image.Resampling.LANCZOS)  # 이미지를 300x200 크기로 조정
        photo = ImageTk.PhotoImage(resized_image)

        # 캔버스에 이미지 배치, 위치는 캔버스 중앙
        self.canvas_img.create_image(150, 100, image=photo)
            
        # 이미지 객체 참조를 유지해야 이미지가 화면에 나타남
        self.canvas_img.image = photo           
        
    def load_words(self, event=None):
        # 난이도에 따라 toeicword에서 모든 단어 가져옴
        selected_difficulty = self.level_var.get()

        cursor = self.connection.cursor()
        cursor.execute("SELECT Spell, Mean FROM toeicword WHERE Difficulty = %s ORDER BY Spell", (selected_difficulty,))
        words = cursor.fetchall()
        cursor.close()

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if words:
            for spell, mean in words:
                word_label = ttk.Label(self.scrollable_frame, text=f"{spell} / {mean}", font=("Helvetica", 12), background="#FFFFFF")
                word_label.pack(anchor="w", pady=2)
        else:
            messagebox.showinfo("단어 없음", "선택한 난이도에 해당하는 단어가 없습니다.")

if __name__ == "__main__":
    user_id = sys.argv[1] if len(sys.argv) > 1 else 'default_user'
    app = LearningApp(user_id)
    app.mainloop()
