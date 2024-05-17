import mysql.connector
from mysql.connector import Error
from tkinter import Tk, Canvas, Entry, Text, Button, ttk, messagebox
import tkinter as tk
import sys
import subprocess
from Util import Util

connection = Util.ConnectMysql()
def LoadWordDay(day):
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

window = Tk()
window.title("날짜별 학습 페이지")
window.geometry("1250x750")
window.configure(bg = "#FFFFFF")
user = sys.argv[1]
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

if connection:
        cursor = connection.cursor(buffered=True)    
        cursor.execute("SELECT wordday from user where id = %s", (user,))
        UserDay = cursor.fetchone()  # 커서를 다시 열어서 새로운 쿼리 실행
        cursor.execute("SELECT DISTINCT Day FROM toeicword")
        EntireDays = cursor.fetchall()
        row = 0
        for index, day in enumerate(EntireDays):
            DayButton = tk.Button(window, text=f"{day[0]}")
            if index+1 < UserDay[0]:
                DayButton.config(bg="lime")
            elif index+1 == UserDay[0]:
                DayButton.config(bg="yellow")
            else:
                DayButton.config(state="disabled")
            DayButton.config(command=lambda day=day[0]: (LoadWordDay(day)))
            DayButton.pack()
            DayButton.place(x=xPos, y=yPos, width=100, height=35)
            xPos += xGap
            row+=1
            if row == 5:
                row = 0
                xPos = 10
                yPos += yGap
TextWidget = tk.Text(window)
GoPrevPageBtn = tk.Button(text="이전으로", command=lambda: Util.SwitchPage(window, "UserMainPage", user))
GoPrevPageBtn.place(x=10, y=670, width=133, height=38)
# 스크롤바 생성
scrollbar = tk.Scrollbar(window, command=TextWidget.yview)
scrollbar.pack(side="right", fill="y")

# 스크롤바와 텍스트 위젯 연결
TextWidget.config(yscrollcommand=scrollbar.set)

window.resizable(False, False)
window.mainloop()
