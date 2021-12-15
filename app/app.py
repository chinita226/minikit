
"""App run class."""
from functools import partial
from tkinter import *
from tkinter import filedialog
import os
import tkinter as tk
import tkinter.messagebox
import requests
import json
from requests.auth import HTTPBasicAuth
import numpy as np
import pandas as pd


def auth_api(username, password):
    """Auth function to validate API."""
    res = requests.get('https://api.quickbutik.com/v1/products', auth=HTTPBasicAuth(username.get(), password.get()))
    print(res.status_code)
    if res.status_code == 200:
        tkinter.messagebox.showinfo("Welcome to quickbutik.", "Login successfully.")
        new_frame.pack_forget()
        path_frame.pack()
    else:
        tkinter.messagebox.showinfo("Login failed.", "Wrong user name or password.")


def check_path(json_path):
    """Check path."""
    if os.path.exists(json_path):
        tkinter.messagebox.showinfo("File name error.", "File already existed.")
        return True
    else:
        return False


def myconverter(obj):
    """Define customized json.dump function."""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()


def csv_to_json(csvFile, json_path):
    """Get csv file and export to json."""
    jsonArray = []

    with open(csvFile, 'r', encoding='UTF-8') as csvf:
        data = pd.read_csv(csvf)
    sku = data.sku
    title = data.title
    description = data.description
    price = data.price
    before_price = data.before_price
    tax_rate = data.tax_rate
    weight = data.weight
    stock = data.stock
    gtin = data.gtin
    images = data.images
    headcategory_name = data.headcategory_name
    visible = data.visible
    x = 0
    while x < len(sku):
        dict_list = {}
    # print(images[x])
        image_list = []
        image_dic = {}
        image_dic["url"] = images[x]
        image_list.append(image_dic)
        dict_list["sku"] = sku[x]
        dict_list["title"] = title[x]
        dict_list["description"] = description[x]
        dict_list["price"] = int(price[x])
        # check if before price has any empty values
        before_price_data = pd.DataFrame(before_price)
        if before_price_data["before_price"].isnull().values.any():
            dict_list["before_price"] = " "
        else:
            dict_list["before_price"] = before_price[x]
        # check if tax rate has nan
        tax_rate_data = pd.DataFrame(tax_rate)
        if tax_rate_data["tax_rate"].isnull().values.any():
            dict_list["tax_rate"] = " "
        else:
            dict_list["tax_rate"] = tax_rate[x]
        weight_data = pd.DataFrame(weight)
        if weight_data["weight"].isnull().values.any():
            dict_list["weight"] = " "
        else:
            dict_list["weight"] = weight[x]
        dict_list["stock"] = stock[x]

        gtin_data = pd.DataFrame(gtin)
        if gtin_data["gtin"].isnull().values.any():
            dict_list["gtin"] = " "
        else:
            dict_list["gtin"] = gtin[x]
        dict_list["images"] = image_list
        dict_list["headcategory_name"] = headcategory_name[x]
        dict_list["visible"] = int(visible[x])
        jsonArray.append(dict_list)
        x = x+1
    toJson(json_path, jsonArray)


def toJson(json_path, container):
    """Convert to json file."""
    global final_json

    file_status = check_path(json_path)
    if file_status is False:
        if (json_path.endswith('.json')):
            with open(json_path, 'w', encoding='UTF-8') as jsonf:
                jsonString = json.dumps(container, ensure_ascii=False, indent=4, default=myconverter, skipkeys=True)
                # uploadJson is file converted
                jsonf.write(jsonString)
                final_json = json_path
                tkinter.messagebox.showinfo("Successful.", "Json file created.")
        else:
            tkinter.messagebox.showinfo("Error.", "Make sure that your file name contains .json.")

    # fixed error of: raise JSONDecodeError("Expecting value", s, err.value) from None
    json_text(final_json)


def json_text(json_filename):
    """Show json text on frame."""
    with open(json_filename, encoding="UTF-8") as f:
        data = json.load(f)

    new_data = json.dumps(data, indent=3, ensure_ascii=False)
    window.geometry("600x600")
    json_frame = Frame(window, width=600, height=600)
    text = Text(json_frame, state='normal')
    text.insert('1.0', str(new_data))
    json_frame.pack()
    text.pack()


def browseFiles(label_file_explorer):
    """Browse csv file."""
    browseFiles.filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("CSV file", "*.csv*"), ("CSV file", "*.csv*")))
    label_file_explorer.configure(text=browseFiles.filename)


def upload():
    """Upload to server."""
    url = "https://api.quickbutik.com/v1/products"
    with open(final_json, encoding="UTF-8") as json_file:
        json_data = json.load(json_file)
    upload = requests.post(url, json=json_data, auth=HTTPBasicAuth(userName.get(), passWord.get()))
    path_frame.forget()
    window.geometry("600x600")
    response_frame = Frame(window, width=600, height=600)
    text = Text(response_frame, state='normal')
    text.insert('1.0', str(upload.content))
    response_frame.pack()
    text.pack()


"""Define app window and login frame."""
window = tk.Tk()
window.geometry("450x400")
window.title("Minikit")

new_frame = Frame(window, width=300, height=300)
userName = StringVar()
passWord = StringVar()
Label(new_frame, text="Enter your api key below").pack()
Label(new_frame, text="User name").pack()
Entry(new_frame, textvariable=userName).pack()
Label(new_frame, text="Password").pack()
Entry(new_frame, textvariable=passWord).pack()
validateLogin = partial(auth_api, userName, passWord)
Button(new_frame, text="Log in", width=10, height=1, command=validateLogin).pack()
new_frame.pack()


"""Frame to convert csv to json and upload to server."""
jsonFile = str
path_frame = Frame(window, width=300, height=300)
Label(path_frame, text="Convert csv to json file", bg="grey", width="300", height="2", font=('Calibri', 13)).pack()
Label(path_frame, text="Browse to find your csv file", width=100, height=1, fg="black").pack()
label_file_explorer = Label(path_frame, text="Name of file", width=100, height=2, fg="black")
label_file_explorer.pack()
Button(path_frame, text="Browse Files", command=lambda: browseFiles(label_file_explorer)).pack()
Label(path_frame, text="Enter name for json file, must end with .json", width=100, height=2, fg="black").pack()
theJson = Entry(path_frame, textvariable=jsonFile)
theJson.pack()
Button(path_frame, text="Convert", command=lambda: csv_to_json(browseFiles.filename, theJson.get())).pack()
Button(path_frame, text="Upload to server!", command=upload).pack(padx=10, pady=10)


if __name__ == "__main__":
    window.mainloop()
