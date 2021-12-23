import json
from subprocess import *
import commands
import os
import time
import threading


class Server:

    def start():
        print('[MINECRAFT] starting')
        os.chdir('..')
        os.chdir('fabric')
        Server.p = Popen("java -Xms4G -Xmx16G -jar fabric-server-launch.jar nogui".split(' '), stdout=PIPE,
                         stdin=PIPE, stderr=PIPE)
        commands.Homes.init()
        while True:
            line = Server.readline()
            print(line, end='')
            if line == '':
                time.sleep(1)
            else:
                Server.handle(line)

    def send(data):
        if type(data) == list:
            for i in data:
                Server.p.stdin.write(bytes(i+'\n', encoding='utf-8'))
                Server.p.stdin.flush()
        else:
            Server.p.stdin.write(bytes(data+'\n', encoding='utf-8'))
            try:
                Server.p.stdin.flush()
            except OSError:
                input('Exit server...')
                exit()


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
            # elif 'Triggered' in line:
            #    print('trigger')
            #    person = line.split('[')[3].split(':')[0]
            #    trigger = line.split('[')[4].split(']]')[0]
            #    print(trigger)
            #    if 'accept' in trigger:
            #        print('accept')
            #        commands.accept(person, trigger)
        except Exception as e:
            print('[INTERNAL SERVER ERROR] '+str(e))

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


t1 = threading.Thread(target=command_line)
t1.start()

commands.init(Server)

Server.start()
