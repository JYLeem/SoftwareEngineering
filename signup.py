import mysql.connector
import subprocess
from mysql.connector import Error
from tkinter import Tk, Canvas
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
            


def back_login():
    window.destroy()
    subprocess.run(['python', 'login.py'])           

def check_id_rebunduncy():
    connection = connect_mysql()
    if connection:
        id = id_entry.get()
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM user WHERE id=%s", (id,))
        id_rebunduncy = cursor.fetchall()
        if id_rebunduncy:
                messagebox.showinfo("아이디 중복", "이미 존재하는 아이디가 있습니다.")
                
        else:
                messagebox.showinfo("아이디 생성 가능", "사용 가능한 아이디 입니다.")

def check_nickname_rebunduncy():
    connection = connect_mysql()
    if connection:
        nickname = nickname_entry.get()
        cursor = connection.cursor()
        cursor.execute("SELECT nickname FROM user WHERE id=%s", (nickname,))
        id_rebunduncy = cursor.fetchall()
        if id_rebunduncy:
                messagebox.showinfo("닉네임 중복", "이미 존재하는 닉네임이 있습니다.")
                
        else:
                messagebox.showinfo("닉네임 생성 가능", "사용 가능한 닉네임 입니다.")
                
def signUp():
    connection = connect_mysql()
    if connection:
        nickname = nickname_entry.get()
        id = id_entry.get()
        password = password_entry.get()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO user (nickname, id, password) VALUES (%s, %s, %s)", (nickname, id, password,));
        connection.commit()  # 커밋을 수행하여 변경 사항을 DB에 적용
        cursor.close()  # 커서 닫기
        connection.close()  # 커넥션 닫기
        messagebox.showinfo("회원가입 성공", "회원가입이 완료되었습니다.")
        back_login()
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

nickname_entry = tk.Entry(bd=0, bg="#CCCCCC", fg="#000716",  highlightthickness=0)
nickname_entry.place(x=122.0, y=177.0, width=522, height=34)

nickname_rebunduncy_btn = tk.Button(text="중복 확인", command=check_nickname_rebunduncy)
nickname_rebunduncy_btn.place(x=650.0, y=177.0, width = 60, height=34)

id_entry = tk.Entry(bd=0, bg="#CCCCCC",fg="#000716",  highlightthickness=0)
id_entry.place(x=122.0, y=240.0, width=522, height = 34)
id_rebunduncy_btn = tk.Button(text="중복 확인", command=check_id_rebunduncy)
id_rebunduncy_btn.place(x=650.0, y=244.0, width = 60, height=34)

password_entry = tk.Entry(bd=0, bg="#CCCCCC",fg="#000716",  highlightthickness=0, show='*')
password_entry.place(x=122.0, y=303.0, width=520, height = 34)

canvas.create_text(
    70.0, 194.0,
    text="닉네임",
    font=("Arial-BoldMT", int(13.0)), anchor="w"
)

canvas.create_text(
    80.0, 257.0,
    text="ID",
    font=("Arial-BoldMT", int(13.0)), anchor="w"
)

canvas.create_text(
    80.0, 320,
    text="PW",
    font=("Arial-BoldMT", int(13.0)), anchor="w"
)
canvas.create_text(
    305.0,
    72.0,
    anchor="nw",
    text="회원가입",
    fill="#000000",
    font=("Inter", 40 * -1)
)

prev_btn = tk.Button(text="이전으로", command=back_login)
prev_btn.place(x=356, y=367, width=133, height=38)

signup_btn = tk.Button(text="회원가입", command=signUp)
signup_btn.place(x=511, y=367, width=133, height=38)

window.resizable(False, False)
window.mainloop()
