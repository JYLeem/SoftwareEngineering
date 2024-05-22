import tkinter as tk
from tkinter import font

# 새로운 Tkinter 윈도우 생성
root = tk.Tk()

# 시스템에 설치된 모든 폰트 목록 출력
print(font.families())

# Tkinter 윈도우 종료
root.destroy()