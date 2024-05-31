import mysql.connector
from mysql.connector import Error
from datetime import datetime
from tkinter import Tk, Canvas, messagebox, Frame
import tkinter as tk
import sys
import subprocess
from Util import Util

class AdminWordManagePage(tk.Tk):
    def __init__(self, adminID):
        super().__init__()
        self.adminID = adminID
        self.connection = Util.ConnectMysql()

        self.PrevInfos = [] 
        
        self.SpellButtons = []
        self.MeanButtons = []
        self.DiffiButtons = []

        self.title("단어 관리 페이지")
        self.geometry("747x531")
        self.configure(bg="#FFFFFF")

        self.canvas = tk.Canvas(
            bg="#FFFFFF",
            height=531,
            width=747,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.ListEntireWordsBtn = tk.Button(text="전체 단어 조회", command=self.ListEntireWords)
        self.ListEntireWordsBtn.place(x=188, y=422, width=150, height=40)

        self.SearchWordInput = tk.Entry()
        self.SearchWordInput.place(x=32, y=103, width=200, height=40)

        self.SearchWordBtn = tk.Button(text="단어 검색", command=self.ListSpecificWords)
        self.SearchWordBtn.place(x=240, y=103, width=100, height=40)

        self.UpdateWordBtn = tk.Button(text="단어 수정", command=self.UpdateWord)
        self.UpdateWordBtn.place(x=143, y=361, width=90, height=40)

        self.DeleteWordBtn = tk.Button(text="단어 삭제", command=self.DeleteWord)
        self.DeleteWordBtn.place(x=37, y=361, width=90, height=40)

        self.InsertWordBtn = tk.Button(text="단어 추가", command=self.InsertWord)
        self.InsertWordBtn.place(x=249, y=361, width=90, height=40)

        self.GoHomeBtn = tk.Button(text="이전으로", command=self.SwitchToAdminMainPage)
        self.GoHomeBtn.place(x=15, y=483, width=90, height=40)

        self.canvas.create_rectangle(
            392.0,
            45.0,
            725.0,
            525.0,
            fill="#FFFFFF",
            outline="black"
        )
        self.canvas.create_text(
            12.0, 182.0,
            text="영단어 : ",
            font=("Arial-BoldMT", int(13.0)), anchor="w"
        )
        self.canvas.create_text(
            430.0, 30.0,
            text="Spell",
            font=("Arial-BoldMT", int(13.0)), anchor="w"
        )
        self.canvas.create_text(
            540.0, 30.0,
            text="Mean",
            font=("Arial-BoldMT", int(13.0)), anchor="w"
        )
        self.canvas.create_text(
            634.0, 30.0,
            text="Difficulty",
            font=("Arial-BoldMT", int(13.0)), anchor="w"
        )
        self.SpellInput = tk.Entry()
        self.SpellInput.place(x=90, y=170, width=250, height=30)
        self.canvas.create_text(
            12.0, 235.0,
            text="뜻 :",
            font=("Arial-BoldMT", int(13.0)), anchor="w"
        )
        self.MeanInput = tk.Entry()
        self.MeanInput.place(x=90, y=223, width=250, height=30)
        self.canvas.create_text(
            12.0, 288.0,
            text="난이도 :",
            font=("Arial-BoldMT", int(13.0)), anchor="w"
        )
        self.DifficultyInput = tk.Entry()
        self.DifficultyInput.place(x=90, y=276, width=250, height=30)

        # 텍스트 위젯 생성
        self.TextWidget = tk.Text(self)

        # 스크롤바 생성
        self.scrollbar = tk.Scrollbar(self, command=self.TextWidget.yview)
        self.scrollbar.pack(side="right", fill="y")

        # 스크롤바와 텍스트 위젯 연결
        self.TextWidget.config(yscrollcommand=self.scrollbar.set)

        self.resizable(False, False)
        
    
    def ListEntireWords(self):
        # 기존 버튼 제거
        for SpellButton, MeanButton, DiffiButton in zip(self.SpellButtons, self.MeanButtons, self.DiffiButtons):
                SpellButton.destroy()
                MeanButton.destroy()
                DiffiButton.destroy()
        self.SpellButtons.clear()
        self.MeanButtons.clear()
        self.DiffiButtons.clear()

        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SELECT word_id, Spell, Mean, Difficulty FROM toeicword")  # id만 가져오도록 수정
            EntireWordInfos = cursor.fetchall()
            if len(EntireWordInfos)==0:
                    messagebox.showinfo("검색 결과 없음", "검색 결과가 없습니다.")
                    return
            yGap = 30
            yPos = 44
            for index, WordInfo in enumerate(EntireWordInfos):
                    SpellButton = tk.Button(self, text=f"{WordInfo[1]}", command=lambda i=index: self.WordButtonClick(i))
                    MeanButton = tk.Button(self, text=f"{WordInfo[2]}", command=lambda i=index: self.WordButtonClick(i))
                    DiffiButton = tk.Button(self, text=f"{WordInfo[3]}", command=lambda i=index: self.WordButtonClick(i))
                    
                    SpellButton.place(x=393, y=yPos, width=111, height=30)
                    
                    SpellButton.pack()
                    SpellButton.place(x=393, y=yPos, width=111, height=30)
                    
                    MeanButton.pack()
                    MeanButton.place(x=504, y=yPos, width=111, height=30)
                    
                    DiffiButton.pack()
                    DiffiButton.place(x=615, y=yPos, width=111, height=30)
                    yPos += yGap
                    self.SpellButtons.append(SpellButton)
                    self.MeanButtons.append(MeanButton)
                    self.DiffiButtons.append(DiffiButton)
                    

    def ListSpecificWords(self):
        # 기존 버튼 제거
        SearchWord = self.SearchWordInput.get()
        if(len(SearchWord) ==0):
            messagebox.showinfo("검색 오류", "입력이 올바르게 되지 않았습니다. 다시 시도해주세요.")
        else:
        
            for SpellButton, MeanButton, DiffiButton in zip(self.SpellButtons, self.MeanButtons, self.DiffiButtons):
                SpellButton.destroy()
                MeanButton.destroy()
                DiffiButton.destroy()

            self.SpellButtons.clear()
            self.MeanButtons.clear()
            self.DiffiButtons.clear()
            
            yGap = 30
            yPos = 44
            if self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT word_id, Spell, Mean, Difficulty FROM toeicword WHERE Spell LIKE %s", ('%' + SearchWord + '%',))
                SpecificWordInfos = cursor.fetchall()
                if len(SpecificWordInfos)==0:
                    messagebox.showinfo("검색 결과 없음", "검색 결과가 없습니다.")
                for index, WordInfo in enumerate(SpecificWordInfos):
                    SpellButton = tk.Button(self, text=f"{WordInfo[1]}", command=lambda i=index: self.WordButtonClick(i))
                    MeanButton = tk.Button(self, text=f"{WordInfo[2]}", command=lambda i=index: self.WordButtonClick(i))
                    DiffiButton = tk.Button(self, text=f"{WordInfo[3]}", command=lambda i=index: self.WordButtonClick(i))
                    
                    SpellButton.pack()
                    SpellButton.place(x=393, y=yPos, width=111, height=30)
                    
                    MeanButton.pack()
                    MeanButton.place(x=504, y=yPos, width=111, height=30)
                    
                    DiffiButton.pack()
                    DiffiButton.place(x=615, y=yPos, width=111, height=30)
                    yPos += yGap

                    self.SpellButtons.append(SpellButton)
                    self.MeanButtons.append(MeanButton)
                    self.DiffiButtons.append(DiffiButton)
                    
    def InsertWord(self):
        MaxLength = 40
        spell = self.SpellInput.get()
        mean = self.MeanInput.get()
        difficulty = self.DifficultyInput.get()
        if(len(spell) > 0 and len(mean) > 0 and len(difficulty) >0):
            now = datetime.now()
            message = f"{self.adminID}님이 {spell} 단어를 추가하셨습니다."
            if self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT MAX(Day) from toeicword");
                day = cursor.fetchone()[0]
                cursor.execute("SELECT * from toeicword where Day = %s",(day,));
                DayLength = len(cursor.fetchall())
                if DayLength >= MaxLength:
                    day += 1
                cursor.execute("INSERT INTO toeicword(Day, Spell, Mean, Difficulty) VALUES (%s,%s, %s, %s)", (day, spell, mean, difficulty))
                cursor.execute("INSERT INTO history(admin, log, changetime) VALUES (%s, %s, %s)", (self.adminID, message, now))
                self.connection.commit()
                cursor.close()  # 커서 닫기
                messagebox.showinfo("단어 추가 성공", "단어가 성공적으로 추가되었습니다.")
        else:
                messagebox.showinfo("단어 정보 누락", "단어 정보에 빠진 값이 없는지 확인해주세요.")  
                
    def DeleteWord(self):
        spell = self.SpellInput.get()
        mean = self.MeanInput.get()
        difficulty = self.DifficultyInput.get()
        if(len(spell) > 0 and len(mean) > 0 and len(difficulty) >0):
            now = datetime.now()
            message = f"{self.adminID}님이 {spell} 단어를 삭제하셨습니다."
            if self.connection:
                cursor = self.connection.cursor()
                cursor.execute("DELETE FROM toeicword WHERE Spell = %s AND Mean = %s AND Difficulty = %s", (spell, mean, difficulty))
                cursor.execute("INSERT INTO history(admin, log, changetime) VALUES (%s, %s, %s)", (self.adminID, message, now))
                self.connection.commit()  # 커밋을 수행하여 변경 사항을 DB에 적용
                cursor.close()  # 커서 닫기  
                messagebox.showinfo("단어 삭제 성공", "단어가 성공적으로 삭제되었습니다.")
                self.SearchWordInput.delete(0, tk.END)
                self.SpellInput.delete(0,tk.END)
                self.MeanInput.delete(0,tk.END)
                self.DifficultyInput.delete(0,tk.END)
                for i in range(3):
                            self.PrevInfos.pop()
        else:
                messagebox.showinfo("단어 정보 누락", "단어 정보에 빠진 값이 없는지 확인해주세요.")   
    def UpdateWord(self):
        spell = self.SpellInput.get()
        mean = self.MeanInput.get()
        difficulty = self.DifficultyInput.get()
        if(len(spell) > 0 and len(mean) > 0 and len(difficulty) >0):
            now = datetime.now()
            message = f"{self.adminID}님이 {spell} 단어를 수정하셨습니다."
            if self.connection:
                cursor = self.connection.cursor()
                cursor.execute("UPDATE toeicword SET Spell = %s, Mean = %s, Difficulty = %s WHERE Spell = %s AND Mean = %s AND Difficulty = %s", (spell, mean, difficulty, self.PrevInfos[0], self.PrevInfos[1],self.PrevInfos[2]))
                cursor.execute("INSERT INTO history(admin, log, changetime) VALUES (%s, %s, %s)", (self.adminID, message, now))
                self.connection.commit()  # 커밋을 수행하여 변경 사항을 DB에 적용
                cursor.close()  # 커서 닫기
                
                messagebox.showinfo("단어 수정 성공", "단어가 성공적으로 수정되었습니다.")
                self.SearchWordInput.delete(0,tk.END)
                self.SpellInput.delete(0,tk.END)
                self.MeanInput.delete(0,tk.END)
                self.DifficultyInput.delete(0,tk.END)        
                for i in range(3):
                            self.PrevInfos.pop()
        else:
            messagebox.showinfo("단어 정보 누락", "단어 정보에 빠진 값이 없는지 확인해주세요.")
    def WordButtonClick(self, index):
        for i in range(len(self.SpellButtons)):  # 모든 행에 대해 반복
            if i == index:  # 현재 클릭된 버튼과 같은 행의 버튼들만
                self.SpellButtons[i].configure(bg="skyblue")  # 다른 행의 버튼은 기본 색상으로 변경
                self.MeanButtons[i].configure(bg="skyblue")
                self.DiffiButtons[i].configure(bg="skyblue")
                
                self.SpellInput.delete(0,tk.END)
                self.SpellInput.insert(0,self.SpellButtons[i].cget("text"))
                self.MeanInput.delete(0,tk.END)
                self.MeanInput.insert(0,self.MeanButtons[i].cget("text"))
                self.DifficultyInput.delete(0,tk.END)
                self.DifficultyInput.insert(0,self.DiffiButtons[i].cget("text"))
                
                self.PrevInfos.append(self.SpellButtons[i].cget("text"))
                self.PrevInfos.append(self.MeanButtons[i].cget("text"))
                self.PrevInfos.append(self.DiffiButtons[i].cget("text"))
                
            else:
                self.SpellButtons[i].configure(bg="SystemButtonFace")  # 다른 행의 버튼은 기본 색상으로 변경
                self.MeanButtons[i].configure(bg="SystemButtonFace")
                self.DiffiButtons[i].configure(bg="SystemButtonFace")
    def SwitchToAdminMainPage(self):
            from AdminMainPage import AdminMainPage
            self.destroy()    
            app = AdminMainPage(self.adminID)
            app.mainloop()
if __name__ == "__main__":
    adminID = sys.argv[1] if len(sys.argv) > 1 else 'default_user'
    app = AdminWordManagePage(adminID)
    app.mainloop()
