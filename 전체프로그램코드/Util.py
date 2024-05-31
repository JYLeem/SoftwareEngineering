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
    def OnClosing(connection, userid):
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute("UPDATE user SET isaccess = 0 WHERE id = %s", (userid,))
            connection.commit()
            cursor.close()