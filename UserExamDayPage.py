import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import random
import sys
from Util import Util
# import ttkbootstrap as ttk
#from ttkbootstrap.constants import *
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
        self.current_index = 0  # 현재 단어 인덱스
        self.correct_count = 0  # 맞은 단어 수
        self.total_questions = 20  # 총 문제 수
        self.timer_id = None  # 타이머 이벤트 ID 저장
        self.time_left = 600  # 10분을 초 단위로 환산
    
    def connect_database(self):
        #db연결 함수
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
        #기본 요소 생성함수
        
        # 이전 버튼 추가, 좌표 지정
        self.back_button = tk.Button(self, text="이전으로", command=lambda: Util.SwitchPage(self, "UserMainPage", self.user), width=6, height=1, font=("Helvetica", 8))
        self.back_button.place(x=25, y=10)  # 좌표 (10, 10) 위치에 버튼 배치
        
        self.buttons_frame = tk.Frame(self, bg="#FFFFFF")
        self.buttons_frame.place(x=25, y=90)

        self.day_label = tk.Label(self, text="먼저 날짜를 선택하세요", font=("Helvetica", 16), bg="#FFFFFF")
        self.day_label.place(x=70, y=45)
        
        self.exam_label = tk.Label(self, text="", font=("Helvetica", 16), bg="#FFFFFF")
        self.exam_label.place(x=430, y=200)
        
        self.answer_entry = tk.Entry(self, font=("Helvetica", 16))
        self.answer_entry.place(x=430, y=250)
        self.answer_entry.bind("<Return>", self.check_answer)

        self.start_button = ttk.Button(self, text="시험 시작", style='TButton', command=self.start_test)
        self.start_button.place(x=520, y=310)

        self.bar_label = tk.Label(self, text="진행도", font=("Helvetica", 8), bg="#FFFFFF")
        self.bar_label.place(x=150, y=290)
        
        self.time_label = tk.Label(self, text="", font=("Helvetica", 12), bg="#FFFFFF")
        self.time_label.place(x=430, y=150)
        
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=300, mode='determinate', maximum=100)
        self.progress_bar.place(x=25, y=310)
        self.progress_bar['value'] = 0
        
        self.load_image("시험진행도.png")  # 이미지 경로 지정

        self.load_day_buttons()
        
    def load_day_buttons(self):
        # 일자선택 버튼 생성
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
        self.canvas = tk.Canvas(self, width=300, height=200,bg='white', borderwidth=0, highlightthickness=0)
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
        #일자 선택에 따라 보여지는 텍스트 조정
        self.current_day = day
        self.day_label.config(text=f"{day+1}일차 시험 준비")
        
        
    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.time_label.config(text=f"남은 시간: {self.time_left // 60}분 {self.time_left % 60}초")
            self.timer_id = self.after(1000, self.update_timer)
        else:
            self.finish_test()
            
    

    def start_test(self):
        if not hasattr(self, 'current_day'):
            messagebox.showinfo("Select Day", "Please select a day first!")
            return
        #시험 시작버튼 누르면
        self.time_left = 600  # 10분
        self.update_timer()  # 타이머 시작
        self.time_label.config(text=f"남은 시간: {self.time_left // 60}분 {self.time_left % 60}초")
        self.time_label.place(x=430, y=150)  # 시간 레이블 보이기
        
        self.progress_bar['value'] = 0  # 프로그레스바 리셋
        self.start_button.place_forget()  # 시험 시작 버튼 숨기기
        self.load_test_words()
        self.next_word()



    def load_test_words(self):
        # toeicword 20개 가져옴, 동시에 게임 변수 index와 count 초기화
        cursor = self.connection.cursor()
        cursor.execute("SELECT Spell, Mean FROM toeicword WHERE Day = %s ORDER BY RAND() LIMIT 20", (self.current_day,))
        words = cursor.fetchall()
        cursor.close()
        self.test_words = words
        self.current_index = 0
        self.correct_count = 0
        self.update_progress()  # 초기 진행 상황 업데이트

    
    def next_word(self):
        #다음단어 가져옴, 다풀면 종료
        if self.current_index < len(self.test_words):
            current_word = self.test_words[self.current_index]
            self.exam_label.config(text=current_word[1])
            self.answer_entry.delete(0, tk.END)
        else:
            self.finish_test()

    def check_answer(self, event=None):
        #정답 맞는지 확인해서 맞으면 correct count증가, 그리고 정답여부와 관곙벗이 index 1증가
        if self.current_index < len(self.test_words):
            if self.answer_entry.get().strip().lower() == self.test_words[self.current_index][0].lower():
                self.correct_count += 1
            self.current_index += 1
            self.update_progress()  # 답을 확인할 때마다 진행 상황 업데이트
            self.next_word()
    
    def update_progress(self):
        progress = (self.current_index / self.total_questions) * 100
        self.progress_bar['value'] = progress

    def finish_test(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)  # 타이머 이벤트 취소
        self.time_label.place_forget()  # 시간 레이블 숨기기
        self.start_button.place(x=520, y=310)  # 시험 시작 버튼 다시 보이기

        messagebox.showinfo("시험 종료", f"점수 : {self.correct_count}/{len(self.test_words)}")
        self.day_label.config(text=f"{self.current_day}일차 시험 준비")
        self.exam_label.config(text="")
        self.answer_entry.delete(0, tk.END)

if __name__ == "__main__":
    user_id = sys.argv[1] if len(sys.argv) > 1 else 'default_user'
    app = DayExam(user_id)
    app.mainloop()
