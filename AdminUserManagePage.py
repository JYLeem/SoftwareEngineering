from mysql.connector import Error
from tkinter import Tk, Canvas, Scrollbar, messagebox
import tkinter as tk 
import importlib
import sys
from Util import Util

class AdminUserManagePage(tk.Tk):
    def __init__(self, adminID):
        super().__init__()
        self.adminID = adminID
        self.UserButtons = []
        self.title("회원 관리 페이지")
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

        self.UserInput = tk.Entry()
        self.UserInput.place(x=28, y=102, width=200, height=40)

        self.UserSearchBtn = tk.Button(text="회원조회", command=self.ListSpecificUsers)
        self.UserSearchBtn.place(x=250, y=102, width=100, height=40)

        self.UserDeleteBtn = tk.Button(text="선택 회원 삭제", command=self.DeleteUser)
        self.UserDeleteBtn.place(x=187, y=193, width=150, height=40)

        self.UserDeleteBtn = tk.Button(text="전체 회원 조회", command=self.ListEntireUsers)  # 수정된 부분
        self.UserDeleteBtn.place(x=28, y=193, width=150, height=40)

        self.TextWidget = tk.Text()
        self.scrollbar = tk.Scrollbar(self, command=self.TextWidget.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.GoHomeBtn = tk.Button(text="이전으로", command=self.SwitchToAdminMainPage)
        self.GoHomeBtn.place(x=15, y=483, width=90, height=40)

        self.canvas.create_rectangle(
            450.0,
            45.0,
            700.0,
            525.0,
            fill="#FFFFFF",
            outline="black"
        )

        self.resizable(False, False)
        self.connection = Util.ConnectMysql()

    def ListEntireUsers(self):
        # 기존 버튼 제거
        for self.UserButton in self.UserButtons:
            self.UserButton.destroy()
        self.UserButtons.clear()
        
        self.gap = 30
        self.yBefore = 29
        if self.connection:
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT nickname FROM user")  # id만 가져오도록 수정
            self.EntireUserNicknames = self.cursor.fetchall()
            for index, UserNickname in enumerate(self.EntireUserNicknames):
                self.UserButton = tk.Button(text=f"{UserNickname[0]}", command=lambda i=index: self.UserButtonClick(i))
                self.yBefore += self.gap
                self.UserButton.pack()
                self.UserButton.place(x=500, y=self.yBefore+self.gap, width=150, height=30)
                self.UserButtons.append(self.UserButton)

    def ListSpecificUsers(self):
        # 기존 버튼 제거
        self.SearchUser = self.UserInput.get()
        if(len(self.SearchUser) ==0):
            messagebox.showinfo("검색 오류", "입력이 올바르게 되지 않았습니다. 다시 시도해주세요.")
        else:
            for UserButton in self.UserButtons:
                UserButton.destroy()
            self.UserButtons.clear()

            self.gap = 30
            self.yBefore = 29
            if self.connection:
                self.cursor = self.connection.cursor()
                self.cursor.execute("SELECT nickname FROM user WHERE nickname LIKE %s", ('%' + self.SearchUser + '%',))
                self.SpecificUserNicknames = self.cursor.fetchall()
                if(len(self.SpecificUserNicknames) == 0):
                    messagebox.showinfo("검색 오류", "해당 사용자 정보가 없습니다.")
                
                for index, UserNickname in enumerate(self.SpecificUserNicknames):
                    self.UserButton = tk.Button(text=f"{UserNickname[0]}", command=lambda i=index: self.UserButtonClick(i))
                    self.yBefore += self.gap
                    self.UserButton.pack()
                    self.UserButton.place(x=500, y=self.yBefore+self.gap, width=150, height=30)
                    self.UserButtons.append(self.UserButton)
    def UserButtonClick(self, index):
        for i in range(len(self.UserButtons)):
            if i == index: 
                self.UserButtons[i].configure(bg="skyblue")
                self.UserInput.delete(0,tk.END)
                self.UserInput.insert(0,self.UserButtons[i].cget("text"))
            else:
                self.UserButtons[i].configure(bg="SystemButtonFace")
    def DeleteUser(self):
        UserDelete = self.UserInput.get()
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM user WHERE nickname = %s", (UserDelete,))
            self.connection.commit()  # 커밋을 수행하여 변경 사항을 DB에 적용
            cursor.close()  # 커서 닫기  
            messagebox.showinfo("사용자 정보 삭제 성공", "사용자 정보가 성공적으로 삭제되었습니다.")
            self.UserInput.delete(0, tk.END)
        
    
    def SwitchToAdminMainPage(self):
        from AdminMainPage import AdminMainPage
        self.destroy()    
        app = AdminMainPage(self.adminID)
        app.mainloop()
if __name__ == "__main__":
    adminID = sys.argv[1] if len(sys.argv) > 1 else 'default_user'
    app = AdminUserManagePage(adminID)
    app.mainloop()