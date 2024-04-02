import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
import tkinter as tk

def connect_mysql():
    try:
        connection = mysql.connector.connect(host='ystdb.cl260eouqhjz.ap-northeast-2.rds.amazonaws.com',
                                                database='wordbook',
                                                user='admin',
                                                password='seat0323')
        if connection.is_connected():
            return connection
    except Error as e:
            print("Error while connecting to MySQL", e)  

            
            
def login():
    connection = connect_mysql()  # MySQL에 연결
    
    if connection:  # 연결 확인
        username = username_entry.get()
        password = password_entry.get()

        if connection.is_connected():
            cursor = connection.cursor()

            # admin 테이블에서 사용자 조회
            cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
            admin_user = cursor.fetchone()

            if admin_user:
                messagebox.showinfo("로그인 성공", "관리자로 로그인 성공!")
                admin_page(connection)
            else:
                # admin 테이블에 사용자가 없으면 users 테이블에서 조회
                cursor.execute("SELECT * FROM user WHERE username=%s AND password=%s", (username, password))
                user = cursor.fetchone()
                if user:
                    messagebox.showinfo("로그인 성공", "사용자로 로그인 성공!")
                    user_page(connection)
                else:
                    messagebox.showerror("로그인 실패", "로그인 실패. 사용자 이름 또는 비밀번호를 확인하세요.")

def user_page(connection):
        if connection.is_connected():
            cursor = connection.cursor()
            user_window = tk.Tk()
            user_window.title("사용자 페이지")
            # 단어 조회
            cursor.execute("SELECT Day FROM toeicword")

            days = cursor.fetchall()
            for day in enumerate(days):
                day_button = tk.Button(user_window, text=f"Day {day[0]+1}", command=lambda day=day[0]+1: list_words(day, connection))
                day_button.pack()
    
          


            
def list_words(day, connection):

        if connection.is_connected():
            cursor = connection.cursor()

            # 단어 조회
            cursor.execute("SELECT Spell, Mean FROM toeicword WHERE Day = %s", (day,))
            words = cursor.fetchall()

            # 화면에 출력
            word_window = tk.Tk()
            word_window.title("단어 페이지")
        for index, word in enumerate(words):
                    spell_label = tk.Label(word_window, text=f"{index+1}. {word[0]} - {word[1]}")
                    spell_label.pack()

def admin_page(connection):
        if connection.is_connected():
            cursor = connection.cursor()

            # Day 조회
            cursor.execute("SELECT DISTINCT Day FROM toeicword")

            days = cursor.fetchall()

            # 화면에 출력
            admin_window = tk.Tk()
            admin_window.title("관리자 페이지")

            for day in enumerate(days):
                day_button = tk.Button(admin_window, text=f"Day {day[0]}")
                day_button.pack()
# 메인 윈도우 생성
root = tk.Tk()
root.title("로그인")

# 라벨 스타일
label_style = {'font': ('Helvetica', 12), 'padx': 10, 'pady': 5}

# 입력 필드 스타일
entry_style = {'font': ('Helvetica', 12), 'width': 20}

# 로그인 버튼 스타일
button_style = {'font': ('Helvetica', 12), 'width': 15, 'pady': 5}

# 사용자 이름 라벨 및 입력 필드
username_label = tk.Label(root, text="아이디:", **label_style)
username_label.pack()
username_entry = tk.Entry(root, **entry_style)
username_entry.pack()

# 비밀번호 라벨 및 입력 필드
password_label = tk.Label(root, text="비밀번호:", **label_style)
password_label.pack()
password_entry = tk.Entry(root, show="*", **entry_style)
password_entry.pack()

# 로그인 버튼
login_button = tk.Button(root, text="로그인", command=login, **button_style)
login_button.pack()

# 윈도우 실행
root.mainloop()
