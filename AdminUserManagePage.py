from mysql.connector import Error
from tkinter import Tk, Canvas, messagebox, Frame, Button
import tkinter as tk
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
            self,
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

        self.ListEntireUsersBtn = tk.Button(text="전체 회원 조회", command=self.ListEntireUsers)
        self.ListEntireUsersBtn.place(x=28, y=193, width=150, height=40)

        self.user_frame = tk.Frame(self)
        self.user_frame.place(x=450, y=45, width=250, height=430)

        self.NextPageBtn = tk.Button(text="다음", command=lambda: self.ShowPage(self.current_page + 1))
        self.NextPageBtn.place(x=640, y=490, width=60, height=30)
        self.PrevPageBtn = tk.Button(text="이전", command=lambda: self.ShowPage(self.current_page - 1))
        self.PrevPageBtn.place(x=570, y=490, width=60, height=30)

        self.resizable(False, False)
        self.connection = Util.ConnectMysql()
        
        self.GoHomeBtn = tk.Button(text="이전으로", command=self.SwitchToAdminMainPage)
        self.GoHomeBtn.place(x=15, y=483, width=90, height=40)

        self.current_page = 0  # 현재 페이지를 트래킹하는 변수
        self.users_per_page = 13  # 페이지당 유저 수
        
    def SwitchToAdminMainPage(self):
        from AdminMainPage import AdminMainPage
        self.destroy()
        app = AdminMainPage(self.adminID)
        app.mainloop()

    def ShowPage(self, page):
        # 페이지 전환을 처리하는 함수
        if page < 0 or (self.EntireUserNicknames and page * self.users_per_page >= len(self.EntireUserNicknames)):
            return

        self.current_page = page

        for widget in self.user_frame.winfo_children():
            widget.destroy()

        start = self.current_page * self.users_per_page
        end = start + self.users_per_page

        frame_width = self.user_frame.winfo_width()
        button_width = int(frame_width * 0.8)

        for index, UserNickname in enumerate(self.EntireUserNicknames[start:end]):
            UserButton = tk.Button(self.user_frame, text=f"{UserNickname[0]}", command=lambda i=index: self.UserButtonClick(i), width=button_width)
            UserButton.pack(pady=2, padx=(frame_width - button_width) // 2)
            self.UserButtons.append(UserButton)

    def ListEntireUsers(self):
        # 기존 버튼 제거
        for UserButton in self.UserButtons:
            UserButton.destroy()
        self.UserButtons.clear()

        if self.connection:
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT nickname FROM user")
            self.EntireUserNicknames = self.cursor.fetchall()
            self.ShowPage(0)

    def ListSpecificUsers(self):
        # 기존 버튼 제거
        SearchUser = self.UserInput.get()
        if not SearchUser:
            messagebox.showinfo("검색 오류", "입력이 올바르게 되지 않았습니다. 다시 시도해주세요.")
            return
        
        for UserButton in self.UserButtons:
            UserButton.destroy()
        self.UserButtons.clear()

        if self.connection:
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT nickname FROM user WHERE nickname LIKE %s", ('%' + SearchUser + '%',))
            self.EntireUserNicknames = self.cursor.fetchall()
            if not self.EntireUserNicknames:
                messagebox.showinfo("검색 오류", "해당 사용자 정보가 없습니다.")
                return
            self.ShowPage(0)

    def UserButtonClick(self, index):
        self.UserInput.delete(0, tk.END)
        self.UserInput.insert(0, self.UserButtons[index].cget("text"))

    def DeleteUser(self):
        UserDelete = self.UserInput.get()
        if not UserDelete:
            messagebox.showinfo("삭제 오류", "삭제할 회원을 입력해주세요.")
            return

        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM user WHERE nickname = %s", (UserDelete,))
            self.connection.commit()
            cursor.close()
            messagebox.showinfo("사용자 정보 삭제 성공", "사용자 정보가 성공적으로 삭제되었습니다.")
            self.UserInput.delete(0, tk.END)
            self.ListEntireUsers()

    def SwitchToAdminMainPage(self):
        from AdminMainPage import AdminMainPage
        self.destroy()
        app = AdminMainPage(self.adminID)
        app.mainloop()

if __name__ == "__main__":
    adminID = sys.argv[1] if len(sys.argv) > 1 else 'default_user'
    app = AdminUserManagePage(adminID)
    app.mainloop()

