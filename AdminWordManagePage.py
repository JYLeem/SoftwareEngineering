import mysql.connector
from mysql.connector import Error
from datetime import datetime
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

def ListEntireWords(window):
    # 기존 버튼 제거
    for SpellButton, MeanButton, DiffiButton in zip(SpellButtons, MeanButtons, DiffiButtons):
            SpellButton.destroy()
            MeanButton.destroy()
            DiffiButton.destroy()
    SpellButtons.clear()
    MeanButtons.clear()
    DiffiButtons.clear()

   
    connection = ConnectMysql()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT Spell, Mean, Difficulty FROM toeicword")  # id만 가져오도록 수정
        EntireWordInfos = cursor.fetchall()
        yGap = 30
        yPos = 44
        for index, WordInfo in enumerate(EntireWordInfos):
                SpellButton = tk.Button(window, text=f"{WordInfo[0]}")
                MeanButton = tk.Button(window, text=f"{WordInfo[1]}")
                DiffiButton = tk.Button(window, text=f"{WordInfo[2]}")
                
                
                SpellButton.pack()
                SpellButton.place(x=393, y=yPos, width=111, height=30)
                
                MeanButton.pack()
                MeanButton.place(x=504, y=yPos, width=111, height=30)
                
                DiffiButton.pack()
                DiffiButton.place(x=615, y=yPos, width=111, height=30)
                yPos += yGap
                SpellButtons.append(SpellButton)
                MeanButtons.append(MeanButton)
                DiffiButtons.append(DiffiButton)

def ListSpecificWords(window):
    # 기존 버튼 제거
    SearchWord = SearchWordInput.get()
    if(len(SearchWord) ==0):
        messagebox.showinfo("검색 오류", "입력이 올바르게 되지 않았습니다. 다시 시도해주세요.")
    else:
    
        for SpellButton, MeanButton, DiffiButton in zip(SpellButtons, MeanButtons, DiffiButtons):
            SpellButton.destroy()
            MeanButton.destroy()
            DiffiButton.destroy()

        SpellButtons.clear()
        MeanButtons.clear()
        DiffiButtons.clear()
        
        yGap = 30
        yPos = 44
        connection = ConnectMysql()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT Spell, Mean, Difficulty FROM toeicword WHERE Spell LIKE %s", ('%' + SearchWord + '%',))
            EntireWordInfos = cursor.fetchall()
            for index, WordInfo in enumerate(EntireWordInfos):
                SpellButton = tk.Button(window, text=f"{WordInfo[0]}")
                MeanButton = tk.Button(window, text=f"{WordInfo[1]}")
                DiffiButton = tk.Button(window, text=f"{WordInfo[2]}")
                
                
                SpellButton.pack()
                SpellButton.place(x=393, y=yPos, width=111, height=30)
                
                MeanButton.pack()
                MeanButton.place(x=504, y=yPos, width=111, height=30)
                
                DiffiButton.pack()
                DiffiButton.place(x=615, y=yPos, width=111, height=30)
                yPos += yGap
                SpellButtons.append(SpellButton)
                MeanButtons.append(MeanButton)
                DiffiButtons.append(DiffiButton)
                
def InsertWord(adminID):
    connection = ConnectMysql()
    spell = SpellInput.get()
    mean = MeanInput.get()
    difficulty = DifficultyInput.get()
    now = datetime.now()
    message = f"{adminID}님이 {spell} 단어를 추가하셨습니다."
    print(message)
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO toeicword(Spell, Mean, Difficulty) VALUES (%s, %s, %s)", (spell, mean, difficulty))
        connection.commit()  # 커밋을 수행하여 변경 사항을 DB에 적용
        cursor.execute("INSERT INTO history(admin, log, changetime) VALUES (%s, %s, %s)", (adminID, message, now))
        connection.commit()  # 커밋을 수행하여 변경 사항을 DB에 적용
        cursor.close()  # 커서 닫기
        connection.close()  # 커넥션 닫기   
        messagebox.showinfo("단어 추가 성공", "단어가 성공적으로 추가되었습니다.")
