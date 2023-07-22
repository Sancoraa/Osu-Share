import os
import re
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import filedialog

# Function for exporting songs
def export_songs():
    # Form the output filename based on the current date and time
    output_filename = os.path.join(current_directory, f"output_{date_str}.txt")
    # Get the path of the osu! songs folder from the entry widget
    songFolder = folder_entry.get()
    # Regular expression pattern to extract song numbers from folder names
    pattern = re.compile(r'^(\d+)')

    # Export songs logic
    with open(output_filename, 'w') as file:
        entries = os.listdir(songFolder)
        for entry in entries:
            match = pattern.match(entry)
            if match:
                number_part = match.group(1)
                file.write(number_part + "\n")
    output_label.config(text=f"The file {output_filename} has been created.")

# Function for importing songs
def import_songs():
    # Ask the user to select the output file containing the song information
    selected_output = filedialog.askopenfilename(title="Select output file", filetypes=[("Text Files", "*.txt")])
    if not selected_output:
        # If no file is selected, return without further action
        return

    # Create a new directory for downloaded beatmaps based on the current date and time
    new_directory = os.path.join(current_directory, date_str)
    desired_extension = '.osz'
    os.makedirs(new_directory, exist_ok=True)
    download_label.config(text='Downloading beatmaps, please wait.')

    # Read the beatmap URLs from the selected output file
    with open(selected_output, 'r') as file:
        urls_to_download = ['https://api.chimu.moe/v1/download/' + line.strip() for line in file]

    def download_beatmap(url):
        # Download the beatmap from the URL
        response = requests.get(url)
        if response.status_code == 200:
            file_path = os.path.join(new_directory, os.path.basename(url) + desired_extension)
            # Save the beatmap to the new directory with the appropriate name
            with open(file_path, 'wb') as new_file:
                new_file.write(response.content)
        else:
            print(f"Error: Failed to download {url}")

    # Use ThreadPoolExecutor to download the beatmaps concurrently
    with ThreadPoolExecutor() as executor:
        executor.map(download_beatmap, urls_to_download)

    download_label.config(text='Download completed.')

# Create the main Tkinter window
root = tk.Tk()
root.title("osu!share")

# Get the current script's directory path
current_directory = os.getcwd()

# Get and format the current date and time
current_datetime = datetime.now()
date_str = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

# Create widgets for export
export_frame = tk.Frame(root, padx=10, pady=10)
export_frame.pack(fill=tk.BOTH, expand=True)

folder_label = tk.Label(export_frame, text="Enter the path of your osu! songs folder:")
folder_label.pack()

folder_entry = tk.Entry(export_frame)
folder_entry.pack()

export_button = tk.Button(export_frame, text="Export Songs", command=export_songs)
export_button.pack()

output_label = tk.Label(export_frame, text="")
output_label.pack()

# Create widgets for import
import_frame = tk.Frame(root, padx=10, pady=10)
import_frame.pack(fill=tk.BOTH, expand=True)

import_button = tk.Button(import_frame, text="Import Songs", command=import_songs)
import_button.pack()

download_label = tk.Label(import_frame, text="")
download_label.pack()

root.mainloop()
