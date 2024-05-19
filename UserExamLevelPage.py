import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import sys
from Util import Util
from PIL import Image, ImageTk

class ExamApp(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.geometry("800x600")
        self.title("수준별 시험")
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
        self.level_label.place(x=430, y=140)

        self.level_var = tk.StringVar(value="하")
        self.level_dropdown = ttk.Combobox(self, textvariable=self.level_var, values=["하", "중", "상"], state="readonly", font=("Helvetica", 12))
        self.level_dropdown.place(x=455, y=180)
        
        self.exam_label = tk.Label(self, text="", font=("Helvetica", 16), bg="#FFFFFF")
        self.exam_label.place(x=440, y=265)
        
        self.answer_entry = tk.Entry(self, font=("Helvetica", 16))
        self.answer_entry.place(x=440, y=300)
        self.answer_entry.bind("<Return>", self.check_answer)

        self.start_button = ttk.Button(self, text="시험 시작", style='TButton', command=self.start_test)
        self.start_button.place(x=520, y=370)

        self.bar_label = tk.Label(self, text="레벨", font=("Helvetica", 12), bg="#FFFFFF")
        self.bar_label.place(x=150, y=150)
        
        self.time_label = tk.Label(self, text="", font=("Helvetica", 12), bg="#FFFFFF")
        self.time_label.place(x=480, y=205)
        
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=300, mode='determinate', maximum=100)
        self.progress_bar.place(x=25, y=180)
        self.progress_bar['value'] = 0
        
        self.load_image("시험진행도.png")  # 이미지 경로 지정
    
    def load_image(self, image_path):
        # 캔버스 설정
        self.canvas = tk.Canvas(self, width=300, height=200, bg='white', borderwidth=0, highlightthickness=0)
        self.canvas.place(x=25, y=220)  # 이미지 위치 지정

        # 이미지 파일 열기
        image = Image.open(image_path)
            
        # 캔버스 크기에 맞게 이미지 크기 조정
        resized_image = image.resize((300, 200), Image.Resampling.LANCZOS)  # 이미지를 300x200 크기로 조정
        photo = ImageTk.PhotoImage(resized_image)

        # 캔버스에 이미지 배치, 위치는 캔버스 중앙
        self.canvas.create_image(150, 100, image=photo)
            
        # 이미지 객체 참조를 유지해야 이미지가 화면에 나타남
        self.canvas.image = photo           
        
    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.time_label.config(text=f"남은 시간: {self.time_left // 60}분 {self.time_left % 60}초")
            self.timer_id = self.after(1000, self.update_timer)
        else:
            self.finish_test()

    def start_test(self):
        # 시험 시작버튼 누르면
        self.time_left = 600  # 10분
        self.update_timer()  # 타이머 시작
        self.time_label.config(text=f"남은 시간: {self.time_left // 60}분 {self.time_left % 60}초")
        self.time_label.place(x=480, y=210)  # 시간 레이블 보이기
        
        self.progress_bar['value'] = 0  # 프로그레스바 리셋
        self.start_button.place_forget()  # 시험 시작 버튼 숨기기
        self.load_test_words()
        self.next_word()

    def load_test_words(self):
        # 난이도에 따라 toeicword에서 20개 단어 가져옴
        selected_difficulty = self.level_var.get()

        cursor = self.connection.cursor()
        cursor.execute("SELECT Spell, Mean FROM toeicword WHERE Difficulty = %s ORDER BY RAND() LIMIT 20", (selected_difficulty,))
        words = cursor.fetchall()
        cursor.close()

        if words:
            self.test_words = words
            self.total_questions = len(self.test_words)
            self.current_index = 0
            self.correct_count = 0
            self.update_progress()  # 초기 진행 상황 업데이트
        else:
            messagebox.showinfo("단어 없음", "선택한 난이도에 해당하는 단어가 없습니다.")
            self.start_button.place(x=520, y=370)  # 시험 시작 버튼 다시 보이기

    def next_word(self):
        # 다음 단어 가져옴, 다 풀면 종료
        if self.current_index < len(self.test_words):
            current_word = self.test_words[self.current_index]
            self.exam_label.config(text=current_word[1])
            self.answer_entry.delete(0, tk.END)
        else:
            self.finish_test()

    def check_answer(self, event=None):
        # 정답 맞는지 확인해서 맞으면 correct count 증가, 그리고 정답 여부와 관계없이 index 1 증가
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
        self.start_button.place(x=520, y=370)  # 시험 시작 버튼 다시 보이기

        messagebox.showinfo("시험 종료", f"점수 : {self.correct_count}/{len(self.test_words)}")
        self.level_label.config(text="난이도를 선택하세요")  # 시험 종료 후 난이도 레이블 텍스트 리셋
        self.exam_label.config(text="")
        self.answer_entry.delete(0, tk.END)

if __name__ == "__main__":
    user_id = sys.argv[1] if len(sys.argv) > 1 else 'default_user'
    app = ExamApp(user_id)
    app.mainloop()
