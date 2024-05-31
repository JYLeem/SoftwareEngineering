import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage, Label, Canvas
import mysql.connector
import random
import time
import sys
from PIL import Image, ImageTk
from Util import Util
from tkinter import font as tkFont
import os

class GameApp(tk.Tk):
    def __init__(self, current_user):
        super().__init__()
        self.geometry("750x530")
        self.title("수뭉이 키우기 게임")
        self.configure(bg='#ffffff')  # 배경색 설정

        self.db = self.connect_database()
        self.cursor = self.db.cursor()
        self.current_user = current_user
        self.game_duration = 2
        self.setup_game_variables()
        self.setup_ui()
        self.protocol("WM_DELETE_WINDOW", self.OnClosing)
        
    def OnClosing(self):
        Util.OnClosing(self.db, self.current_user)
        self.destroy()
        
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
        self.info_image = self.load_image("게임정보수뭉이.png", (275, 181), alpha=True)  # 게임 정보 이미지 추가
        self.background_info_image = self.load_image("게임배경배경.jpg", (279, 185), alpha=True)  # 배경 이미지 추가
        self.logo_image = self.load_image("게임로고.png", (450, 100), alpha=True)  # 게임 로고 이미지 추가
        self.level_info_bg = self.load_image("레벨정보배경.jpg", (120, 30), alpha=True)  # 레벨 정보 배경 이미지 추가
        self.time_info_bg = self.load_image("남은시간배경.jpg", (180, 30), alpha=True)  # 남은 시간 배경 이미지 추가

        # 메이플스토리 폰트 로드
        self.maple_font_16_bold = tkFont.Font(family="Maplestory", size=16, weight="bold")
        self.maple_font_15_bold = tkFont.Font(family="Maplestory", size=15, weight="bold")
        self.maple_font_13_bold = tkFont.Font(family="Maplestory", size=13, weight="bold")
        self.maple_font_14 = tkFont.Font(family="Maplestory", size=14)

    def setup_ui(self):
        # 배경 이미지 로드 및 설정
        self.background_image = self.load_background_image("게임배경.jpg", (750, 530))
        self.bg_label = Label(self, image=self.background_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.back_button = self.create_image_button("이전으로일반.png", "이전으로호버.png", command=self.SwitchToUserMainPage, width=50, height=30)
        self.back_button.place(x=10, y=10)
        
        # 실시간 순위 라벨과 프레임 위치 조정
        self.leaderboard_label = tk.Label(self, text="현재 실시간 순위", font=self.maple_font_16_bold, bg='#8C5105', foreground='white')
        self.leaderboard_label.place(x=375, y=370, anchor="center")
        self.leaderboard_frame = tk.Frame(self, bg='#8C5105')
        self.leaderboard_frame.place(x=375, y=425, anchor="center")
        self.display_leaderboard()
        
        # 수뭉이 이미지 위치 조정
        self.image_label = Label(self, image=self.images[self.level], bg='#48B8FA')
        self.image_label.pack(pady=5)
        
        # 게임 시작 버튼 위치 조정
        self.button_start = self.create_image_button("게임시작일반.png", "게임시작호버.png", self.start_game, 90, 40)
        self.button_start.place(x=325, y=277)
        
        # 문제 라벨을 word_frame 외부로 이동
        self.label_word = tk.Label(self, text="", font=("Arial-BoldMT", 20), bg='#48B8FA')
        self.label_word.pack(pady=5)
        
        # 문제와 입력 필드를 포함하는 프레임 생성
        self.word_frame = tk.Frame(self, bg='#48B8FA')
        self.word_frame.place_forget()  # 게임 시작 전에는 숨김

        # 입력 필드
        self.entry_answer = ttk.Entry(self.word_frame, font=("Arial-BoldMT", 20))
        self.entry_answer.pack(pady=10)
        self.entry_answer.bind("<Return>", self.check_answer)
        
        self.label_status = tk.Label(self, text="", font=self.maple_font_15_bold, bg='#8C5105', width=12)
        self.label_status.place_forget()

        self.label_timer = tk.Label(self, text="", font=self.maple_font_13_bold, bg='#8C5105', width=15)
        self.label_timer.place_forget()
        
        # 게임 정보 이미지 캔버스 생성
        self.info_canvas = Canvas(self, width=275, height=181, bg='#48B8FA', highlightthickness=0)
        self.info_canvas.create_image(0, 0, anchor="nw", image=self.background_info_image)
        self.info_canvas.create_image(0, 0, anchor="nw", image=self.info_image)
        self.info_canvas.place_forget()  # 초기에는 숨김

        # 게임 로고 이미지 라벨 생성
        self.logo_label = Label(self, image=self.logo_image, bg='#48B8FA')
        self.logo_label.place(x=130, y=170)

    def load_images(self):
        image_paths = {
            1: "수뭉이1.png",
            2: "수뭉이2.png",
            3: "수뭉이3.png",
            4: "수뭉이4.png",
            5: "수뭉이5.png"
        }
        # 이미지 로드 시 알파 채널을 사용하여 투명한 배경을 처리
        return {level: self.load_image(path, (180, 180), alpha=True) for level, path in image_paths.items()}

    def load_image(self, path, size, alpha=False):
        image = Image.open(path)
        if alpha:
            image = image.convert("RGBA")  # 알파 채널을 사용하여 투명한 배경 처리
        return ImageTk.PhotoImage(image.resize(size, Image.Resampling.LANCZOS))

    def load_background_image(self, path, size):
        image = Image.open(path)
        return ImageTk.PhotoImage(image.resize(size, Image.Resampling.LANCZOS))

    def create_image_button(self, normal_image_path, hover_image_path, command, width, height):
        # 이미지 로드 및 리사이징
        normal_image = Image.open(normal_image_path).resize((width, height), Image.Resampling.LANCZOS).convert("RGBA")
        hover_image = Image.open(hover_image_path).resize((width, height), Image.Resampling.LANCZOS).convert("RGBA")
        
        normal_image_tk = ImageTk.PhotoImage(normal_image)
        hover_image_tk = ImageTk.PhotoImage(hover_image)

        button = tk.Label(self, image=normal_image_tk, bg='#48B8FA')
        button.image = normal_image_tk  # 이미지 참조 보관

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
        self.label_status.config(text=f"레벨: {self.level}, 점수: {self.current_score}", foreground='white')
        self.label_status.place(x=296, y=372)  # 위치 조정
        
        # 숨겨진 요소들 보이기
        self.word_frame.place(relx=0.5, rely=0.6, anchor="center")  # 중앙에 위치 조정
        self.label_word.pack(pady=5)
        self.label_timer.place(x=292, y=403)  # 상태 정보를 위치 조정
        self.info_canvas.place(x=279, y=360)  # 게임 정보 이미지 위치 조정

        # 로고 이미지 숨기기
        self.logo_label.place_forget()

        # 레벨과 타이머를 info image 위로 보이도록 설정
        self.label_status.tkraise()
        self.label_timer.tkraise()

        # 시작 시 숨김 처리되었던 요소들 보이기
        self.button_start.place_forget()
        self.leaderboard_label.place_forget()
        self.leaderboard_frame.place_forget()
        
        self.update_timer()  # 타이머 업데이트 시작

    def next_word(self):
        self.current_word, self.current_meaning = self.fetch_word()
        self.label_word.config(text=self.current_meaning)

    def display_leaderboard(self):
        """리더보드를 갱신하는 메서드"""
        # 리더보드 프레임 내의 모든 위젯을 제거
        for widget in self.leaderboard_frame.winfo_children():
            widget.destroy()
        # 데이터베이스에서 상위 3명의 사용자 정보를 다시 조회
        self.cursor.execute("SELECT id, highscore FROM user ORDER BY highscore DESC LIMIT 3")
        rows = self.cursor.fetchall()
        for idx, (user_id, score) in enumerate(rows, start=1):
            tk.Label(self.leaderboard_frame, text=f"{idx}등: {user_id} - {score}점", font=self.maple_font_14, bg='#8C5105', foreground='white').pack()

    def show_transparent_popup(self, message, color, image):
        popup = tk.Toplevel(self)
        popup.overrideredirect(True)  # 윈도우 테두리와 제목 표시줄 제거
        popup.geometry("200x80+{}+{}".format(self.winfo_x() + 280, self.winfo_y() + 100))
        popup.attributes('-alpha', 0.7)  # 윈도우 투명도 설정 (70%)

        # 이미지와 텍스트를 포함하는 레이블 생성
        if image:
            label_image = tk.Label(popup, image=image, bg='#ffffff')
            label_image.pack(side='top')
        
        popup_label = tk.Label(popup, text=message, font=("Arial-BoldMT", 16), fg=color, bg="white")
        popup_label.pack(expand=True, fill='both')
        # 팝업을 700ms 후에 자동으로 닫기
        popup.after(700, popup.destroy)

    def level_up(self):
        if self.level <= 4 and self.current_score % 30 == 0:
            self.level += 1
        self.label_status.config(text=f"레벨: {self.level}, 점수: {self.current_score}")
        self.image_label.config(image=self.images[self.level])
    
    # 최고 점수 업데이트
    def update_high_score(self):
        """사용자의 최고 점수를 데이터베이스에 업데이트하는 메서드"""
        query = "UPDATE user SET highscore = %s WHERE id = %s AND highscore < %s"
        try:
            self.cursor.execute(query, (self.current_score, self.current_user, self.current_score))
            self.db.commit()
        except mysql.connector.Error as err:
            self.db.rollback()

    def update_timer(self):
        if not self.game_active:
            return  # 게임이 비활성화 상태면 타이머 업데이트 중단
        elapsed_time = int(time.time() - self.start_time)
        remaining_time = self.game_duration * 60 - elapsed_time
        minutes, seconds = divmod(remaining_time, 60)
        formatted_time = f"{minutes:02}분 {seconds:02}초"
        self.label_timer.config(text=f"남은 시간: {formatted_time}", foreground='white')
        if remaining_time > 0:
            self.after(1000, self.update_timer)  # 1초 후 다시 이 메서드를 호출
        else:
            messagebox.showinfo("게임 종료", "게임이 종료되었습니다")
            self.update_high_score()
            messagebox.showinfo("게임 종료", f"최종 점수: {self.current_score}")
            self.reset_game()

    def reset_game(self):
        """게임을 리셋하고 초기 화면을 준비하는 메서드"""
        self.game_active = False
        self.update_high_score()  # 게임이 끝나면 점수 업데이트
        self.display_leaderboard()  # 데이터베이스에서 갱신된 순위로 리더보드 갱신
        self.current_score = 0
        self.level = 1
        self.label_word.config(text="다시 시작하려면 게임 시작을 누르세요")
        self.label_word.pack(pady=5)  # 다시 화면에 표시
        self.label_status.place_forget()
        self.label_timer.place_forget()
        self.entry_answer.delete(0, tk.END)
        self.word_frame.place_forget()  # 초기 화면에서는 입력 필드를 숨김
        self.info_canvas.place_forget()  # 게임 정보 이미지 숨김
        # 게임 시작 버튼을 다시 표시
        self.button_start.place(x=325, y=277)
        # 로고 이미지 다시 보이기
        # self.logo_label.place(x=130, y=170)
        # 리더보드 프레임과 라벨을 다시 배치
        self.leaderboard_label.place(x=375, y=370, anchor="center")
        self.leaderboard_frame.place(x=375, y=425, anchor="center")
        # 리더보드 내용을 갱신
        self.display_leaderboard()
        self.image_label.config(image=self.images[self.level])
        
    def SwitchToUserMainPage(self):
        from UserMainPage import UserMainPage
        self.destroy()
        app = UserMainPage(self.current_user)
        app.mainloop()
if __name__ == "__main__":
    current_user = sys.argv[1] if len(sys.argv) > 1 else 'default_user'
    app = GameApp(current_user)
    app.mainloop()
