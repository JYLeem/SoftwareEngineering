import mysql.connector
from mysql.connector import Error
from datetime import datetime
from tkinter import Tk, Canvas, messagebox, Frame
import tkinter as tk
import sys
import subprocess
from Util import Util

connection = Util.ConnectMysql()

def ListEntireWords(window):
    # 기존 버튼 제거
    for SpellButton, MeanButton, DiffiButton in zip(SpellButtons, MeanButtons, DiffiButtons):
            SpellButton.destroy()
            MeanButton.destroy()
            DiffiButton.destroy()
    SpellButtons.clear()
    MeanButtons.clear()
    DiffiButtons.clear()

    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT word_id, Spell, Mean, Difficulty FROM toeicword")  # id만 가져오도록 수정
        EntireWordInfos = cursor.fetchall()
        yGap = 30
        yPos = 44
        for index, WordInfo in enumerate(EntireWordInfos):
                SpellButton = tk.Button(window, text=f"{WordInfo[1]}")
                MeanButton = tk.Button(window, text=f"{WordInfo[2]}")
                DiffiButton = tk.Button(window, text=f"{WordInfo[3]}")
                
                SpellButton.place(x=393, y=yPos, width=111, height=30)
                
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
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT word_id, Spell, Mean, Difficulty FROM toeicword WHERE Spell LIKE %s", ('%' + SearchWord + '%',))
            EntireWordInfos = cursor.fetchall()
            for index, WordInfo in enumerate(EntireWordInfos):
                SpellButton = tk.Button(window, text=f"{WordInfo[1]}", command=lambda i=index: WordButtonClick(i))
                MeanButton = tk.Button(window, text=f"{WordInfo[2]}", command=lambda i=index: WordButtonClick(i))
                DiffiButton = tk.Button(window, text=f"{WordInfo[3]}", command=lambda i=index: WordButtonClick(i))
                
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
    spell = SpellInput.get()
    mean = MeanInput.get()
    difficulty = DifficultyInput.get()
    now = datetime.now()
    message = f"{adminID}님이 {spell} 단어를 추가하셨습니다."
    print(message)
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO toeicword(Spell, Mean, Difficulty) VALUES (%s, %s, %s)", (spell, mean, difficulty))
        cursor.execute("INSERT INTO history(admin, log, changetime) VALUES (%s, %s, %s)", (adminID, message, now))
        connection.commit()
        cursor.close()  # 커서 닫기
        messagebox.showinfo("단어 추가 성공", "단어가 성공적으로 추가되었습니다.")
def DeleteWord():
    spell = SpellInput.get()
    mean = MeanInput.get()
    difficulty = DifficultyInput.get()
    now = datetime.now()
    message = f"{adminID}님이 {spell} 단어를 삭제하셨습니다."
    if connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM toeicword WHERE Spell = %s AND Mean = %s AND Difficulty = %s", (spell, mean, difficulty))
        cursor.execute("INSERT INTO history(admin, log, changetime) VALUES (%s, %s, %s)", (adminID, message, now))
        connection.commit()  # 커밋을 수행하여 변경 사항을 DB에 적용
        cursor.close()  # 커서 닫기  
        messagebox.showinfo("단어 삭제 성공", "단어가 성공적으로 삭제되었습니다.")
        SearchWordInput.delete(0, tk.END)
        SpellInput.delete(0,tk.END)
        MeanInput.delete(0,tk.END)
        DifficultyInput.delete(0,tk.END)
        for i in range(3):
                    PrevInfos.pop()
        
def UpdateWord():
    spell = SpellInput.get()
    mean = MeanInput.get()
    difficulty = DifficultyInput.get()
    now = datetime.now()
    message = f"{adminID}님이 {spell} 단어를 수정하셨습니다."
    if connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE toeicword SET Spell = %s, Mean = %s, Difficulty = %s WHERE Spell = %s AND Mean = %s AND Difficulty = %s", (spell, mean, difficulty, PrevInfos[0], PrevInfos[1], PrevInfos[2]))
        cursor.execute("INSERT INTO history(admin, log, changetime) VALUES (%s, %s, %s)", (adminID, message, now))
        connection.commit()  # 커밋을 수행하여 변경 사항을 DB에 적용
        cursor.close()  # 커서 닫기
        
        messagebox.showinfo("단어 수정 성공", "단어가 성공적으로 수정되었습니다.")
        SearchWordInput.delete(0,tk.END)
        SpellInput.delete(0,tk.END)
        MeanInput.delete(0,tk.END)
        DifficultyInput.delete(0,tk.END)        
        for i in range(3):
                    PrevInfos.pop()
def WordButtonClick(index):
    for i in range(len(SpellButtons)):  # 모든 행에 대해 반복
        if i == index:  # 현재 클릭된 버튼과 같은 행의 버튼들만
            SpellButtons[i].configure(bg="skyblue")  # 다른 행의 버튼은 기본 색상으로 변경
            MeanButtons[i].configure(bg="skyblue")
            DiffiButtons[i].configure(bg="skyblue")
            
            SpellInput.delete(0,tk.END)
            SpellInput.insert(0,SpellButtons[i].cget("text"))
            MeanInput.delete(0,tk.END)
            MeanInput.insert(0,MeanButtons[i].cget("text"))
            DifficultyInput.delete(0,tk.END)
            DifficultyInput.insert(0,DiffiButtons[i].cget("text"))
            
            PrevInfos.append(SpellButtons[i].cget("text"))
            PrevInfos.append(MeanButtons[i].cget("text"))
            PrevInfos.append(DiffiButtons[i].cget("text"))
            
        else:
            SpellButtons[i].configure(bg="SystemButtonFace")  # 다른 행의 버튼은 기본 색상으로 변경
            MeanButtons[i].configure(bg="SystemButtonFace")
            DiffiButtons[i].configure(bg="SystemButtonFace")
        

PrevInfos=[]

SpellButtons=[]
MeanButtons=[]
DiffiButtons=[]

window = Tk()
window.title("단어 관리 페이지")
window.geometry("747x531")
window.configure(bg = "#FFFFFF")

adminID = sys.argv[1]

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

UpdateWordBtn = tk.Button(text="단어 수정", command=UpdateWord)
UpdateWordBtn.place(x=143, y=361, width=90, height=40)

DeleteWordBtn = tk.Button(text="단어 삭제", command=DeleteWord)
DeleteWordBtn.place(x=37, y=361, width=90, height=40)

InsertWordBtn = tk.Button(text="단어 추가", command=lambda:InsertWord(adminID))
InsertWordBtn.place(x=249, y=361, width=90, height=40)

GoHomeBtn = tk.Button(text="이전으로", command=lambda:Util.SwitchPage(window, "AdminMainPage", adminID))
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
