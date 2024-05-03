import mysql.connector
from mysql.connector import Error
from tkinter import Tk, Canvas, messagebox
import tkinter as tk
import subprocess
import sys
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

def ListEntireUsers(window):
    # 기존 버튼 제거
    for UserButton in UserButtons:
        UserButton.destroy()
    UserButtons.clear()

    gap = 30
    yBefore = 29
    connection = ConnectMysql()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT nickname FROM user")  # id만 가져오도록 수정
        EntireUserNicknames = cursor.fetchall()
        for index, UserNickname in enumerate(EntireUserNicknames):
            UserButton = tk.Button(window, text=f"{UserNickname[0]}")
            yBefore += gap
            UserButton.pack()
            UserButton.place(x=500, y=yBefore+gap, width=150, height=30)
            UserButtons.append(UserButton)

def ListSpecificUsers(window):
    # 기존 버튼 제거
    SearchUser = UserSearchInput.get()
    if(len(SearchUser) ==0):
        messagebox.showinfo("검색 오류", "입력이 올바르게 되지 않았습니다. 다시 시도해주세요.")
    else:
        
        for UserButton in UserButtons:
            UserButton.destroy()
        UserButtons.clear()


        gap = 30
        yBefore = 29
        connection = ConnectMysql()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT nickname FROM user WHERE nickname LIKE %s", ('%' + SearchUser + '%',))
            SpecificUserNicknames = cursor.fetchall()
            if(len(SpecificUserNicknames) == 0):
                messagebox.showinfo("검색 오류", "해당 사용자 정보가 없습니다.")
            
            for index, UserNickname in enumerate(SpecificUserNicknames):
                UserButton = tk.Button(window, text=f"{UserNickname[0]}")
                yBefore += gap
                UserButton.pack()
                UserButton.place(x=500, y=yBefore+gap, width=150, height=30)
                UserButtons.append(UserButton)

# 초기화
UserButtons = []
def GoAdminStatusPage(adminID):
    window.destroy()
    subprocess.run(['python', 'AdminStatusPage.py',adminID])
window = Tk()
window.title("회원 관리 페이지")
window.geometry("747x531")
window.configure(bg = "#FFFFFF")

adminID = "pjy"
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



UserSearchInput = tk.Entry()
UserSearchInput.place(x=28, y=102, width=200, height=40)

UserSearchBtn = tk.Button(text="회원조회", command=lambda: ListSpecificUsers(window))
UserSearchBtn.place(x = 250, y=102, width=100, height=40)


UserDeleteBtn = tk.Button(text="선택 회원 삭제")
UserDeleteBtn.place(x=187, y=193, width=150, height=40)

UserDeleteBtn = tk.Button(text="전체 회원 조회", command=lambda: ListEntireUsers(window)) # 수정된 부분
UserDeleteBtn.place(x=28, y=193, width=150, height=40)

TextWidget = tk.Text(window)
scrollbar = tk.Scrollbar(window, command=TextWidget.yview)
scrollbar.pack(side="right", fill="y")

GoHomeBtn = tk.Button(text="이전으로", command=lambda:GoAdminStatusPage(adminID))
GoHomeBtn.place(x=15, y = 483, width=90, height=40)


canvas.create_rectangle(
    450.0,
    45.0,
    700.0,
    525.0,
    fill="#FFFFFF",
    outline="black")

window.resizable(False, False)
window.mainloop()
