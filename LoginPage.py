import mysql.connector
from mysql.connector import Error
from tkinter import Tk, Canvas, messagebox
import tkinter as tk
import subprocess

def ConnectMysql():
    try:
        connection = mysql.connector.connect(host='ystdb.cl260eouqhjz.ap-northeast-2.rds.amazonaws.com',
                                                database='wordbook',
                                                user='admin',
                                                password='seat0323')
        if connection.is_connected():
            return connection
    except Error as e:
            print("Error while connecting to MySQL", e)  
            
def Login():
    connection = ConnectMysql()  # MySQL에 연결
    
    if connection:  # 연결 확인
        id = IDEntry.get()
        password = PasswordEntry.get()

        if connection.is_connected():
            cursor = connection.cursor()

            # admin 테이블에서 사용자 조회
            cursor.execute("SELECT * FROM admin WHERE id=%s AND password=%s", (id, password))
            IsAdmin = cursor.fetchone()

            if IsAdmin:
                messagebox.showinfo("로그인 성공", "관리자로 로그인 성공!")
                GoAdminPage()
                
            else:
                # admin 테이블에 사용자가 없으면 users 테이블에서 조회
                cursor.execute("SELECT * FROM user WHERE id=%s AND password=%s", (id, password))
                IsUser = cursor.fetchone()
                if IsUser:
                    messagebox.showinfo("로그인 성공", "사용자로 로그인 성공!")
                else:
                    messagebox.showerror("로그인 실패", "로그인 실패. 사용자 이름 또는 비밀번호를 확인하세요.")
def GoSignUp():
    window.destroy()
    subprocess.run(['python', 'SignUpPage.py'])
def GoAdminPage():
    window.destroy()
    subprocess.run(['python', 'AdminPage_select.py'])

window = Tk()

window.geometry("747x531")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 531,
    width = 747,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
IDEntry = tk.Entry(bd=0, bg="#CCCCCC",fg="#000716",  highlightthickness=0)
IDEntry.place(x=128.0, y=218.0, width=520, height = 34)

PasswordEntry = tk.Entry(bd=0, bg="#CCCCCC",fg="#000716",  highlightthickness=0, show='*')
PasswordEntry.place(x=128.0, y=279.0, width=520, height = 34)
canvas.create_text(
    110.0, 233.0,
    text="ID",
    font=("Arial-BoldMT", int(13.0)), anchor="w"
)

canvas.create_text(
    98.0, 294.0,
    text="PW",
    font=("Arial-BoldMT", int(13.0)), anchor="w"
)


canvas.create_text(
    126.0,
    72.0,
    anchor="nw",
    text="TOEIC 영단어 학습 프로그램",
    fill="#000000",
    font=("Inter", 40 * -1)
)
SignUpBtn = tk.Button(text="회원가입", command=GoSignUp)
SignUpBtn.place(x=374, y=350, width = 133, height = 33)
LogInBtn = tk.Button(text="로그인", command=Login)
LogInBtn.place(x=530, y=350, width = 133, height = 33)
window.resizable(False, False)
window.mainloop()
