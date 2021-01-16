from quickstart import main
import requests
import json
import sys
import os 
from datetime import datetime, date
from dotenv import load_dotenv
load_dotenv()


def upload_to_drive(filename, path_to_file):

    headers = {"Authorization": "Bearer " + os.getenv('ACCESS_TOKEN'), 
    "Content-Type": "application/json; charset=UTF-8"} 

    # print(filename, path_to_file)

    filesize = os.path.getsize(path_to_file)

    params = {
        "name": filename,
        "parents": [os.getenv('FOLDER')],
        "mimeType": "video/mp4"
    }

    r = requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable",
        headers=headers,
        data=json.dumps(params)
    )
    
    location = r.headers['Location']
    # print(location)

    headers = {"Content-Range": "bytes 0-" + str(filesize - 1) + "/" + str(filesize)}
    r = requests.put(
        location,
        headers=headers,
        data=open(path_to_file, 'rb')
    )

    if r.status_code == '200':
        with open('/home/kushagra/Desktop/zoomuploadgd/already_uploaded.txt', 'a') as file:
            file.write(filename) 
            file.write("\n")


if __name__ == '__main__':
    path = '/home/kushagra/Documents/Zoom/'
    os.chdir(path)

    with open('/home/kushagra/Desktop/zoomuploadgd/already_uploaded.txt', 'r') as f:
        already_uploaded = f.readlines()

    month_dict = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'June', 7:'July', 8:'Aug', 9:'Sept', 10:'Oct', 11:'Nov', 12:'Dec'}

    for dir in os.listdir('.'):
        dir_name = dir
        dmy = dir_name.split()[0]
        time = dir_name.split()[1]
        new_time_format = datetime.strptime(time, "%H.%M.%S")
        new_time = new_time_format.strftime("%I:%M%p")
        dte = dmy.split('-')[-1]
        month = month_dict[int(dmy.split('-')[1])]
        year = '21'
        day_name = date(int(year), int(dmy.split('-')[1]), int(dte)) 
        day = day_name.strftime("%A")
        new_dir_name = 'Kushagra ' + dte + month + year + ' ' + new_time + ' ' + day
        path_to_file = path + dir + '/' + 'zoom_0.mp4'
        # print(dir, new_dir_name) 
        if new_dir_name not in already_uploaded:
            for file in os.listdir(dir):
                if file == 'zoom_0.mp4':
                    # print(new_dir_name)
                    upload_to_drive(new_dir_name, path_to_file)
  
            



