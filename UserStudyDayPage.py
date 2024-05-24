import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import sys
from Util import Util
from PIL import Image, ImageTk
import datetime

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
        self.words_per_page = 12  # 한 페이지당 단어 수, 초기값 설정
        self.current_word_page = 0  # 현재 단어 페이지
        self.wordday = 0  # 사용자 단어일 초기값
        self.create_widgets()
        self.update_progress_bar()
    
    def connect_database(self):
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
        style = ttk.Style()
        style.configure("TButton",
                        padding=0,  # 패딩을 0으로 설정
                        background="#FFFFFF",  # 배경색 제거
                        relief="flat")  # 테두리 제거

        self.back_button = self.create_image_button(
            normal_image_path="이전으로일반.png",
            hover_image_path="이전으로호버.png",
            command=lambda: Util.SwitchPage(self, "UserMainPage", self.user),
            scale=0.8
        )
        self.back_button.place(x=25, y=10)
        
        self.buttons_frame = tk.Frame(self, bg="#FFFFFF")
        self.buttons_frame.place(x=25, y=90)

        self.day_label = tk.Label(self, text="학습 일자를 선택하세요", font=("Helvetica", 16), bg="#FFFFFF")
        self.day_label.place(x=70, y=45)

        self.bar_label = tk.Label(self, text="진도율", font=("Helvetica", 12), bg="#FFFFFF")
        self.bar_label.place(x=145, y=285)
        
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=300, mode='determinate', maximum=100)
        self.progress_bar.place(x=25, y=310)
        self.progress_bar['value'] = 0
        
        self.load_image("시험진행도.png")

        self.prev_button = self.create_image_button(
            normal_image_path="이전버튼일반.png",
            hover_image_path="이전버튼호버.png",
            command=self.prev_page,
            scale=1.0
        )
        self.prev_button.place(x=25, y=250)
        
        self.next_button = self.create_image_button(
            normal_image_path="다음버튼일반.png",
            hover_image_path="다음버튼호버.png",
            command=self.next_page,
            scale=1.0
        )
        self.next_button.place(x=260, y=250)

        self.load_day_buttons()

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
        
        self.word_prev_button = self.create_image_button(
            "이전버튼일반.png", "이전버튼호버.png", self.prev_word_page, 1.0
        )
        self.word_next_button = self.create_image_button(
            "다음버튼일반.png", "다음버튼호버.png", self.next_word_page, 1.0
        )
        self.word_prev_button.place(x=400, y=556)
        self.word_next_button.place(x=500, y=556)
        self.word_prev_button.place_forget()
        self.word_next_button.place_forget()

    def create_image_button(self, normal_image_path, hover_image_path, command, scale):
        original_normal_image = Image.open(normal_image_path)
        original_hover_image = Image.open(hover_image_path)
        normal_image = ImageTk.PhotoImage(original_normal_image.resize(
            (int(original_normal_image.width * scale), int(original_normal_image.height * scale)), Image.Resampling.LANCZOS))
        hover_image = ImageTk.PhotoImage(original_hover_image.resize(
            (int(original_hover_image.width * scale), int(original_hover_image.height * scale)), Image.Resampling.LANCZOS))
        button = tk.Label(self, image=normal_image, bg="#FFFFFF")
        button.image = normal_image
        button.bind("<Enter>", lambda e: button.config(image=hover_image))
        button.bind("<Leave>", lambda e: button.config(image=normal_image))
        button.bind("<Button-1>", lambda e: command())
        return button
        
    def load_day_buttons(self):
        cursor = self.connection.cursor()
        
        # Get maximum day from toeicword table
        cursor.execute("SELECT MAX(Day) FROM toeicword")
        max_day = cursor.fetchone()[0]
        
        # Get user wordday and gendate
        cursor.execute("SELECT wordday, gendate FROM user WHERE id = %s", (self.user,))
        user_data = cursor.fetchone()
        wordday, gendate = user_data[0], user_data[1]
        
        cursor.close()

        # Convert gendate to date type if it's datetime
        if isinstance(gendate, datetime.datetime):
            gendate = gendate.date()

        today = datetime.date.today()
        days_since_gendate = (today - gendate).days

        # Limit wordday to days_since_gendate
        if wordday > days_since_gendate:
            wordday = days_since_gendate

        self.wordday = wordday  # Update self.wordday

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
                    btn = ttk.Button(self.buttons_frame, text=f"{day+1}", command=lambda d=day: self.select_day(d), width=7, style="TButton")
                    if day < self.wordday:  # 수정된 부분: day < self.wordday
                        btn.state(['!disabled'])  # Enable button if within wordday limit
                    else:
                        btn.state(['disabled'])  # Disable button if beyond wordday limit
                    btn.grid(row=r, column=c, padx=1, pady=1)
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
        self.canvas_img = tk.Canvas(self, width=300, height=200, bg='white', borderwidth=0, highlightthickness=0)
        self.canvas_img.place(x=25, y=350)

        image = Image.open(image_path)
        resized_image = image.resize((300, 200), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)

        self.canvas_img.create_image(150, 100, image=photo)
        self.canvas_img.image = photo           

    def select_day(self, day):
        self.current_day = day
        self.day_label.config(text=f"{day+1}일차 단어 학습")
        self.current_word_page = 0  # 일자 선택 시 단어 페이지 초기화
        self.load_words(day+1)  # 수정된 부분: day+1 전달

    def load_words(self, day):
        cursor = self.connection.cursor()
        cursor.execute("SELECT Spell, Mean FROM toeicword WHERE Day = %s", (day,))
        self.words = cursor.fetchall()
        cursor.close()
        self.display_words()

    def display_words(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        self.update_idletasks()  # 레이아웃 업데이트

        frame_height = self.word_frame.winfo_height() * 0.99  # 프레임 높이의 90%를 사용
        word_frame_height = 40  # 각 단어 프레임의 높이
        self.words_per_page = max(1, int(frame_height / word_frame_height))  # 최소 1개의 단어는 표시
        
        start_index = self.current_word_page * self.words_per_page
        end_index = min(start_index + self.words_per_page, len(self.words))
        
        for spell, mean in self.words[start_index:end_index]:
            word_frame = tk.Frame(self.scrollable_frame, bg="#F0F0F0", padx=10, pady=5)
            word_frame.pack(fill="x", padx=5, pady=2)

            spell_label = tk.Label(word_frame, text=spell, font=("Helvetica", 12, "bold"), bg="#F0F0F0", anchor="w", wraplength=200)
            spell_label.grid(row=0, column=0, sticky="w")

            mean_label = tk.Label(word_frame, text=mean, font=("Helvetica", 12), bg="#F0F0F0", anchor="e", wraplength=290)
            mean_label.grid(row=0, column=1, sticky="e")

            word_frame.grid_columnconfigure(0, weight=1)
            word_frame.grid_columnconfigure(1, weight=1)

        self.update_word_navigation_buttons()


    def update_word_navigation_buttons(self):
        self.word_prev_button.place(x=400, y=556)
        self.word_next_button.place(x=500, y=556)
        
        if self.current_word_page > 0:
            self.word_prev_button.config(state=tk.NORMAL)
        else:
            self.word_prev_button.config(state=tk.DISABLED)
        
        if (self.current_word_page + 1) * self.words_per_page < len(self.words):
            self.word_next_button.config(state=tk.NORMAL)
        else:
            self.word_next_button.config(state=tk.DISABLED)

    def prev_word_page(self):
        if self.current_word_page > 0:
            self.current_word_page -= 1
            self.display_words()

    def next_word_page(self):
        if (self.current_word_page + 1) * self.words_per_page < len(self.words):
            self.current_word_page += 1
            self.display_words()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_day_buttons()

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_day_buttons()


    def update_progress_bar(self):
        cursor = self.connection.cursor()

        cursor.execute("SELECT wordday FROM user WHERE id = %s", (self.user,))
        wordday = cursor.fetchone()[0]

        cursor.execute("SELECT MAX(Day) FROM toeicword")
        total_day = cursor.fetchone()[0]

        cursor.close()

        progress_value = (wordday / total_day) * 100
        self.progress_bar['value'] = progress_value

if __name__ == "__main__":
    user_id = sys.argv[1] if len(sys.argv) > 1 else 'default_user'
    app = DayStudy(user_id)
    app.mainloop()
