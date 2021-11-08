
"""when it is in test mode, use app instead of .app."""
"""When running the app, use app instead of app."""

from functools import partial
from tkinter import *
import tkinter as tk
import requests
import json
import pandas as pd
from requests.auth import HTTPBasicAuth


def auth_api(username, password):
    res = requests.get('https://api.quickbutik.com/v1/products', auth=HTTPBasicAuth(username.get(), password.get()))
    print(res.status_code)
    if res.status_code == 200:
        Label(window, text="Login successfully.").pack()
        # Open file function
        #openFile()
    elif res.status_code == 401:
        Label(window, text="Wrong API key.").pack()
    else:
        Label(window, text="Other errors.").pack()


def login():
    global window1
    window1 = Toplevel(window)
    window1.title("Upload csv file to create products.")
    window1.geometry("300x250")



def main_window():
    global window
    window = tk.Tk()
    window.geometry("300x250")
    window.title("Minikit")
    Label(text="Minikit 2.0", bg="grey", width="300", height="2", font=('Calibri', 13)).pack()
    #Button(text="API login", height="2", width="30", command=login).pack()
    userName = StringVar()
    passWord = StringVar()
    Label(window, text="Enter your api key below").pack()
    Label(window, text="User name").pack()
    Entry(window, textvariable= userName).pack()
    Label(window, text="Password").pack()
    Entry(window, textvariable=passWord).pack()
    validateLogin = partial(auth_api, userName, passWord)
    Button(window, text="Log in", width=10, height=1, command=validateLogin).pack()


if __name__== "__main__":
    main_window()
    window.mainloop()

#userName = input("Your user name?")
#passWord = input("Your password:")
#auth_api(userName, passWord)