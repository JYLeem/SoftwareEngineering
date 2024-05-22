import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import sys
from Util import Util
from PIL import Image, ImageTk

class DayStudy(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.geometry("800x600")
        self.title("일자별 학습")
        self.configure(bg="#FFFFFF")
        self.connection = self.connect_database()
        self.current_page = 0
        self.days_per_page = 30  # 한 페이지당 일 수
        self.create_widgets()
        self.update_progress_bar()
    
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
        
        self.buttons_frame = tk.Frame(self, bg="#FFFFFF")
        self.buttons_frame.place(x=25, y=90)

        self.day_label = tk.Label(self, text="학습 일자를 선택하세요", font=("Helvetica", 16), bg="#FFFFFF")
        self.day_label.place(x=70, y=45)

        self.bar_label = tk.Label(self, text="진도율", font=("Helvetica", 12), bg="#FFFFFF")
        self.bar_label.place(x=145, y=285)
        
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=300, mode='determinate', maximum=100)
        self.progress_bar.place(x=25, y=310)
        self.progress_bar['value'] = 0
        
        self.load_image("시험진행도.png")  # 이미지 경로 지정

        # '이전', '다음' 버튼 추가
        self.prev_button = tk.Button(self, text="이전", command=self.prev_page, width=7, height=1)
        self.prev_button.place(x=25, y=250)
        self.next_button = tk.Button(self, text="다음", command=self.next_page, width=7, height=1)
        self.next_button.place(x=260, y=250)

        self.load_day_buttons()

        # 단어 목록을 표시할 Frame과 Scrollbar 생성
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
        
    def load_day_buttons(self):
        # 일자선택 버튼 생성
        cursor = self.connection.cursor()
        cursor.execute("SELECT MAX(Day) FROM toeicword")
        max_day = cursor.fetchone()[0]
        cursor.close()
        
        self.total_pages = (max_day + self.days_per_page - 1) // self.days_per_page
        
        self.update_day_buttons()
        
    def update_day_buttons(self):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        
        start_day = self.current_page * self.days_per_page
        end_day = start_day + self.days_per_page
        if end_day > start_day + self.days_per_page:
            end_day = start_day + self.days_per_page
        
        cursor = self.connection.cursor()
        cursor.execute("SELECT DISTINCT Day FROM toeicword WHERE Day BETWEEN %s AND %s ORDER BY Day", (start_day, end_day))
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

        self.update_navigation_buttons()

    def update_navigation_buttons(self):
        if self.current_page > 0:
            self.prev_button.config(state=tk.NORMAL)
        else:
            self.prev_button.config(state=tk.DISABLED)
        
        if self.current_page < self.total_pages - 1:
            self.next_button.config(state=tk.NORMAL)
        else:
            self.next_button.config(state=tk.DISABLED)

    def load_image(self, image_path):
        # 캔버스 설정
        self.canvas_img = tk.Canvas(self, width=300, height=200, bg='white', borderwidth=0, highlightthickness=0)
        self.canvas_img.place(x=25, y=350)  # 이미지 위치 지정

        # 이미지 파일 열기
        image = Image.open(image_path)
            
        # 캔버스 크기에 맞게 이미지 크기 조정
        resized_image = image.resize((300, 200), Image.Resampling.LANCZOS)  # 이미지를 300x200 크기로 조정
        photo = ImageTk.PhotoImage(resized_image)

        # 캔버스에 이미지 배치, 위치는 캔버스 중앙
        self.canvas_img.create_image(150, 100, image=photo)
            
        # 이미지 객체 참조를 유지해야 이미지가 화면에 나타남
        self.canvas_img.image = photo           

    def select_day(self, day):
        # 일자 선택에 따라 보여지는 텍스트 조정
        self.current_day = day
        self.day_label.config(text=f"{day+1}일차 단어 학습")
        self.load_words(day)

    def load_words(self, day):
        # 선택한 일자의 단어를 가져와서 표시
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        cursor = self.connection.cursor()
        cursor.execute("SELECT Spell, Mean FROM toeicword WHERE Day = %s", (day,))
        words = cursor.fetchall()
        cursor.close()
        
        for spell, mean in words:
            word_frame = tk.Frame(self.scrollable_frame, bg="#F0F0F0", padx=10, pady=5)
            word_frame.pack(fill="x", padx=5, pady=2)

            # Spell Label
            spell_label = tk.Label(word_frame, text=spell, font=("Helvetica", 12, "bold"), bg="#F0F0F0", anchor="w", wraplength=200)
            spell_label.grid(row=0, column=0, sticky="w")

            # Mean Label
            mean_label = tk.Label(word_frame, text=mean, font=("Helvetica", 12), bg="#F0F0F0", anchor="e", wraplength=290)
            mean_label.grid(row=0, column=1, sticky="e")

            # Ensure that both labels fill the frame evenly
            word_frame.grid_columnconfigure(0, weight=1)
            word_frame.grid_columnconfigure(1, weight=1)



    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_day_buttons()
    
    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_day_buttons()

    def update_progress_bar(self):
        # 데이터베이스 연결
        conn = mysql.connector.connect(
            host='ystdb.cl260eouqhjz.ap-northeast-2.rds.amazonaws.com',
            user='admin',
            password='seat0323',
            database='wordbook'
        )
        cursor = conn.cursor()

        # 쿼리 실행
        cursor.execute("SELECT wordday FROM user WHERE id = %s", (self.user,))
        wordday = cursor.fetchone()[0]

        cursor.execute("SELECT MAX(Day) FROM toeicword")
        total_day = cursor.fetchone()[0]

        # 연결 종료
        conn.close()

        # 진행도 계산
        progress_value = (wordday / total_day) * 100
        self.progress_bar['value'] = progress_value

if __name__ == "__main__":
    user_id = sys.argv[1] if len(sys.argv) > 1 else 'default_user'
    app = DayStudy(user_id)
    app.mainloop()
