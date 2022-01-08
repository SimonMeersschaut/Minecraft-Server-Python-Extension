import json
from subprocess import *
from flask import Flask
import commands
import os
import time
import threading
import logging


api = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
class Server:
    waiting = False
    line = ''
    def start():
        os.chdir('..')
        os.chdir('fabric')
        print('[MINECRAFT] starting')
        Server.p = Popen("java -Xms2G -Xmx16G -jar fabric-server-launch.jar nogui".split(' '), stdout=PIPE,
                         stdin=PIPE, stderr=PIPE)
        commands.Homes.init()
        while True:
            Server.line = Server.readline()
            if not Server.waiting:
                print(Server.line, end='')
            if Server.line == '':
                time.sleep(1)
            else:
                Server.handle(Server.line)
    
    def send(line):
        if type(line) == list:
            for i in line:
                Server.p.stdin.write(bytes(i+'\n', encoding='utf-8'))
                Server.p.stdin.flush()
        else:
            Server.p.stdin.write(bytes(line+'\n', encoding='utf-8'))
            try:
                Server.p.stdin.flush()
            except OSError:
                input('Exit server...')
                exit()
        return True
    
    @api.route('/run/<line>')
    def run(line):
        Server.waiting = True
        Server.send(line)
        time.sleep(0.5)
        line = Server.line
        # while line == '':
        #     line = Server.readline()
        #     print(line)
        Server.waiting = False
        return "response: "+line
    def readline():
        try:
            return Server.p.stdout.readline().decode("utf-8")
        except UnicodeError:
            print('ERROR: cant decode...')
    def handle(line):
        try:
            if '<' in line and '>' in line:  # message
                person = line.split('<')[1].split('>')[0]

                if '!' in line:  # command
                    print(line)
                    line = line.strip('\r\n')
                    command = ''.join(line.split('> !')[1:])
                    command_name = command.split(' ')[0]
                    run = True
                    function = getattr(commands, command_name)
                    response = function(person, command.split(' '))
            if 'joined' in line:
                person = line.split(']: ')[1].split(' ')[0]
                with open('user_info.json', 'r') as f:
                    data = json.load(f)
                if person not in data:
                    data.update({person: {}})
                with open('user_info.json', 'w') as f:
                    json.dump(data, f)
        except:
            pass
        # elif 'Triggered' in line:
        #    print('trigger')
        #    person = line.split('[')[3].split(':')[0]
        #    trigger = line.split('[')[4].split(']]')[0]
        #    print(trigger)
        #    if 'accept' in trigger:
        #        print('accept')
        #        commands.accept(person, trigger)

    def get_position(username):
        Server.send(f'execute at {username} run spawnpoint {username} ~ ~ ~')
        response = Server.readline()
        print('YES, '+response)
        x, y, z = response.split('to ')[1].replace(',', '').split(' ')[0:3]
        print('pos: ', str(x), str(y), str(z))
        return x, y, z


def command_line():
    while True:
        Server.send(input(''))

def api_function():
    api.run(debug=False, use_reloader=False)
    

if __name__ == '__main__':
    t1 = threading.Thread(target=command_line)
    t1.start()
    t2 = threading.Thread(target=api_function)
    t2.start()
    os.system('cls')

    commands.init(Server)
    
    
    Server.start()
