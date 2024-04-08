from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import tkinter as tk
import subprocess


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

def go_adminpage_user():
    window.destroy()
    subprocess.run(['python', 'AdminPage_user.py'])
    
canvas.place(x = 0, y = 0)

manage_words_btn = tk.Button(text = "단어 관리")
manage_words_btn.place(x=283, y=98, width=180, height=80)

manage_users_btn = tk.Button(text="유저 관리", command=go_adminpage_user)
manage_users_btn.place(x=283, y=231, width=180, height=80)

logout_btn = tk.Button(text = "로그아웃")
logout_btn.place(x=283, y=364, width=180, height=80)




window.resizable(False, False)
window.mainloop()
