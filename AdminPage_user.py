import mysql.connector
from mysql.connector import Error
from tkinter import Tk, Canvas, messagebox
import tkinter as tk
import subprocess

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

def list_entire_users(window):
    # 기존 버튼 제거
    for user_button in user_buttons:
        user_button.destroy()
    user_buttons.clear()

    gap = 30
    yBefore = 29
    connection = connect_mysql()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT nickname FROM user")  # id만 가져오도록 수정
        entire_user_nicknames = cursor.fetchall()
        for index, user_nickname in enumerate(entire_user_nicknames):
            user_button = tk.Button(window, text=f"{user_nickname[0]}")
            yBefore += gap
            user_button.pack()
            user_button.place(x=500, y=yBefore+gap, width=150, height=30)
            user_buttons.append(user_button)

def list_specific_users(window):
    # 기존 버튼 제거
    search_user = user_search_input.get()
    if(len(search_user) ==0):
        messagebox.showinfo("검색 오류", "입력이 올바르게 되지 않았습니다. 다시 시도해주세요.")
    else:
        
        for user_button in user_buttons:
            user_button.destroy()
        user_buttons.clear()


        gap = 30
        yBefore = 29
        connection = connect_mysql()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT nickname FROM user WHERE nickname LIKE %s", ('%' + search_user + '%',))
            entire_user_nicknames = cursor.fetchall()
            for index, user_nickname in enumerate(entire_user_nicknames):
                user_button = tk.Button(window, text=f"{user_nickname[0]}")
                yBefore += gap
                user_button.pack()
                user_button.place(x=500, y=yBefore+gap, width=150, height=30)
                user_buttons.append(user_button)

# 초기화
user_buttons = []
def go_back():
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
canvas.create_rectangle(
    392.0,
    0.0,
    747.0,
    531.0,
    fill="#CCCCCC",
    outline="")



user_search_input = tk.Entry()
user_search_input.place(x=28, y=102, width=200, height=40)

user_search_btn = tk.Button(text="회원조회", command=lambda: list_specific_users(window))
user_search_btn.place(x = 250, y=102, width=100, height=40)


user_delete_btn = tk.Button(text="선택 회원 삭제")
user_delete_btn.place(x=187, y=193, width=150, height=40)

user_delete_btn = tk.Button(text="전체 회원 조회", command=lambda: list_entire_users(window)) # 수정된 부분
user_delete_btn.place(x=28, y=193, width=150, height=40)

scrollbar = tk.Scrollbar()
scrollbar.place(x=707, y = 11, width=50, height=510)

back_home_btn = tk.Button(text="홈으로", command=go_back)
back_home_btn.place(x=15, y = 483, width=90, height=40)


canvas.create_rectangle(
    467.0,
    29.0,
    650.0,
    309.0,
    fill="#CCCCCC",
    outline="")

window.resizable(False, False)
window.mainloop()
