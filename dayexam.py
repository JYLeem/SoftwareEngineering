import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import sys
from Util import Util
from PIL import Image, ImageTk

class DayExam(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.geometry("800x600")
        self.title("일자별 시험")
        self.configure(bg="#FFFFFF")
        self.connection = self.connect_database()
        self.current_page = 0
        self.days_per_page = 30
        self.test_words = []
        self.entry_vars = []
        self.correct_count = 0
        self.total_questions = 20
        self.current_day = None
        self.current_test_page = 0
        self.time_remaining = 600
        self.timer_id = None
        self.sumoongi_image = None
        self.create_widgets()

    def connect_database(self):
        try:
            return mysql.connector.connect(
                host="ystdb.cl260eouqhjz.ap-northeast-2.rds.amazonaws.com",
                user="admin",
                password="seat0323",
                database="wordbook"
            )
        except mysql.connector.Error as err:
            messagebox.showerror("Database Connection Error", f"An error occurred: {err}")
            self.destroy()

    def create_widgets(self):
        self.back_button = self.create_image_button(
            "이전으로일반.png", "이전으로호버.png",
            lambda: Util.SwitchPage(self, "UserMainPage", self.user), 0.8
        )
        self.back_button.place(x=25, y=10)
        self.buttons_frame = tk.Frame(self, bg="#FFFFFF")
        self.buttons_frame.place(x=25, y=90)
        self.day_label = tk.Label(self, text="먼저 날짜를 선택하세요", font=("Helvetica", 16), bg="#FFFFFF")
        self.day_label.place(x=70, y=45)

        self.exam_frame_container = tk.Frame(self, bg="#FFFFFF", highlightbackground="black", highlightthickness=1)
        self.exam_frame_container.place(x=350, y=35, width=425, height=515)

        self.canvas = tk.Canvas(self.exam_frame_container, bg="#FFFFFF")
        self.scrollbar = tk.Scrollbar(self.exam_frame_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFFFFF")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.load_sumoongi_image()
        self.start_button = self.create_image_button(
            "시험시작일반.png", "시험시작호버.png", self.start_test, 1.0
        )
        self.start_button.place(x=130, y=310)

        self.timer_label = tk.Label(self, text="남은시간: 10분 00초", font=("Helvetica", 16), bg="#FFFFFF")
        self.timer_label.place_forget()
        self.end_button = self.create_image_button(
            "시험종료일반.png", "시험종료호버.png", self.finish_test, 1.0
        )
        self.end_button.place_forget()

        self.day_prev_button = self.create_image_button(
            "이전버튼일반.png", "이전버튼호버.png", self.prev_day_page, 1.0
        )
        self.day_next_button = self.create_image_button(
            "다음버튼일반.png", "다음버튼호버.png", self.next_day_page, 1.0
        )
        self.day_prev_button.place(x=25, y=250)
        self.day_next_button.place(x=260, y=250)

        self.prev_test_button = self.create_image_button(
            "이전버튼일반.png", "이전버튼호버.png", self.prev_test_page, 1.0
        )
        self.next_test_button = self.create_image_button(
            "다음버튼일반.png", "다음버튼호버.png", self.next_test_page, 1.0
        )
        self.prev_test_button.place_forget()
        self.next_test_button.place_forget()

        self.load_image("시험진행도.png")
        self.load_day_buttons()
        self.update_day_navigation_buttons()

    def load_sumoongi_image(self):
        image = Image.open("시험시작수뭉이.png")
        resized_image = image.resize((300, 300), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)
        self.sumoongi_canvas = tk.Canvas(self, width=300, height=300, bg='white', highlightthickness=0)
        self.sumoongi_canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        self.sumoongi_canvas.image = photo
        self.sumoongi_canvas.place(x=400, y=150)

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
        cursor.execute("SELECT MAX(Day) FROM toeicword")
        max_day = cursor.fetchone()[0]
        cursor.close()
        self.total_pages = (max_day + self.days_per_page - 1) // self.days_per_page
        self.update_day_buttons()

    def update_day_buttons(self):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        start_day = self.current_page * self.days_per_page
        end_day = min(start_day + self.days_per_page, start_day + self.days_per_page)
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
        self.update_day_navigation_buttons()

    def prev_day_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_day_buttons()

    def next_day_page(self):
        if (self.current_page + 1) * self.days_per_page < self.total_pages * self.days_per_page:
            self.current_page += 1
            self.update_day_buttons()

    def update_day_navigation_buttons(self):
        self.day_prev_button.place(x=25, y=250)
        self.day_next_button.place(x=260, y=250)
        if self.current_page > 0:
            self.day_prev_button.config(state=tk.NORMAL)
        else:
            self.day_prev_button.config(state=tk.DISABLED)
        if (self.current_page + 1) * self.days_per_page < self.total_pages * self.days_per_page:
            self.day_next_button.config(state=tk.NORMAL)
        else:
            self.day_next_button.config(state=tk.DISABLED)

    def load_image(self, image_path):
        self.canvas_img = tk.Canvas(self, width=300, height=200, bg='white', highlightthickness=0)
        self.canvas_img.place(x=25, y=350)
        image = Image.open(image_path)
        resized_image = image.resize((300, 200), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)
        self.canvas_img.create_image(150, 100, image=photo)
        self.canvas_img.image = photo

    def select_day(self, day):
        self.current_day = day
        self.day_label.config(text=f"{day+1}일차 시험 준비")

    def start_test(self):
        if not self.current_day:
            messagebox.showinfo("Select Day", "Please select a day first!")
            return
        self.sumoongi_canvas.place_forget()
        self.start_button.place_forget()
        self.timer_label.place(x=75, y=310)
        self.end_button.place(x=600, y=556)
        self.prev_test_button.place(x=400, y=556)
        self.next_test_button.place(x=500, y=556)
        self.load_test_words()
        self.display_test_words()
        self.reset_timer()
        self.update_timer()

    def load_test_words(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT Spell, Mean FROM toeicword WHERE Day = %s ORDER BY RAND() LIMIT 20", (self.current_day,))
        words = cursor.fetchall()
        cursor.close()
        self.test_words = words
        self.correct_count = 0
        self.entry_vars = [tk.StringVar() for _ in range(len(self.test_words))]
        self.current_test_page = 0

    def display_test_words(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        start_index = self.current_test_page * 10
        end_index = min(start_index + 10, len(self.test_words))
        for i, (spell, mean) in enumerate(self.test_words[start_index:end_index]):
            word_frame = tk.Frame(self.scrollable_frame, bg="#F0F0F0", padx=10, pady=5)
            word_frame.grid(row=i, column=0, columnspan=2, padx=5, pady=2, sticky="ew")
            mean_label = tk.Label(word_frame, text=mean, font=("Helvetica", 10), bg="#F0F0F0", anchor="w", wraplength=200)
            mean_label.grid(row=0, column=0, sticky="w", padx=0, pady=0)
            entry = tk.Entry(word_frame, textvariable=self.entry_vars[start_index + i], font=("Helvetica", 11), width=20)
            entry.grid(row=0, column=1, padx=0, pady=0, sticky="e")
            entry.grid(ipady=5)  # Adjust height with internal padding
            word_frame.grid_columnconfigure(0, weight=6)
            word_frame.grid_columnconfigure(1, weight=4)
        self.update_test_navigation_buttons()

    def update_test_navigation_buttons(self):
        if self.current_test_page > 0:
            self.prev_test_button.place(x=400, y=556)
            self.prev_test_button.config(state=tk.NORMAL)
        else:
            self.prev_test_button.config(state=tk.DISABLED)
        if (self.current_test_page + 1) * 10 < len(self.test_words):
            self.next_test_button.place(x=500, y=556)
            self.next_test_button.config(state=tk.NORMAL)
        else:
            self.next_test_button.config(state=tk.DISABLED)
        self.end_button.place(x=600, y=556)

    def prev_test_page(self):
        if self.current_test_page > 0:
            self.current_test_page -= 1
            self.display_test_words()

    def next_test_page(self):
        if (self.current_test_page + 1) * 10 < len(self.test_words):
            self.current_test_page += 1
            self.display_test_words()

    def update_timer(self):
        if self.time_remaining > 0:
            minutes, seconds = divmod(self.time_remaining, 60)
            self.timer_label.config(text=f"남은시간: {minutes:02}분 {seconds:02}초")
            self.time_remaining -= 1
            self.timer_id = self.after(1000, self.update_timer)
        else:
            self.finish_test()

    def reset_timer(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
        self.time_remaining = 600  # Reset to 10 minutes
        self.timer_label.config(text="남은시간: 10분 00초")

    def finish_test(self):
        self.reset_timer()
        self.timer_label.place_forget()  # 타이머 라벨 숨김

        # 기존 이미지 숨기고 새로운 이미지 표시
        self.canvas_img.place_forget()
        self.load_result_sumoongi_image()

        incorrect_words = [(spell, mean) for i, (spell, mean) in enumerate(self.test_words) if self.entry_vars[i].get().strip().lower() != spell.lower()]
        score_message = f"점수 : {len(self.test_words) - len(incorrect_words)}/{len(self.test_words)}"
        messagebox.showinfo("시험 종료", score_message)

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        frame_width = self.scrollable_frame.winfo_width()
        wrap_length = frame_width - 20

        for i, (spell, mean) in enumerate(incorrect_words):
            word_frame = tk.Frame(self.scrollable_frame, bg="#F0F0F0", padx=10, pady=5)
            word_frame.grid(row=i, column=0, padx=5, pady=2, sticky="ew")

            spell_label = tk.Label(word_frame, text=spell, font=("Helvetica", 10, "bold"), bg="#F0F0F0", anchor="w")
            spell_label.grid(row=0, column=0, sticky="w")
            spell_label.config(wraplength=wrap_length / 2)

            mean_label = tk.Label(word_frame, text=mean, font=("Helvetica", 10), bg="#F0F0F0", anchor="e")
            mean_label.grid(row=0, column=1, sticky="e")
            mean_label.config(wraplength=wrap_length / 2)

            word_frame.grid_columnconfigure(0, weight=1)
            word_frame.grid_columnconfigure(1, weight=1)

        self.prev_test_button.place_forget()
        self.next_test_button.place_forget()
        self.end_button.place_forget()

        # 결과 확인 버튼 이미지 적용
        self.result_confirm_button = self.create_image_button(
            "결과확인일반.png", "결과확인호버.png", self.reset_to_initial, 1.0
        )
        self.result_confirm_button.place(x=350, y=560)

    def load_result_sumoongi_image(self):
        image = Image.open("결과확인수뭉이.png")
        resized_image = image.resize((200, 200), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)
        self.result_sumoongi_canvas = tk.Canvas(self, width=200, height=200, bg='white', highlightthickness=0)
        self.result_sumoongi_canvas.create_image(100, 100, image=photo, anchor=tk.CENTER)
        self.result_sumoongi_canvas.image = photo
        self.result_sumoongi_canvas.place(x=85, y=310)  # Same position as the original image

    def reset_to_initial(self):
        self.result_confirm_button.place_forget()
        self.result_sumoongi_canvas.place_forget()
        self.load_image("시험진행도.png")  # Load the original image again
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.day_label.config(text="먼저 날짜를 선택하세요")
        self.load_day_buttons()
        self.sumoongi_canvas.place(x=400, y=150)
        self.start_button.place(x=130, y=310)


    def stop_test_and_go_back(self):
        self.reset_timer()
        self.finish_test()
        Util.SwitchPage(self, "UserMainPage", self.user)

if __name__ == "__main__":
    user_id = sys.argv[1] if len(sys.argv) > 1 else 'default_user'
    app = DayExam(user_id)
    app.mainloop()
