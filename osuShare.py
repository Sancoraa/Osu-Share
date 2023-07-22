import os
import re
import requests
from datetime import datetime

# Получаем путь к текущей директории скрипта
current_directory = os.getcwd()

# Получаем и форматируем текущую дату и время
current_datetime = datetime.now()
date_str = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

choice = input('Do you want to import or export songs? (imp/exp)\n')

if choice == 'exp':
    # Формируем имя файла вывода
    output_filename = os.path.join(current_directory, f"output_{date_str}.txt")
    songFolder = input('Enter the path of your osu! songs folder:\n')
    pattern = re.compile(r'^(\d+)')

    with open(output_filename, 'w') as file:
        entries = os.listdir(songFolder)
        print('The file ' + output_filename + ' has been created.')
        for entry in entries:
            match = pattern.match(entry)
            if match:
                number_part = match.group(1)
                file.write(number_part + "\n")

elif choice == 'imp':
    # Ищем файл "output" в текущей директории
    output_files = [f for f in os.listdir(current_directory) if f.startswith("output") and f.endswith(".txt")]
    if not output_files:
        print("Error: The 'output' file not found in the current directory.")
    else:
        # Берем первый найденный файл "output" (можно настроить для нескольких файлов)
        output_filename = os.path.join(current_directory, output_files[0])
        new_directory = os.path.join(current_directory, date_str)
        desired_extension = '.osz'
        os.makedirs(new_directory, exist_ok=True)
        print('Downloading beatmaps, please wait.')

        with open(output_filename, 'r') as file:
            for line in file:
                url_to_file = 'https://api.chimu.moe/v1/download/' + line.strip()
                print(url_to_file)
                response = requests.get(url_to_file)
                if response.status_code == 200:
                    file_path = os.path.join(new_directory, line.strip() + desired_extension)
                    with open(file_path, 'wb') as new_file:
                        new_file.write(response.content)
                    print(f"Downloaded: {file_path}")
                else:
                    print(f"Error: Failed to download {line.strip()}")

else:
    print('Please write "imp" or "exp"')
