import mysql.connector
from mysql.connector import Error
from tkinter import Tk, Canvas, Entry, Text, Button, ttk, messagebox
import tkinter as tk

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
    for WordButton in WordButtons:
        WordButton.destroy()
    WordButtons.clear()

    gap = 30
    yBefore = 29
    connection = ConnectMysql()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT Spell FROM toeicword")  # id만 가져오도록 수정
        EntireWordSpells = cursor.fetchall()
        for index, WordSpell in enumerate(EntireWordSpells):
            WordButton = tk.Button(window, text=f"{WordSpell[0]}")
            yBefore += gap
            WordButton.pack()
            WordButton.place(x=500, y=yBefore+gap, width=150, height=30)
            WordButtons.append(WordButton)

def ListSpecificWords(window):
    # 기존 버튼 제거
    SearchWord = SearchWordInput.get()
    if(len(SearchWord) ==0):
        messagebox.showinfo("검색 오류", "입력이 올바르게 되지 않았습니다. 다시 시도해주세요.")
    else:
        
        for WordButton in WordButtons:
            WordButton.destroy()
        WordButtons.clear()


        gap = 30
        yBefore = 29
        connection = ConnectMysql()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT Spell FROM toeicword WHERE Spell LIKE %s", ('%' + SearchWord + '%',))
            EntireWordSpells = cursor.fetchall()
            for index, WordSpell in enumerate(EntireWordSpells):
                WordButton = tk.Button(window, text=f"{WordSpell[0]}")
                yBefore += gap
                WordButton.pack()
                WordButton.place(x=500, y=yBefore+gap, width=150, height=30)
                WordButtons.append(WordButton)
                
def InsertWord():
    connection = ConnectMysql()
    spell = SpellInput.get()
    mean = MeanInput.get()
    difficulty = DifficultyInput.get()
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO toeicword(Spell, Mean, Difficulty) VALUES (%s, %s, %s)", (spell, mean, difficulty))
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

WordButtons=[]
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

InsertWordBtn = tk.Button(text="단어 추가", command=InsertWord)
InsertWordBtn.place(x=249, y=361, width=90, height=40)

GoHomeBtn = tk.Button(text="홈으로")
GoHomeBtn.place(x=15, y=483, width=90, height=40)


canvas.create_rectangle(
    392.0,
    45.0,
    757.0,
    621.0,
    fill="#CCCCCC",
    outline="")
canvas.create_text(
    12.0, 182.0,
    text="영단어 : ",
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
scrollbar = tk.Scrollbar()
scrollbar.place(x=707, y = 11, width=10, height=510)

window.resizable(False, False)
window.mainloop()
