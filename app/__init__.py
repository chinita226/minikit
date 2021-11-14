
"""when it is in test mode, use app instead of .app."""
"""When running the app, use app instead of app."""

from functools import partial
from os import PathLike
from tkinter import *
from tkinter import filedialog
import os
import tkinter as tk
import requests
import json
import csv
import pandas as pd
from requests.auth import HTTPBasicAuth


def auth_api(username, password):
    """Auth function to validate API."""

    res = requests.get('https://api.quickbutik.com/v1/products', auth=HTTPBasicAuth(username.get(), password.get()))
    print(res.status_code)
    if res.status_code == 200:
        Label(window, text="Login successfully.").pack()
        path_window()
    elif res.status_code == 401:
        Label(window, text="Wrong API key.").pack()
    else:
        Label(window, text="Other errors.").pack()


def csv_to_json(csvFile, jsonPath):
    """Get csv file and export to json."""
    global jsonArray
    jsonArray = []

    try:    
        if(csvFile.endswith('.csv')): 
            with open(csvFile,'r', encoding='UTF-8') as csvf: 
                csvReader = csv.DictReader(csvf) 

                for row in csvReader: 
                    jsonArray.append(row)
        else:
            Label(window, text="Error! Make sure your file is type CSV").pack()
        if os.path.exists(jsonPath): 
            Label(window, text="File already exists")
        
        elif(jsonPath.endswith('.json')):
            with open(jsonPath, 'w', encoding='UTF-8') as jsonf:
            
                jsonString = json.dumps(jsonArray, ensure_ascii= False, indent=4)
                jsonf.write(jsonString)
                Label(window, text="File created!").pack()

        else:
            Label(window, text="An error has occured").pack()
            Label(window, text="Make sure that your file name contains .json").pack()
      
    except IOError:
        print("File not accessible")


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


def browseFiles(label_file_explorer):
    browseFiles.filename = filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = (("CSV file", "*.csv*"),("all files","*.*")))
    
    label_file_explorer.configure(text = browseFiles.filename)


def path_window():
    global window1
    jsonFile = str
    window1 = Toplevel(window)
    window1.title('File Explorer')
    window1.geometry("300x300")
    window1.title("Minikit")

    Label(window1, text="Minikit 2.0", bg="grey", width="300", height="2", font=('Calibri', 13)).pack()
    Label(window1, text = "Browse to find your csv file", width = 100, height = 1,fg = "black").pack()
    label_file_explorer = Label(window1, text = "Name of file", width=100, height= 2, fg = "black")
    label_file_explorer.pack()
    Button(window1, text = "Browse Files", command = lambda: browseFiles(label_file_explorer)).pack()
    Label(window1, text = "Enter name for json file, must end with .json", width = 100, height = 2,fg = "black").pack()
    theJson = Entry(window1,textvariable = jsonFile)
    theJson.pack()
    Button(window1, text = "Convert", command = lambda: csv_to_json(browseFiles.filename, theJson.get())).pack()   


if __name__== "__main__":
    main_window()
    window.mainloop()


#userName = input("Your user name?")
#passWord = input("Your password:")
#auth_api(userName, passWord)