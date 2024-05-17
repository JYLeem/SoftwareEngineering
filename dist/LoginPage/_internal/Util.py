import mysql.connector
from mysql.connector import Error
import sys
import subprocess
from tkinter import Tk, Canvas
import tkinter as tk

class Util:
    @staticmethod
    def ConnectMysql():
        try:
            connection = mysql.connector.connect(host='ystdb.cl260eouqhjz.ap-northeast-2.rds.amazonaws.com',
                                                    database='wordbook',
                                                    user='admin',
                                                    password='seat0323')
            if connection.is_connected():
                return connection
        except Error as e:
            print("MySQL에 연결하는 동안 오류 발생:", e)  
    
    @staticmethod
    def SwitchPage(window, PageName, id=None):
        # 현재 프로세스를 실행하여 subprocess.Popen 객체로 저장
        process = None
        if id is None:
            process = subprocess.Popen(['python', '%s.py' % PageName])
        else:
            process = subprocess.Popen(['python', '%s.py' % PageName, id])

        # 이전 페이지를 종료하지 않고 현재 페이지를 숨김
        window.withdraw()

        # subprocess.Popen 객체 반환
        return process