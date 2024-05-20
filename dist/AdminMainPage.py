import sys
import tkinter as tk
from tkinter import ttk  # 추가
from Util import Util

class AdminMainPage(tk.Tk):
    def __init__(self, adminID):
        super().__init__()
        self.geometry("747x531")
        self.title("관리자 메인 페이지")
        self.configure(bg="#FFFFFF")
        self.adminID = adminID
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
        self.AdminIDLabel = tk.Label(self, text=adminID)
        self.AdminIDLabel.place(x=300, y=0, width=100, height=30)
        self.ManageWordBtn = tk.Button(text="단어 관리", command=self.SwitchToAdminWordManagePage)
        self.ManageWordBtn.place(x=400, y=0, width=100, height=30)
        self.ManageUserBtn = tk.Button(text="유저 관리", command=self.SwitchToAdminUserManagePage)
        self.ManageUserBtn.place(x=500, y=0, width=100, height=30)
        self.LogOutBtn = tk.Button(text="로그아웃", command=self.SwitchToLoginPage)
        self.LogOutBtn.place(x=600, y=0, width=100, height=30)
        self.canvas.create_rectangle(
            10.0,
            50.0,
            230.0,
            300.0,
            fill="#FFFFFF",
            outline="#000000"
        )
        self.canvas.create_text(
            85.0, 60.0,
            text="단어 현황",
            font=("Arial-BoldMT", int(13.0)), anchor="w"
        )
        self.canvas.create_text(
            50.0, 320.0,
            text="최근 활동",
            font=("Arial-BoldMT", int(13.0)), anchor="w"
        )
        
        # 스크롤바와 캔버스 추가
        self.log_frame = tk.Frame(self)
        self.log_frame.place(x=10, y=330, width=680, height=190)
        
        self.log_canvas = tk.Canvas(self.log_frame, bg="#FFFFFF")
        self.scrollbar = ttk.Scrollbar(self.log_frame, orient="vertical", command=self.log_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.log_canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.log_canvas.configure(
                scrollregion=self.log_canvas.bbox("all")
            )
        )

        self.log_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.log_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.log_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.create_rectangle(
            240.0,
            50.0,
            460.0,
            300.0,
            fill="#FFFFFF",
            outline="#000000"
        )
        self.canvas.create_text(
            315.0, 60.0,
            text="유저 현황",
            font=("Arial-BoldMT", int(13.0)), anchor="w"
        )
        
        self.canvas.create_rectangle(
            470.0,
            50.0,
            690.0,
            300.0,
            fill="#FFFFFF",
            outline="#000000"
        )
        self.canvas.create_text(
            515.0, 60.0,
            text="현재 접속자 수",
            font=("Arial-BoldMT", int(13.0)), anchor="w"
        )
        self.DisplayStatus()
        self.resizable(False, False)

    def DisplayStatus(self):
        connection = Util.ConnectMysql()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT Spell from toeicword")
            NumWords = cursor.fetchall()
            cursor.execute("SELECT id from user")
            NumUsers = cursor.fetchall()
            cursor.execute("SELECT isaccess from user where isaccess = 1")
            NumAccesses = cursor.fetchall()
            self.canvas.create_text(
                100.0, 175.0,
                text=f"{len(NumWords)}",
                font=("Arial-BoldMT", int(13.0)), anchor="w"
            )
            self.canvas.create_text(
                330.0, 175.0,
                text=f"{len(NumUsers)}",
                font=("Arial-BoldMT", int(13.0)), anchor="w"
            )
            self.canvas.create_text(
                560.0, 175.0,
                text=f"{len(NumAccesses)}",
                font=("Arial-BoldMT", int(13.0)), anchor="w"
            )
            cursor.execute("SELECT admin, log, changetime from history")
            ChangeHistorys = cursor.fetchall()
            for index, ChangeHistory in enumerate(ChangeHistorys):
                content = f"{ChangeHistory[2]} {ChangeHistory[1]}"
                CHLabel = tk.Label(self.scrollable_frame, text=content, bg="white", justify="left", anchor="w")
                CHLabel.pack(fill="x")

    def SwitchToAdminWordManagePage(self):
        from AdminWordManagePage import AdminWordManagePage
        self.destroy()
        app = AdminWordManagePage(self.adminID)
        app.mainloop()

    def SwitchToAdminUserManagePage(self):
        from AdminUserManagePage import AdminUserManagePage
        self.destroy()
        app = AdminUserManagePage(self.adminID)
        app.mainloop()

    def SwitchToLoginPage(self):
        from LoginPage import LoginPage
        self.destroy()
        app = LoginPage()
        app.mainloop()

if __name__ == "__main__":
    adminID = sys.argv[1] if len(sys.argv) > 1 else 'default_user'
    app = AdminMainPage(adminID)
    app.mainloop()
