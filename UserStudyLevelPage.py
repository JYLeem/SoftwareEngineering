import tkinter as tk
from tkinter import ttk, messagebox, font as tkFont
import mysql.connector
import sys
from Util import Util
from PIL import Image, ImageTk

class LevelStudy(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.geometry("800x600")
        self.title("수준별 학습")
        self.configure(bg="#FFFFFF")
        self.connection = self.connect_database()
        self.words = []
        self.current_page = 0
        self.words_per_page = 10

        # 메이플스토리 폰트 로드
        self.maple_font_14_bold = tkFont.Font(family="Maplestory", size=14, weight="bold")

        self.create_widgets()
    
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

    def get_user_level(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT level FROM user WHERE id = %s", (self.user,))
            level = cursor.fetchone()[0]
            cursor.close()
            return level
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"An error occurred: {err}")
            self.destroy()
            return 0
    
    def create_widgets(self):
        # 기본 요소 생성함수
        
        # 이전 버튼 추가, 좌표 지정
        self.back_button = self.create_image_button(
            "이전으로일반.png", "이전으로호버.png",
            lambda: Util.SwitchPage(self, "UserMainPage", self.user), 0.8
        )
        self.back_button.place(x=25, y=10)

        # 난이도 선택 레이블 및 드롭다운 메뉴 추가
        self.level_label = tk.Label(self, text="난이도를 선택해!", font=self.maple_font_14_bold, bg="#FFFFFF")
        self.level_label.place(x=70, y=135)

        self.level_var = tk.StringVar(value="하")
        self.level_dropdown = ttk.Combobox(self, textvariable=self.level_var, values=["하", "중", "상"], state="readonly", font=("Helvetica", 12))
        self.level_dropdown.place(x=37, y=60)
        self.level_dropdown.bind("<<ComboboxSelected>>", self.update_level_label)
        
        # 현재 레벨을 표시하는 라벨 추가
        self.user_level = self.get_user_level()
        self.level_text_label = tk.Label(self, text=f"Level {self.user_level}", font=("Helvetica", 12, "bold"), bg="#FFFFFF")
        self.level_text_label.place(x=145, y=295)  # 위치를 조정

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=300, mode='determinate', maximum=100)
        self.progress_bar.place(x=25, y=320)  # 위치를 사진 아래로 조정
        self.update_progress_bar()  # 프로그레스바 업데이트

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
        self.load_level_image()  # 수준별 시험의 이미지를 로드
        
        # 이전, 다음 버튼 추가
        self.word_prev_button = self.create_image_button(
            "이전버튼일반.png", "이전버튼호버.png", self.prev_page, 1.0
        )
        self.word_next_button = self.create_image_button(
            "다음버튼일반.png", "다음버튼호버.png", self.next_page, 1.0
        )
        self.word_prev_button.place(x=400, y=556)
        self.word_next_button.place(x=500, y=556)

        self.update_buttons()

    def update_progress_bar(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT level FROM user WHERE id = %s", (self.user,))
        level = cursor.fetchone()[0]
        cursor.close()
        
        level_quotient = level // 100
        progress_value = level % 100
        
        self.level_text_label.config(text=f"Level {level_quotient}")
        self.progress_bar['value'] = progress_value

    
    def load_image(self, image_path):
        # 캔버스 설정
        self.canvas_img = tk.Canvas(self, width=300, height=200, bg='white', borderwidth=0, highlightthickness=0)
        self.canvas_img.place(x=25, y=350)

        # 이미지 파일 열기
        image = Image.open(image_path)
            
        # 캔버스 크기에 맞게 이미지 크기 조정
        resized_image = image.resize((300, 200), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)

        # 캔버스에 이미지 배치, 위치는 캔버스 중앙
        self.canvas_img.create_image(150, 100, image=photo)
            
        # 이미지 객체 참조를 유지해야 이미지가 화면에 나타남
        self.canvas_img.image = photo           

    def load_level_image(self):
        image = Image.open("수준선택수뭉이.png")
        resized_image = image.resize((320, 182), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)
        self.level_image_canvas = tk.Canvas(self, width=320, height=182, bg='white', highlightthickness=0)
        self.level_image_canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        self.level_image_canvas.image = photo
        self.level_image_canvas.place(x=15, y=95)
        self.level_label.tkraise()  # 라벨을 최상위 레벨로 올림

    def update_level_label(self, event=None):
        selected_level = self.level_var.get()
        if self.load_words() != 1:
            self.level_label.config(text=f"{selected_level} 난이도를 선택했어!", font=self.maple_font_14_bold, bg="#FFFFFF")
            self.level_label.place(x=50, y=135)
            self.level_label.tkraise()  # 라벨을 최상위 레벨로 올림
        
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
        
    def load_words(self, event=None):
        selected_difficulty = self.level_var.get()

        if selected_difficulty == "하" and self.user_level >= 0:
            max_difficulty = "하"
        elif selected_difficulty == "중" and self.user_level >= 400:
            max_difficulty = "중"
        elif selected_difficulty == "상" and self.user_level >= 700:
            max_difficulty = "상"
        else:
            messagebox.showinfo("제한", "현재 레벨에서 접근할 수 없는 난이도입니다.")
            return 1

        cursor = self.connection.cursor()
        cursor.execute("SELECT Spell, Mean FROM toeicword WHERE Difficulty = %s ORDER BY Spell", (selected_difficulty,))
        self.words = cursor.fetchall()
        cursor.close()

        self.current_page = 0
        self.display_words()
        self.update_buttons()

    def display_words(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        self.update_idletasks()  # 레이아웃 업데이트

        frame_height = self.word_frame.winfo_height() * 0.99  # 프레임 높이의 99%를 사용
        word_frame_height = 40  # 각 단어 프레임의 높이
        self.words_per_page = max(1, int(frame_height / word_frame_height))  # 최소 1개의 단어는 표시
        
        start_index = self.current_page * self.words_per_page
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
        
        if self.current_page > 0:
            self.word_prev_button.config(state=tk.NORMAL)
        else:
            self.word_prev_button.config(state=tk.DISABLED)
        
        if (self.current_page + 1) * self.words_per_page < len(self.words):
            self.word_next_button.config(state=tk.NORMAL)
        else:
            self.word_next_button.config(state=tk.DISABLED)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_words()
            self.update_buttons()

    def next_page(self):
        if (self.current_page + 1) * self.words_per_page < len(self.words):
            self.current_page += 1
            self.display_words()
            self.update_buttons()

    def update_buttons(self):
        if self.current_page == 0:
            self.word_prev_button.config(state=tk.DISABLED)
        else:
            self.word_prev_button.config(state=tk.NORMAL)

        if (self.current_page + 1) * self.words_per_page >= len(self.words):
            self.word_next_button.config(state=tk.DISABLED)
        else:
            self.word_next_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    user_id = sys.argv[1] if len(sys.argv) > 1 else 'default_user'
    app = LevelStudy(user_id)
    app.mainloop()
