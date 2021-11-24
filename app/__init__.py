
"""App run class."""
from functools import partial
from tkinter import *
from tkinter import filedialog
import os
import tkinter as tk
import tkinter.messagebox
from typing import cast
import requests
import json
import csv
from requests.auth import HTTPBasicAuth


def auth_api(username, password):
    """Auth function to validate API."""

    res = requests.get('https://api.quickbutik.com/v1/products', auth=HTTPBasicAuth(username.get(), password.get()))
    print(res.status_code)
    if res.status_code == 200:
        tkinter.messagebox.showinfo("Welcome to quickbutik.", "Login successfully.")
        new_frame.pack_forget()
        path_frame.pack()
        #path_window()
    else:
        tkinter.messagebox.showinfo("Login failed.", "Wrong user name or password.")

window = tk.Tk()
window.geometry("450x400")
window.title("Minikit")

new_frame = Frame(window, width=300, height=300)
userName = StringVar()
passWord = StringVar()
Label(new_frame, text="Enter your api key below").pack()
Label(new_frame, text="User name").pack()
Entry(new_frame, textvariable= userName).pack()
Label(new_frame, text="Password").pack()
Entry(new_frame, textvariable=passWord).pack()
validateLogin = partial(auth_api, userName, passWord)
Button(new_frame, text="Log in", width=10, height=1, command=validateLogin).pack()
new_frame.pack()

def check_path(json_path):
    if os.path.exists(json_path): 
        tkinter.messagebox.showinfo("File name error.", "File already existed.")
        return True
    else:
        return False

def csv_to_json(csvFile, json_path):
    """Get csv file and export to json."""
    global jsonArray
    jsonArray = []
    global uploadJson

    with open(csvFile,'r', encoding='UTF-8') as csvf: 
        csvReader = csv.DictReader(csvf) 
        for row in csvReader: 
            jsonArray.append(row)
    
    file_status = check_path(json_path)

    if file_status==False:
        if (json_path.endswith('.json')):
            with open(json_path, 'w', encoding='UTF-8') as jsonf:
                jsonString = json.dumps(jsonArray, ensure_ascii= False, indent=4)
                # uploadJson is file converted
                jsonf.write(jsonString)
                uploadJson=json_path
                tkinter.messagebox.showinfo("Successful.", "Json file created.")
        else:
            tkinter.messagebox.showinfo("Error.", "Make sure that your file name contains .json.")

def browseFiles(label_file_explorer):
    browseFiles.filename = filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = (("CSV file", "*.csv*"),("CSV file", "*.csv*")))
    label_file_explorer.configure(text = browseFiles.filename)

"""Start from here to browse the json file."""
def upload_to_server():
    path_frame.pack_forget()
    upload_frame = Frame(window, width=300, height=300).pack()
    Label(upload_frame, text="Upload json to quickbuti server", bg="grey", width="300", height="2", font=('Calibri', 13)).pack()
    Button(upload_frame, text = "Browse json file", width = 100, height = 1,fg = "black", command=upload).pack()


jsonFile = str
path_frame = Frame(window, width=300, height=300)
Label(path_frame, text="Convert csv to json file", bg="grey", width="300", height="2", font=('Calibri', 13)).pack()
Label(path_frame, text = "Browse to find your csv file", width = 100, height = 1,fg = "black").pack()
label_file_explorer = Label(path_frame, text = "Name of file", width=100, height= 2, fg = "black")
label_file_explorer.pack()
Button(path_frame, text = "Browse Files", command = lambda: browseFiles(label_file_explorer)).pack()
Label(path_frame, text = "Enter name for json file, must end with .json", width = 100, height = 2,fg = "black").pack()
theJson = Entry(path_frame, textvariable = jsonFile)
theJson.pack()
Button(path_frame, text = "Convert", command = lambda: csv_to_json(browseFiles.filename, theJson.get())).pack()   
Button(path_frame, text="Upload to server!", command=upload_to_server).pack(padx=10,pady=10)


def upload():
    #url = "https://api.quickbutik.com/v1/products"
    #print(uploadJson)
    with open('{uploadJson}') as json_file:
        json_data = json.load(json_file)
    print(json_data)
    #upload = requests.post(url, json=json_data)
    #print(upload.status_codes)

#path_frame.pack()

if __name__== "__main__":
    #main_window()
    window.mainloop()
