import mysql.connector
from mysql.connector import Error
from tkinter import Tk, Canvas, Entry, Text, Button, ttk, messagebox
import tkinter as tk
import sys
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

def LoadWordDay(day):
    connection = ConnectMysql()
    cursor = connection.cursor()
    cursor.execute("SELECT Spell, Mean from toeicword where Day = %s", (day,))
    wordInfos = cursor.fetchall()
    xGap = 300
    yGap = 40
    xPos = 10
    yPos = 210
    row = 0
    for index, wordInfo in enumerate(wordInfos):
            wordLabel = tk.Label(window, text=f"{wordInfo[0]}-{wordInfo[1]}")
            wordLabel.pack()
            wordLabel.place(x=xPos, y=yPos, width=300, height=40)
            labelWidth = wordLabel.winfo_reqwidth()
            print(labelWidth)
            
            
            xPos += xGap
            row+=1
            if row == 4:
                row = 0
                xPos = 10
                yPos += yGap
def ChangeButtonColor(button):
    button.configure(bg="lime")
    ColoredBtn.append(button)
    if(len(ColoredBtn) > 1):
        ColoredBtn[0].configure(bg="white")
        ColoredBtn[0] = ColoredBtn[1]
        ColoredBtn.pop()
def GoPrevPage():
    window.destroy()
    subprocess.run(['python', 'UserSelectActionPage.py'])
window = Tk()
window.title("날짜별 학습 페이지")
window.geometry("1250x750")
window.configure(bg = "#FFFFFF")

ColoredBtn = []

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
# 텍스트 위젯 생성
xGap = 100
yGap = 35
xPos = 10
yPos = 0
connection = ConnectMysql()
if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT Day FROM toeicword")  # id만 가져오도록 수정
        EntireDays = cursor.fetchall()
        row = 0
        for index, day in enumerate(EntireDays):
            DayButton = tk.Button(window, text=f"{day[0]}", bg="white")
            DayButton.config(command=lambda day=day[0], button=DayButton: (ChangeButtonColor(button), LoadWordDay(day)))
            DayButton.pack()
            DayButton.place(x=xPos, y=yPos, width=100, height=35)
            xPos += xGap
            row+=1
            if row == 5:
                row = 0
                xPos = 10
                yPos += yGap
TextWidget = tk.Text(window)
GoPrevPageBtn = tk.Button(text="이전으로", command=GoPrevPage)
GoPrevPageBtn.place(x=10, y=670, width=133, height=38)
# 스크롤바 생성
scrollbar = tk.Scrollbar(window, command=TextWidget.yview)
scrollbar.pack(side="right", fill="y")

# 스크롤바와 텍스트 위젯 연결
TextWidget.config(yscrollcommand=scrollbar.set)

window.resizable(False, False)
window.mainloop()
