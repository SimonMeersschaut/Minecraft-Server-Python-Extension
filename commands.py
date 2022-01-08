import json
import time
import os


server = None


class Homes:
    def init():
        os.chdir('..')
        os.chdir('python')

    def read():
        with open('user_info.json', 'r') as f:
            return json.load(f)

    def write(dictionary):
        with open('user_info.json', 'w') as f:
            json.dump(dictionary, f)


def init(server_obj):
    global server
    server = server_obj


requests = {}


def ask(sender, reciever, text, command):
    return [
        'tellraw '+reciever +
        ' [{"text":"'+sender+'", "bold":false, "color":"aqua"}, {"text":" wil naar je teleporteren", "color":"gold", "bold":false}]',
        'tellraw '+reciever +
        ' {"text":"'+text+'", "color":"dark_green", "bold":true, "clickEvent":{"action":"run_command", "value":"'+command+'"}}'
    ]


def create_request(asker, reciever, command, trigger_name):
    global requests
    requests.update(
        {reciever: {"asker": asker, "command": command, "time": time.time(), "trigger": trigger_name}})

################


def tp(sender, args):
    print(sender)
    print('args:')
    print(args)
    trigger_name = f'accept_tp_from_{sender}'
    create_request(sender, args[1], f'/tp {sender} {args[1]}', trigger_name)
    # return 'tellraw @a {"text":"test", "color":"gold", "bold":true, "clickEvent":{"action":"run_command", "value":"!accept"}}'
    server.send(f'/msg {sender} request send')
    server.send(ask(sender, args[1], "[accepteer]",
                f"!accept {trigger_name}"))


def accept(accepter, args):

    print(requests)
    request = requests[accepter]
    asker = args[1].split('_')[-1]
    if asker.lower() == request['asker'].lower():
        if time.time()-request['time'] < 60:
            server.send(request['command'])
        else:
            server.send('msg '+accepter+' request timed out')
    else:
        print('oeps, daar ging iet mis')


def home(sender, args):

    homes = Homes.read()
    if args[1] == 'set':
        x, y, z = server.get_position(sender)
        homes[sender].update({args[2]: [x, y, z]})
        Homes.write(homes)
        server.send('/tellraw '+sender+' {"text":"Home set", "color":"green"}')
    else:
        try:
            x, y, z = homes[sender][args[1]]
            server.send('/tp '+sender+' '+x+' '+y+' '+z)
        except KeyError:
            server.send('/tellraw '+sender +
                        ' {"text":"Home does not exist", "color":"red"}')

        #
        # /tellraw @p {"text":"Do You Like Answering Questions?","color":"gold","bold":true,"hoverEvent":{"action":"show_text","contents":[{"text":"Why are you looking here? Look below!","color":"dark_red","bold":true}]}}
        # First answer: /tellraw @p [{"text":"[YES]","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/tellraw @p [{\"text\":\"Good!\",\"color\":\"green\",\"bold\":true}]"}},{"text":"   "},{"text":"[NO]","color":"red","clickEvent":{"action":"run_command","value":"/tellraw @p [{\"text\":\"Why did you answer this one then???\",\"color\":\"red\",\"bold\":true}]"}}]


def bot(sender, args):
        #temp = f'execute at {sender} run player {args[1]} {args[2]} {args[3]}'
        #if temp[-1] == ' ':
        #        temp = temp[:-1]
        server.send(f'execute at {sender} run player {" ".join(args[1:])}')
        server.send('gamemode survival @a')


def zon(sender, args):
    server.send('weather clear')

def regen(sender, args):
    server.send('weather rain')

def storm(sender, args):
    server.send('weather thunder')