import tkinter as tk
from tkinter import font
from tkinter import filedialog
import tkinter
from downloader import downloadMp3
import asyncio
import os


def DownloadBtnClick():
    if lblFolderSearch.cget("text") == "Done" and lblFileSearch.cget("text") == "Done":
        for url in urls:
            asyncio.run(downloadMp3(url, folder_directory))

def get_urls():
    global urls
    file_directory = open_file_dialog()
    try:
        with open(file_directory, 'r') as file:
            urls = file.readlines()
        lblFileSearch.config(text="Done")
    except FileNotFoundError:
        print(f"The file '{file_directory}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def open_file_dialog():
    file_path = filedialog.askopenfilename(initialdir="D:\dokumenty", title="Select the file", filetypes=[("Txt files", "*.txt")])
    print(f"file path: {file_path}")
    if file_path is not None and file_path != "":
        return file_path

def open_folder_dialog():
    folder_path = filedialog.askdirectory(initialdir="D:\dokumenty")
    if folder_path is not None:
        return folder_path

def set_download_folder():
    global folder_directory
    folder_directory = open_folder_dialog()
    folder_directory = f"{folder_directory}/"
    if folder_directory:
        lblFolderSearch.config(text="Done")


def main():
    # Create the main Tkinter instance
    root = tk.Tk()
    root.title("Youtube downloader")
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 300
    screen_width = root.winfo_screenwidth()  # Get screen width
    screen_height = root.winfo_screenheight()  # Get screen height

    x_coordinate = (screen_width - WINDOW_WIDTH) // 2
    y_coordinate = (screen_height - WINDOW_HEIGHT) // 2

    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x_coordinate}+{y_coordinate}")

    global lblFileSearch
    global lblFolderSearch

    #Create search file button
    btnFileSearch = tk.Button(root, text="Select txt File", command=get_urls)
    btnFileSearch.place(x=WINDOW_WIDTH/2, y=30)
    lblFileSearch = tk.Label(root, text="None")
    lblFileSearch.place(x=(WINDOW_WIDTH/2)-50, y=30)

    #Create search folder button
    btnFolderSearch = tk.Button(root, text="Select download folder", command=set_download_folder)
    btnFolderSearch.place(x=WINDOW_WIDTH/2, y=80)
    lblFolderSearch = tk.Label(root, text="None")
    lblFolderSearch.place(x=(WINDOW_WIDTH/2)-50, y=80)

    # Create a download button
    btnDownload = tk.Button(root, text="Download", command=DownloadBtnClick)
    btnDownload.place(x=WINDOW_WIDTH/2, y=130)

    # Start the Tkinter main event loop
    root.mainloop()

main()