def DeleteWord():
    connection = ConnectMysql()
    spell = SpellInput.get()
    mean = MeanInput.get()
    difficulty = DifficultyInput.get()
    if connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM toeicword WHERE Spell = %s AND Mean = %s AND Difficulty = %s", (spell, mean, difficulty))
        connection.commit()  # 커밋을 수행하여 변경 사항을 DB에 적용
        cursor.close()  # 커서 닫기
        connection.close()  # 커넥션 닫기   
        messagebox.showinfo("단어 삭제 성공", "단어가 성공적으로 삭제되었습니다.")
def GoAdminStatusPage(adminID):
    window.destroy()
    subprocess.run(['python', 'AdminStatusPage.py',adminID])
SpellButtons=[]
MeanButtons=[]
DiffiButtons=[]
window = Tk()
window.title("단어 관리 페이지")
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
ListEntireWordsBtn = tk.Button(text="전체 단어 조회", command=lambda:ListEntireWords(window))
ListEntireWordsBtn.place(x=188, y=422, width=150, height=40)

SearchWordInput = tk.Entry()
SearchWordInput.place(x=32, y=103, width=200, height=40)

SearchWordBtn = tk.Button(text="단어 검색", command=lambda:ListSpecificWords(window))
SearchWordBtn.place(x=240, y=103, width=100, height=40)

UpdateWordBtn = tk.Button(text="단어 수정")
UpdateWordBtn.place(x=143, y=361, width=90, height=40)

DeleteWordBtn = tk.Button(text="단어 삭제", command=DeleteWord)
DeleteWordBtn.place(x=37, y=361, width=90, height=40)

InsertWordBtn = tk.Button(text="단어 추가", command=lambda:InsertWord(adminID))
InsertWordBtn.place(x=249, y=361, width=90, height=40)

GoHomeBtn = tk.Button(text="이전으로", command=lambda:GoAdminStatusPage(adminID))
GoHomeBtn.place(x=15, y=483, width=90, height=40)


canvas.create_rectangle(
    392.0,
    45.0,
    725.0,
    525.0,
    fill="#FFFFFF",
    outline="black")
canvas.create_text(
    12.0, 182.0,
    text="영단어 : ",
    font=("Arial-BoldMT", int(13.0)), anchor="w"
)
canvas.create_text(
   430.0, 30.0,
   text="Spell",
   font=("Arial-BoldMT", int(13.0)), anchor="w" 
)
canvas.create_text(
   540.0, 30.0,
   text="Mean",
   font=("Arial-BoldMT", int(13.0)), anchor="w" 
)
canvas.create_text(
   634.0, 30.0,
   text="Difficulty",
   font=("Arial-BoldMT", int(13.0)), anchor="w" 
)
SpellInput = tk.Entry()
SpellInput.place(x=90, y=170, width=250, height=30)
canvas.create_text(
    12.0, 235.0,
    text="뜻 :",
    font=("Arial-BoldMT", int(13.0)), anchor="w"
)
MeanInput = tk.Entry()
MeanInput.place(x=90, y=223, width=250, height=30)
canvas.create_text(
    12.0, 288.0,
    text="난이도 :",
    font=("Arial-BoldMT", int(13.0)), anchor="w"
)
DifficultyInput = tk.Entry()
DifficultyInput.place(x=90, y=276, width=250, height=30)

# 텍스트 위젯 생성
TextWidget = tk.Text(window)

# 스크롤바 생성
scrollbar = tk.Scrollbar(window, command=TextWidget.yview)
scrollbar.pack(side="right", fill="y")

# 스크롤바와 텍스트 위젯 연결
TextWidget.config(yscrollcommand=scrollbar.set)


window.resizable(False, False)
window.mainloop()
