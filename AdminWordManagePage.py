import mysql.connector
from mysql.connector import Error
from datetime import datetime
from tkinter import Tk, Canvas, messagebox, Frame, Button
import tkinter as tk
import sys
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

        self.current_page = 0  # 현재 페이지를 트래킹하는 변수
        self.words_per_page = 13  # 페이지당 단어 수

        self.title("단어 관리 페이지")
        self.geometry("747x531")
        self.configure(bg="#FFFFFF")

        self.canvas = tk.Canvas(
            self,
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

        self.SearchInfoInput = tk.Entry()
        self.SearchInfoInput.place(x=32, y=103, width=200, height=40)

        self.SearchInfoBtn = tk.Button(text="단어 검색", command=self.ListSpecificWords)
        self.SearchInfoBtn.place(x=240, y=103, width=100, height=40)

        self.UpdateWordBtn = tk.Button(text="단어 수정", command=self.UpdateWord)
        self.UpdateWordBtn.place(x=143, y=361, width=90, height=40)

        self.DeleteWordBtn = tk.Button(text="단어 삭제", command=self.DeleteWord)
        self.DeleteWordBtn.place(x=37, y=361, width=90, height=40)

        self.InsertWordBtn = tk.Button(text="단어 추가", command=self.InsertWord)
        self.InsertWordBtn.place(x=249, y=361, width=90, height=40)

        self.GoHomeBtn = tk.Button(text="이전으로", command=self.SwitchToAdminMainPage)
        self.GoHomeBtn.place(x=15, y=483, width=90, height=40)

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

        # 단어 출력 부분
        self.word_frame = tk.Frame(self)
        self.word_frame.place(x=388, y=44, width=340, height=400)

        self.next_button = tk.Button(self, text="다음", command=self.NextPage)
        self.next_button.place(x=648, y=460, width=80, height=30)
        self.prev_button = tk.Button(self, text="이전", command=self.PrevPage)
        self.prev_button.place(x=548, y=460, width=80, height=30)

        self.resizable(False, False)

    def ListEntireWords(self):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SELECT word_id, Spell, Mean, Difficulty FROM toeicword")
            self.WordInfos = cursor.fetchall()
            self.current_page = 0
            self.ShowPage()

    def ListSpecificWords(self):
        SearchInfo = self.SearchInfoInput.get()
        if len(SearchInfo) == 0:
            messagebox.showinfo("검색 오류", "입력이 올바르게 되지 않았습니다. 다시 시도해주세요.")
        else:
            if self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT word_id, Spell, Mean, Difficulty FROM toeicword WHERE Spell LIKE %s OR Mean LIKE %s OR Difficulty LIKE %s", ('%' + SearchInfo + '%', '%' + SearchInfo + '%', '%' + SearchInfo + '%',))
                self.WordInfos = cursor.fetchall()
                if len(self.WordInfos)==0:
                    messagebox.showinfo("검색 결과 없음", "검색 결과가 없습니다.")
                self.current_page = 0
                self.ShowPage()

    def ShowPage(self):
        for widget in self.word_frame.winfo_children():
            widget.destroy()

        start_idx = self.current_page * self.words_per_page
        end_idx = start_idx + self.words_per_page

        for WordInfo in self.WordInfos[start_idx:end_idx]:
            frame = tk.Frame(self.word_frame)
            frame.pack(fill='x', padx=5, pady=2)
            SpellButton = tk.Button(frame, text=f"{WordInfo[1]}", command=lambda wi=WordInfo: self.WordButtonClick(wi), width=14)
            MeanButton = tk.Button(frame, text=f"{WordInfo[2]}", command=lambda wi=WordInfo: self.WordButtonClick(wi), width=14)
            DiffiButton = tk.Button(frame, text=f"{WordInfo[3]}", command=lambda wi=WordInfo: self.WordButtonClick(wi), width=14)

            SpellButton.pack(side='left', fill='x', expand=True)
            MeanButton.pack(side='left', fill='x', expand=True)
            DiffiButton.pack(side='left', fill='x', expand=True)

            self.SpellButtons.append(SpellButton)
            self.MeanButtons.append(MeanButton)
            self.DiffiButtons.append(DiffiButton)

        self.next_button.config(state=tk.NORMAL if end_idx < len(self.WordInfos) else tk.DISABLED)
        self.prev_button.config(state=tk.NORMAL if self.current_page > 0 else tk.DISABLED)

    def NextPage(self):
        self.current_page += 1
        self.ShowPage()

    def PrevPage(self):
        self.current_page -= 1
        self.ShowPage()

    def InsertWord(self):
        MaxWordNum = 40
        spell = self.SpellInput.get()
        mean = self.MeanInput.get()
        difficulty = self.DifficultyInput.get()
        now = datetime.now()
        message = f"{self.adminID}님이 {spell} 단어를 추가하셨습니다."
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SELECT MAX(Day) from toeicword");
            day = cursor.fetchone()[0]
            cursor.execute("SELECT * from toeicword where Day = %s",(day,));
            WordNum = len(cursor.fetchall())
            if WordNum >= MaxWordNum:
                day += 1
            cursor.execute("INSERT INTO toeicword(Day, Spell, Mean, Difficulty) VALUES (%s,%s, %s, %s)", (day, spell, mean, difficulty))
            cursor.execute("INSERT INTO history(admin, log, changetime) VALUES (%s, %s, %s)", (self.adminID, message, now))
            self.connection.commit()
            cursor.close()  # 커서 닫기
            messagebox.showinfo("단어 추가 성공", "단어가 성공적으로 추가되었습니다.")
            self.SearchInfoInput.delete(0, tk.END)
            self.SpellInput.delete(0, tk.END)
            self.MeanInput.delete(0, tk.END)
            self.DifficultyInput.delete(0, tk.END)
            for i in range(3):
                self.PrevInfos.pop()
    def DeleteWord(self):
        spell = self.SpellInput.get()
        mean = self.MeanInput.get()
        difficulty = self.DifficultyInput.get()
        now = datetime.now()
        message = f"{self.adminID}님이 {spell} 단어를 삭제하셨습니다."
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM toeicword WHERE Spell = %s AND Mean = %s AND Difficulty = %s", (spell, mean, difficulty))
            cursor.execute("INSERT INTO history(admin, log, changetime) VALUES (%s, %s, %s)", (self.adminID, message, now))
            self.connection.commit()  # 커밋을 수행하여 변경 사항을 DB에 적용
            cursor.close()  # 커서 닫기
            messagebox.showinfo("단어 삭제 성공", "단어가 성공적으로 삭제되었습니다.")
            self.SearchInfoInput.delete(0, tk.END)
            self.SpellInput.delete(0, tk.END)
            self.MeanInput.delete(0, tk.END)
            self.DifficultyInput.delete(0, tk.END)
            for i in range(3):
                self.PrevInfos.pop()

    def UpdateWord(self):
        spell = self.SpellInput.get()
        mean = self.MeanInput.get()
        difficulty = self.DifficultyInput.get()
        now = datetime.now()
        message = f"{self.adminID}님이 {spell} 단어를 수정하셨습니다."
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE toeicword SET Spell = %s, Mean = %s, Difficulty = %s WHERE Spell = %s AND Mean = %s AND Difficulty = %s", (spell, mean, difficulty, self.PrevInfos[0], self.PrevInfos[1], self.PrevInfos[2]))
            cursor.execute("INSERT INTO history(admin, log, changetime) VALUES (%s, %s, %s)", (self.adminID, message, now))
            self.connection.commit()  # 커밋을 수행하여 변경 사항을 DB에 적용
            cursor.close()  # 커서 닫기

            messagebox.showinfo("단어 수정 성공", "단어가 성공적으로 수정되었습니다.")
            self.SearchInfoInput.delete(0, tk.END)
            self.SpellInput.delete(0, tk.END)
            self.MeanInput.delete(0, tk.END)
            self.DifficultyInput.delete(0, tk.END)
            for i in range(3):
                self.PrevInfos.pop()

    def WordButtonClick(self, WordInfo):
        self.SpellInput.delete(0, tk.END)
        self.SpellInput.insert(0, WordInfo[1])
        self.MeanInput.delete(0, tk.END)
        self.MeanInput.insert(0, WordInfo[2])
        self.DifficultyInput.delete(0, tk.END)
        self.DifficultyInput.insert(0, WordInfo[3])

        self.PrevInfos = [WordInfo[1], WordInfo[2], WordInfo[3]]

    def SwitchToAdminMainPage(self):
        from AdminMainPage import AdminMainPage
        self.destroy()
        app = AdminMainPage(self.adminID)
        app.mainloop()

if __name__ == "__main__":
    adminID = sys.argv[1] if len(sys.argv) > 1 else 'default_user'
    app = AdminWordManagePage(adminID)
    app.mainloop()
