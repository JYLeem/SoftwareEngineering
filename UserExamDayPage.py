import tkinter as tk
from tkinter import messagebox
import mysql.connector
import random
import sys

class ExamApp(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.geometry("800x600")
        self.title("날짜별 학습 페이지")
        self.configure(bg="#FFFFFF")
        self.connection = self.connect_database()
        self.create_widgets()
        self.test_words = []  # 시험을 위한 단어 목록
        self.current_index = 0  # 현재 단어 인덱스
        self.correct_count = 0  # 맞은 단어 수
    
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
        self.buttons_frame = tk.Frame(self, bg="#FFFFFF")
        self.buttons_frame.pack(side="top", anchor="center")

        self.day_label = tk.Label(self, text="먼저 날짜를 선택하세요.", font=("Helvetica", 16), bg="#FFFFFF")
        self.day_label.pack(pady=(100, 0), anchor="center")
        
        self.answer_entry = tk.Entry(self, font=("Helvetica", 16))
        self.answer_entry.pack(pady=10, anchor="center")
        self.answer_entry.bind("<Return>", self.check_answer)

        self.start_button = tk.Button(self, text="시험 시작", command=self.start_test)
        self.start_button.pack(pady=(5, 10), anchor="center")

        self.load_day_buttons()
    
    def load_day_buttons(self):
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
                    btn = tk.Button(self.buttons_frame, text=f"{day}", command=lambda d=day: self.select_day(d), width=10, height=2)
                    btn.grid(row=r, column=c)
                except StopIteration:
                    break

    def select_day(self, day):
        self.current_day = day
        self.day_label.config(text=f"{day}일차 시험 준비")

    def start_test(self):
        if not hasattr(self, 'current_day'):
            messagebox.showinfo("Select Day", "Please select a day first!")
            return
        self.load_test_words()
        self.next_word()

    def load_test_words(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT Spell, Mean FROM toeicword WHERE Day = %s ORDER BY RAND() LIMIT 20", (self.current_day,))
        words = cursor.fetchall()
        cursor.close()
        self.test_words = words
        self.current_index = 0
        self.correct_count = 0

    def next_word(self):
        if self.current_index < len(self.test_words):
            current_word = self.test_words[self.current_index]
            self.day_label.config(text=current_word[1])
            self.answer_entry.delete(0, tk.END)
        else:
            self.finish_test()

    def check_answer(self, event=None):
        if self.current_index < len(self.test_words):
            if self.answer_entry.get().strip().lower() == self.test_words[self.current_index][0].lower():
                self.correct_count += 1
            self.current_index += 1
            self.next_word()

    def finish_test(self):
        messagebox.showinfo("Test Finished", f"You scored {self.correct_count}/{len(self.test_words)}")
        self.day_label.config(text=f"{self.current_day}일차 시험 준비")
        self.answer_entry.delete(0, tk.END)

if __name__ == "__main__":
    user_id = sys.argv[1] if len(sys.argv) > 1 else 'default_user'
    app = ExamApp(user_id)
    app.mainloop()
