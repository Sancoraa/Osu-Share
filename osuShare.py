import os
import re
import subprocess
from datetime import datetime

# Get and format date
current_datetime = datetime.now()
date_str = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

choice = input('Do you want to import or export songs ? (imp/exp)\n')

if choice == 'exp':
	output_filename = f"output_{date_str}.txt" #Create file
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
	pathChoice = input('Enter the path of the txt file:\n')
	current_directory = os.path.dirname(os.path.abspath(__file__))
	directory_name = date_str
	new_directory = os.path.join(current_directory, directory_name)
	desired_extension = '.osz'
	os.makedirs(new_directory, exist_ok=True)
	print('Downloading beatmaps, please wait.')

	with open (pathChoice, 'r') as file:
		for line in file:
			url_to_file = 'https://api.chimu.moe/v1/download/' + line.strip()
			print(url_to_file)
			result = subprocess.run(['curl', '-O', '--output-dir', directory_name, url_to_file])
			#result = subprocess.run(['wget', '--content-disposition', '-P', directory_name, url_to_file])
			#if result.returncode == 0:
			#	print('File downloaded sucessfully.')
			#else:
			#	print('Error downloading file')
			#print(line.strip())

else:
	print('Please write imp or exp')