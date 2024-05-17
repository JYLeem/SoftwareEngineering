import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Pillow 라이브러리 필요
from tkinter import messagebox
import mysql.connector
import random
import sys


class StudyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Progress App")
        self.root.geometry("800x600")  # 윈도우 크기 설정

        self.connection = self.connect_database()
        
        # 달력 생성
        self.buttons_frame = tk.Frame(self.root, width=150, height=100)
        self.buttons_frame.grid(row=0, column=0, sticky='nw')
        self.buttons_frame.grid_propagate(False)  # 프레임 크기 고정
        self.load_day_buttons()
        
        # 진행도 막대
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=150, mode='determinate', maximum=100)
        self.progress_bar.grid(row=1, column=0, columnspan=2, pady=10, padx=50)
        
        # 이미지 캔버스
        self.canvas = tk.Canvas(self.root, width=200, height=150)
        self.canvas.grid(row=0, column=1)
        self.image_path = "수뭉이1.png"  # 이미지 경로 설정
        self.display_image(self.image_path)

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

    def load_study_data(self, date):
        # 날짜에 따라 데이터를 불러오는 기능 구현
        # 데이터베이스에서 데이터를 읽어와 진행도를 업데이트
        print(f"Loading data for {date}")
        self.update_progress(50)  # 예시 진행도 값

    def update_progress(self, value):
        self.progress_bar['value'] = value

    def display_image(self, path):
        image = Image.open(path)
        photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(100, 100, image=photo)  # 이미지 중앙 배치
        self.canvas.image = photo  # 참조 유지

if __name__ == "__main__":
    root = tk.Tk()
    app = StudyApp(root)
    root.mainloop()
