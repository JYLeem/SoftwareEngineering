import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Button
import mysql.connector
import time
from PIL import Image, ImageTk
from Util import Util
from tkinter import font as tkFont
import sys
import os

class GameApp(tk.Tk):
    def __init__(self, current_user):
        super().__init__()
        self.geometry("750x530")
        self.title("수뭉이 키우기 게임")
        self.configure(bg='#ffffff')

        self.db = self.connect_database()
        self.cursor = self.db.cursor()
        self.current_user = current_user
        self.game_duration = 1
        self.setup_game_variables()
        self.setup_ui()

    def connect_database(self):
        return mysql.connector.connect(
            host="ystdb.cl260eouqhjz.ap-northeast-2.rds.amazonaws.com",
            user="admin",
            password="seat0323",
            database="wordbook"
        )

    def setup_game_variables(self):
        self.current_score = 0
        self.level = 1
        self.start_time = time.time()
        self.game_active = False
        self.images = self.load_images()
        self.correct_image = self.load_image("수뭉이정답용.png", (50, 50), alpha=True)
        self.incorrect_image = self.load_image("수뭉이오답용.png", (50, 50), alpha=True)
        self.info_image = self.load_image("게임정보수뭉이.png", (275, 181), alpha=True)
        self.background_info_image = self.load_image("게임배경배경.jpg", (279, 185), alpha=True)
        self.logo_image = self.load_image("게임로고.png", (450, 100), alpha=True)
        self.level_info_bg = self.load_image("레벨정보배경.jpg", (161, 30), alpha=True)
        self.time_info_bg = self.load_image("남은시간배경.jpg", (207, 30), alpha=True)

        # 메이플스토리 폰트 로드
        self.maple_font_16_bold = tkFont.Font(family="Maplestory", size=16, weight="bold")
        self.maple_font_15_bold = tkFont.Font(family="Maplestory", size=15, weight="bold")
        self.maple_font_13_bold = tkFont.Font(family="Maplestory", size=13, weight="bold")
        self.maple_font_14 = tkFont.Font(family="Maplestory", size=14)

    def setup_ui(self):
        # 배경 이미지 로드 및 설정
        self.background_image = self.load_background_image("게임배경.jpg", (750, 530))
        self.bg_label = tk.Label(self, image=self.background_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.back_button = self.create_image_button("이전으로일반.png", "이전으로호버.png", lambda: Util.SwitchPage(self, "UserMainPage", self.current_user), 50, 30)
        self.back_button.place(x=10, y=10)
        
        # 실시간 순위 라벨과 프레임 위치 조정
        self.leaderboard_label = tk.Label(self, text="현재 실시간 순위", font=self.maple_font_16_bold, bg='#ffffff')
        self.leaderboard_label.place(x=375, y=370, anchor="center")
        self.leaderboard_frame = tk.Frame(self, bg='#ffffff')
        self.leaderboard_frame.place(x=375, y=425, anchor="center")
        self.display_leaderboard()
        
        # 수뭉이 이미지 위치 조정
        self.image_label = tk.Label(self, image=self.images[self.level], bg='#48B8FA')
        self.image_label.pack(pady=5)
        
        # 게임 시작 버튼 위치 조정
        self.button_start = self.create_image_button("게임시작일반.png", "게임시작호버.png", self.start_game, 90, 40)
        self.button_start.place(x=325, y=277)
        
        # 문제 라벨을 word_frame 외부로 이동
        self.label_word = tk.Label(self, text="", font=("Arial-BoldMT", 20), bg='#48B8FA')
        self.label_word.pack(pady=5)
        
        # 문제와 입력 필드를 포함하는 프레임 생성
        self.word_frame = tk.Frame(self, bg='#48B8FA')
        self.word_frame.place_forget()

        # 입력 필드
        self.entry_answer = ttk.Entry(self.word_frame, font=("Arial-BoldMT", 20))
        self.entry_answer.pack(pady=10)
        self.entry_answer.bind("<Return>", self.check_answer)
        
        # 레벨 상태 정보 버튼
        self.level_button = tk.Button(self, image=self.level_info_bg, text="", font=self.maple_font_15_bold, compound='center', relief="flat", disabledforeground="black",foreground="#FFFFFF", height=22, width=118)
        self.level_button.place_forget()

        # 남은 시간 버튼
        self.time_button = tk.Button(self, image=self.time_info_bg, text="", font=self.maple_font_13_bold, compound='center', relief="flat", disabledforeground="black",foreground="#FFFFFF", height=20, width=137)
        self.time_button.place_forget()
        
        # 게임 정보 이미지 캔버스 생성
        self.info_canvas = tk.Canvas(self, width=275, height=181, bg='#48B8FA', highlightthickness=0)
        self.info_canvas.create_image(0, 0, anchor="nw", image=self.background_info_image)
        self.info_canvas.create_image(0, 0, anchor="nw", image=self.info_image)
        self.info_canvas.place_forget()

        # 게임 로고 이미지 라벨 생성
        self.logo_label = tk.Label(self, image=self.logo_image, bg='#48B8FA')
        self.logo_label.place(x=130, y=170)

    def load_images(self):
        image_paths = {
            1: "수뭉이1.png",
            2: "수뭉이2.png",
            3: "수뭉이3.png",
            4: "수뭉이4.png",
            5: "수뭉이5.png"
        }
        return {level: self.load_image(path, (180, 180), alpha=True) for level, path in image_paths.items()}

    def load_image(self, path, size, alpha=False):
        image = Image.open(path)
        if alpha:
            image = image.convert("RGBA")
        return ImageTk.PhotoImage(image.resize(size, Image.Resampling.LANCZOS))

    def load_background_image(self, path, size):
        image = Image.open(path)
        return ImageTk.PhotoImage(image.resize(size, Image.Resampling.LANCZOS))
    
    

    def create_image_button(self, normal_image_path, hover_image_path, command, width, height):
        normal_image = Image.open(normal_image_path).resize((width, height), Image.Resampling.LANCZOS).convert("RGBA")
        hover_image = Image.open(hover_image_path).resize((width, height), Image.Resampling.LANCZOS).convert("RGBA")
        
        normal_image_tk = ImageTk.PhotoImage(normal_image)
        hover_image_tk = ImageTk.PhotoImage(hover_image)

        button = tk.Label(self, image=normal_image_tk, bg='#48B8FA')
        button.image = normal_image_tk

        def on_enter(event):
            button.config(image=hover_image_tk)

        def on_leave(event):
            button.config(image=normal_image_tk)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        button.bind("<Button-1>", lambda event: command())

        return button

    def fetch_word(self):
        self.cursor.execute("SELECT Spell, Mean FROM toeicword ORDER BY RAND() LIMIT 1")
        return self.cursor.fetchone()

    def check_answer(self, event=None):
        if not self.game_active:
            return
        answer = self.entry_answer.get().lower().strip()
        if answer == self.current_word:
            self.show_transparent_popup("정답입니다!", "green", self.correct_image)
            self.current_score += 10
            self.level_up()
        else:
            self.show_transparent_popup("오답입니다!", "red", self.incorrect_image)
        self.entry_answer.delete(0, tk.END)
        self.next_word()

    def start_game(self):
        self.game_active = True
        self.current_score = 0
        self.level = 1
        self.start_time = time.time()
        self.next_word()
        self.entry_answer.focus_set()
        
        # 점수와 레벨을 표시하는 라벨의 텍스트를 업데이트하고 화면에 표시
        self.level_button.config(text=f"레벨: {self.level}, 점수: {self.current_score}")
        self.level_button.place(x=308, y=363)
        
        # 숨겨진 요소들 보이기
        self.word_frame.place(relx=0.5, rely=0.6, anchor="center")
        self.label_word.pack(pady=5)
        self.time_button.place(x=297, y=392)
        self.info_canvas.place(x=279, y=345)
        
        # 버튼을 최상위로 올리기
        self.level_button.tkraise()
        self.time_button.tkraise()

        # 로고 이미지 숨기기
        self.logo_label.place_forget()

        # 시작 시 숨김 처리되었던 요소들 보이기
        self.button_start.place_forget()
        self.leaderboard_label.place_forget()
        self.leaderboard_frame.place_forget()
        
        self.update_timer()

    def next_word(self):
        self.current_word, self.current_meaning = self.fetch_word()
        self.label_word.config(text=self.current_meaning)

    def display_leaderboard(self):
        for widget in self.leaderboard_frame.winfo_children():
            widget.destroy()
        self.cursor.execute("SELECT id, highscore FROM user ORDER BY highscore DESC LIMIT 3")
        rows = self.cursor.fetchall()
        for idx, (user_id, score) in enumerate(rows, start=1):
            tk.Label(self.leaderboard_frame, text=f"{idx}등: {user_id} - {score}점", font=self.maple_font_14, bg='#ffffff').pack()

    def show_transparent_popup(self, message, color, image):
        popup = tk.Toplevel(self)
        popup.overrideredirect(True)
        popup.geometry("200x80+{}+{}".format(self.winfo_x() + 280, self.winfo_y() + 100))
        popup.attributes('-alpha', 0.7)

        if image:
            label_image = tk.Label(popup, image=image, bg='#ffffff')
            label_image.pack(side='top')
        
        popup_label = tk.Label(popup, text=message, font=("Arial-BoldMT", 16), fg=color, bg="white")
        popup_label.pack(expand=True, fill='both')
        popup.after(700, popup.destroy)

    def level_up(self):
        if self.level <= 4 and self.current_score % 10 == 0:
            self.level += 1
        self.level_button.config(text=f"레벨: {self.level}, 점수: {self.current_score}")
        self.image_label.config(image=self.images[self.level])
    
    def update_high_score(self):
        query = "UPDATE user SET highscore = %s WHERE id = %s AND highscore < %s"
        try:
            self.cursor.execute(query, (self.current_score, self.current_user, self.current_score))
            self.db.commit()
        except mysql.connector.Error as err:
            self.db.rollback()

    def update_timer(self):
        if not self.game_active:
            return
        elapsed_time = int(time.time() - self.start_time)
        remaining_time = self.game_duration * 60 - elapsed_time
        minutes, seconds = divmod(remaining_time, 60)
        formatted_time = f"{minutes:02}분 {seconds:02}초"
        self.time_button.config(text=f"남은 시간: {formatted_time}")
        if remaining_time > 0:
            self.after(1000, self.update_timer)
        else:
            messagebox.showinfo("게임 종료", "게임이 종료되었습니다")
            self.update_high_score()
            messagebox.showinfo("게임 종료", f"최종 점수: {self.current_score}")
            self.reset_game()

    def reset_game(self):
        self.game_active = False
        self.update_high_score()
        self.display_leaderboard()
        self.current_score = 0
        self.level = 1
        self.label_word.config(text="다시 시작하려면 게임 시작을 누르세요")
        self.label_word.pack(pady=5)
        self.level_button.place_forget()
        self.time_button.place_forget()
        self.entry_answer.delete(0, tk.END)
        self.word_frame.place_forget()
        self.info_canvas.place_forget()
        self.button_start.place(x=325, y=277)
        self.logo_label.place(x=130, y=170)
        self.leaderboard_label.place(x=375, y=370, anchor="center")
        self.leaderboard_frame.place(x=375, y=425, anchor="center")
        self.display_leaderboard()
        self.image_label.config(image=self.images[self.level])

if __name__ == "__main__":
    current_user = sys.argv[1] if len(sys.argv) > 1 else 'default_user'
    app = GameApp(current_user)
    app.mainloop()
