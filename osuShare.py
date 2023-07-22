import os
import re
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Get the current script's directory path
current_directory = os.getcwd()

# Get and format the current date and time
current_datetime = datetime.now()
date_str = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

# Ask the user to choose between import ('imp') or export ('exp') songs
choice = input('Do you want to import or export songs? (imp/exp)\n')

if choice == 'exp':
    # Form the output file name
    output_filename = os.path.join(current_directory, f"output_{date_str}.txt")
    songFolder = input('Enter the path of your osu! songs folder:\n')
    pattern = re.compile(r'^(\d+)')

    # Export songs
    with open(output_filename, 'w') as file:
        entries = os.listdir(songFolder)
        print('The file ' + output_filename + ' has been created.')
        for entry in entries:
            match = pattern.match(entry)
            if match:
                number_part = match.group(1)
                file.write(number_part + "\n")

elif choice == 'imp':
    # Search for the "output" files in the current directory
    output_files = [f for f in os.listdir(current_directory) if f.startswith("output") and f.endswith(".txt")]
    if not output_files:
        print("Error: No 'output' files found in the current directory.")
    else:
        # Display the available "output" files to the user and let them choose one
        print("Available 'output' files:")
        for idx, file in enumerate(output_files, 1):
            print(f"{idx}. {file}")
        selection = int(input("Choose the number corresponding to the 'output' file to use: "))

        # Ensure the selected number is within the valid range
        if 1 <= selection <= len(output_files):
            # Take the selected "output" file
            selected_output = output_files[selection - 1]
            output_filename = os.path.join(current_directory, selected_output)
            new_directory = os.path.join(current_directory, date_str)
            desired_extension = '.osz'
            os.makedirs(new_directory, exist_ok=True)
            print('Downloading beatmaps, please wait.')

            # Read the beatmap URLs from the selected "output" file
            with open(output_filename, 'r') as file:
                urls_to_download = ['https://api.chimu.moe/v1/download/' + line.strip() for line in file]

            def download_beatmap(url):
                # Download the beatmap from the URL
                print(f"Downloading: {url}")
                response = requests.get(url)
                if response.status_code == 200:
                    file_path = os.path.join(new_directory, os.path.basename(url) + desired_extension)
                    # Save the beatmap to the new directory with the appropriate name
                    with open(file_path, 'wb') as new_file:
                        new_file.write(response.content)
                    print(f"Downloaded: {file_path}")
                else:
                    print(f"Error: Failed to download {url}")

            # Use the ThreadPoolExecutor to download the beatmaps concurrently
            with ThreadPoolExecutor() as executor:
                executor.map(download_beatmap, urls_to_download)
        else:
            print("Invalid selection. Please choose a valid number.")
else:
    print('Please write "imp" or "exp"')
