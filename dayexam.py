import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import random
import sys
from Util import Util
from PIL import Image, ImageTk  # PIL 라이브러리 추가

class DayExam(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.geometry("800x600")
        self.title("일자별 시험")
        self.configure(bg="#FFFFFF")
        self.connection = self.connect_database()
        self.create_widgets()
        self.test_words = []  # 시험을 위한 단어 목록
        self.entry_vars = []  # 입력 필드 변수 목록
        self.correct_count = 0  # 맞은 단어 수
        self.total_questions = 20  # 총 문제 수
        self.current_day = None  # 현재 선택된 날짜
    
    def connect_database(self):
        # DB 연결 함수
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
        # 기본 요소 생성 함수
        
        # 이전 버튼 추가, 좌표 지정
        self.back_button = tk.Button(self, text="이전으로", command=lambda: Util.SwitchPage(self, "UserMainPage", self.user), width=6, height=1, font=("Helvetica", 8))
        self.back_button.place(x=25, y=10)  # 좌표 (10, 10) 위치에 버튼 배치
        
        self.buttons_frame = tk.Frame(self, bg="#FFFFFF")
        self.buttons_frame.place(x=25, y=90)

        self.day_label = tk.Label(self, text="먼저 날짜를 선택하세요", font=("Helvetica", 16), bg="#FFFFFF")
        self.day_label.place(x=70, y=45)
        
        self.exam_frame = tk.Frame(self, bg="#FFFFFF")
        self.exam_frame.place(x=25, y=150)
        
        self.start_button = ttk.Button(self, text="시험 시작", style='TButton', command=self.start_test)
        self.start_button.place(x=520, y=310)

        self.end_button = ttk.Button(self, text="시험 종료", style='TButton', command=self.finish_test)
        self.end_button.place(x=620, y=310)
        self.end_button.place_forget()  # 시험 종료 버튼 숨기기
        
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=300, mode='determinate', maximum=100)
        self.progress_bar.place(x=25, y=310)
        self.progress_bar['value'] = 0
        
        self.load_image("시험진행도.png")  # 이미지 경로 지정

        self.load_day_buttons()
        
    def load_day_buttons(self):
        # 일자 선택 버튼 생성
        cursor = self.connection.cursor()
        cursor.execute("SELECT DISTINCT Day FROM toeicword ORDER BY Day")
        days = cursor.fetchall()
        cursor.close()
        
        rows, cols = 6, 5
        day_iter = iter(days)
        for r in range(rows):
            for c in range(cols):
                try:
                    day = next(day_iter)[0]
                    btn = tk.Button(self.buttons_frame, text=f"{day+1}", command=lambda d=day: self.select_day(d), width=7, height=1)
                    btn.grid(row=r, column=c)
                except StopIteration:
                    break
    
    def load_image(self, image_path):
        # 캔버스 설정
        self.canvas = tk.Canvas(self, width=300, height=200, bg='white', borderwidth=0, highlightthickness=0)
        self.canvas.place(x=25, y=350)  # 이미지 위치 지정

        # 이미지 파일 열기
        image = Image.open(image_path)
            
        # 캔버스 크기에 맞게 이미지 크기 조정
        resized_image = image.resize((300, 200), Image.Resampling.LANCZOS)  # 이미지를 300x200 크기로 조정
        photo = ImageTk.PhotoImage(resized_image)

        # 캔버스에 이미지 배치, 위치는 캔버스 중앙
        self.canvas.create_image(150, 100, image=photo)
            
        # 이미지 객체 참조를 유지해야 이미지가 화면에 나타남
        self.canvas.image = photo           
    
    def select_day(self, day):
        # 일자 선택에 따라 보여지는 텍스트 조정
        self.current_day = day
        self.day_label.config(text=f"{day+1}일차 시험 준비")

    def start_test(self):
        if not self.current_day:
            messagebox.showinfo("Select Day", "Please select a day first!")
            return
        
        self.progress_bar['value'] = 0  # 프로그레스바 리셋
        self.start_button.place_forget()  # 시험 시작 버튼 숨기기
        self.end_button.place(x=620, y=310)  # 시험 종료 버튼 보이기
        self.load_test_words()
        self.display_test_words()

    def load_test_words(self):
        # toeicword 20개 가져옴
        cursor = self.connection.cursor()
        cursor.execute("SELECT Spell, Mean FROM toeicword WHERE Day = %s ORDER BY RAND() LIMIT 20", (self.current_day,))
        words = cursor.fetchall()
        cursor.close()
        self.test_words = words
        self.correct_count = 0
        self.entry_vars = [tk.StringVar() for _ in range(len(self.test_words))]
    
    def display_test_words(self):
        for widget in self.exam_frame.winfo_children():
            widget.destroy()
        
        for i, (spell, mean) in enumerate(self.test_words):
            tk.Label(self.exam_frame, text=mean, font=("Helvetica", 12), bg="#FFFFFF").grid(row=i, column=0, padx=5, pady=5)
            tk.Entry(self.exam_frame, textvariable=self.entry_vars[i], font=("Helvetica", 12)).grid(row=i, column=1, padx=5, pady=5)

    def finish_test(self):
        # 시험 종료 버튼을 누르면 실행되는 함수
        self.correct_count = sum(1 for i, (spell, mean) in enumerate(self.test_words) if self.entry_vars[i].get().strip().lower() == spell.lower())
        messagebox.showinfo("시험 종료", f"점수 : {self.correct_count}/{len(self.test_words)}")
        
        self.progress_bar['value'] = 0  # 프로그레스바 리셋
        self.start_button.place(x=520, y=310)  # 시험 시작 버튼 보이기
        self.end_button.place_forget()  # 시험 종료 버튼 숨기기
        self.day_label.config(text=f"{self.current_day + 1}일차 시험 준비")
        
        # 시험 관련 레이블 및 입력 필드 초기화
        for widget in self.exam_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    user_id = sys.argv[1] if len(sys.argv) > 1 else 'default_user'
    app = DayExam(user_id)
    app.mainloop()
