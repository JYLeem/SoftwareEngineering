import mysql.connector
from mysql.connector import Error
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import tkinter as tk
import subprocess
import sys
from Util import Util

connection = Util.ConnectMysql()

def DisplayStatus():
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT Spell from toeicword")
        NumWords = cursor.fetchall()
        cursor.execute("SELECT id from user")
        NumUsers = cursor.fetchall()
        NumAccesses = 0
        canvas.create_text(
            100.0, 175.0,
            text=f"{len(NumWords)}",
            font=("Arial-BoldMT", int(13.0)), anchor="w"
        )
        canvas.create_text(
            330.0, 175.0,
            text=f"{len(NumUsers)}",
            font=("Arial-BoldMT", int(13.0)), anchor="w"
        )
        canvas.create_text(
            560.0, 175.0,
            text=f"{NumAccesses}",
            font=("Arial-BoldMT", int(13.0)), anchor="w"
        )
        cursor.execute("SELECT admin, log, changetime from history")
        xPos = 20
        yPos = 340
        yGap = 30
        ChangeHistorys = cursor.fetchall()
        MaxLength = max(len(f"{ChangeHistory[2]} {ChangeHistory[1]}") for ChangeHistory in ChangeHistorys)  # 가장 긴 내용의 길이
        for index, ChangeHistory in enumerate(ChangeHistorys):
            content = f"{ChangeHistory[2]} {ChangeHistory[1]}"
            PaddedContent = content.ljust(MaxLength)  # 내용을 가장 긴 길이로 맞춤
            CHLabel = tk.Label(window, text=PaddedContent, bg="white", justify="left")
            CHLabel.pack()
            CHLabel.place(x=xPos, y=yPos, width=400, height=30)
            yPos += yGap

        
window = Tk()
window.title("관리자 메인 페이지")
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
adminID = sys.argv[1]
AdminIDLabel = tk.Label(window, text=adminID)
AdminIDLabel.place(x=300,y=0,width=100,height=30)
ManageWordBtn = tk.Button(text = "단어 관리", command=lambda:Util.SwitchPage(window,"AdminWordManagePage",adminID))
ManageWordBtn.place(x=400, y=0, width=100, height=30)

ManageUserBtn = tk.Button(text="유저 관리", command=lambda:Util.SwitchPage(window, "AdminUserManagePage",adminID))
ManageUserBtn.place(x=500, y=0, width=100, height=30)

LogOutBtn = tk.Button(text = "로그아웃")
LogOutBtn.place(x=600, y=0, width=100, height=30)

canvas.create_rectangle(
    10.0,
    50.0,
    230.0,
    300.0,
    fill="#FFFFFF",
    outline="#000000")
canvas.create_text(
    85.0,60.0,
    text="단어 현황",
    font=("Arial-BoldMT", int(13.0)), anchor="w"
)
canvas.create_text(
    50.0,320.0,
    text="최근 활동",
    font=("Arial-BoldMT", int(13.0)), anchor="w"
)
canvas.create_rectangle(
    10.0,
    330.0,
    690.0,
    520.0,
    fill="#FFFFFF",
    outline="#000000")
canvas.create_rectangle(
    240.0,
    50.0,
    460.0,
    300.0,
    fill="#FFFFFF",
    outline="#000000")
canvas.create_text(
    315.0,60.0,
    text="유저 현황",
    font=("Arial-BoldMT", int(13.0)), anchor="w"
)
canvas.create_rectangle(
    470.0,
    50.0,
    690.0,
    300.0,
    fill="#FFFFFF",
    outline="#000000")
canvas.create_text(
    545.0,60.0,
    text="접속 유저",
    font=("Arial-BoldMT", int(13.0)), anchor="w"
)
DisplayStatus()
window.resizable(False, False)
window.mainloop()
