import mysql.connector
from mysql.connector import Error
import sys
import subprocess
from tkinter import Tk, Canvas
import tkinter as tk
class Util:
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
    
    def SwitchPage(window, PageName, id=None):
        window.destroy()
        if id is None:
            subprocess.run(['python', '%s.py' % PageName])
        else:
            subprocess.run(['python', '%s.py' % PageName, id])
    
