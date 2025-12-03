import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import mimetypes
import os
import hashlib

id = ""
url = "https://www.virustotal.com/api/v3/files"
check_url = f"https://www.virustotal.com/api/v3/files/{id}"

headers = {
    "accept": "application/json",
    "x-apikey": "b7869e37f2589d67bb4ce271a0d5e4074a723672cae260f54664da188f33c047"
}


WIDTH = 1000
HEIGHT = 600




def on_closing():
    if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
        app.destroy()



def recognize_file_type(file_name):
    file_type, _ = mimetypes.guess_type(file_name)
    if file_type is None:
        file_type = "application/octet-stream"
    return file_type


def set_folder_path():
    folder_path = fd.askdirectory()
    if folder_path != "":
        print(f"Selected folder: {folder_path}")
        return folder_path
    else:
        messagebox.showwarning("No Folder Was Selected", "Please select a folder to scan.")
        return None
    
def create_dict_of_folder_files():
    folder_path = set_folder_path()
    if folder_path is None:
        return None
    files = {}
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            file_type = recognize_file_type(filename)
            files[filename] = (filename, open(file_path, 'rb'), file_type)
    return files

def set_file_path(dict):
    file_path = fd.askopenfilename()
    if file_path != "":
        print(f"Selected file: {file_path}")
        file_name = file_path.split("/")[-1]
        file_type = recognize_file_type(file_name)
        dict["file"] = (file_name, open(file_path, 'rb'), file_type)
        return dict
    else:
        messagebox.showwarning("No File Was Selected", "Please select a file to scan.")
        return None

    
def folder_scan():
    global url, headers
    files = create_dict_of_folder_files()

    if files is None:
        return None
    else:
        isContinue = input(f"(y/n): ")#message to send: {url, files, headers}\nscan file? 
        if isContinue.lower() != 'y':
            print("Scan cancelled by user.")
            return
        else:
            try:
                #add a for loop to send all files in the folder one by one
                for file_key in files:
                    single_file = {file_key: files[file_key]}
                    response = requests.post(url, files=single_file, headers=headers)
                    print(response.text)
            except:
                messagebox.showerror("Error", "Failed to connect to the VirusTotal API.")


def file_scan():
    global url, headers
    files = {}
    files = set_file_path(files)
    if files is None:
        return None 
    else:
        isContinue = input(f"message to send: {url, files, headers}\nscan file? (y/n): ")
        if isContinue.lower() != 'y':
            print("Scan cancelled by user.")
            return
        else:
            try:
                response = requests.post(url, files=files, headers=headers)
                print(response.text)
                return response
            except:
                messagebox.showerror("Error", "Failed to connect to the VirusTotal API.")


def analyze_response(response):
    pass



def home_screen(img):
    for widget in app.winfo_children():
        widget.destroy()

    title = tk.Label(app, text="Liron the protector", font=("Arial", 50), bg="#101E29", fg="white")
    title.place(x=WIDTH / 2, y=75, anchor="center")

    slogan = tk.Label(app, text="Best anti virus in the world", font=("Arial", 20), bg="#101E29", fg="white")
    slogan.place(x=WIDTH / 2, y=135, anchor="center")

    img_label = tk.Label(app, image=img, bg="#101E29") 
    img_label.place(x=WIDTH / 2 - 5, y=275, anchor="center")

    choose_file_button = tk.Button(app, text="Choose A File For Scan", command = file_scan, font=("Arial", 18), bg="#4CAF50", fg="white")
    choose_file_button.place(x=WIDTH / 2, y=425, anchor="center")

    or_label = tk.Label(app, text="OR", font=("Arial", 16), bg="#101E29", fg="white")
    or_label.place(x=WIDTH / 2, y=475, anchor="center")

    choose_folder_button = tk.Button(app, text="Choose A Folder For Scan", command= folder_scan, font=("Arial", 18), bg="#2196F3", fg="white")
    choose_folder_button.place(x=WIDTH / 2, y=525, anchor="center")



if __name__ == "__main__":
    app = tk.Tk()
    app.iconbitmap('images/logo.ico')
    app.title("Liron the protector")

    app.geometry("1000x600")
    app.resizable(False, False)

    app.configure(bg="#101E29")

    app.protocol("WM_DELETE_WINDOW", on_closing)

    home_page_image = Image.open("images/small_desktop_PC.png")

    home_page_image = home_page_image.resize((320, 220), Image.Resampling.LANCZOS)
    home_page_image = ImageTk.PhotoImage(home_page_image)

    home_screen(home_page_image)
    print()

    app.mainloop()