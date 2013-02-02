import socket
import urllib.request
import json
import re

with open("kirb.cfg.txt", "r") as f:
    for l in f.readlines():
        exec(l.strip())

def esend(message):
    message += "\r\n"
    s.sendall(message.encode())
def msend(message):
    message = "PRIVMSG {} :{}\r\n".format(CHAN, message)
    s.sendall(message.encode())
def stalk(player):
    try:
        p = json.loads(urllib.request.urlopen("https://api.kag2d.com/player/{}/status".format(player)).read().decode())
        s = json.loads(urllib.request.urlopen("https://api.kag2d.com/server/ip/{}/port/50301/status".format(p['playerStatus']['server']['serverIPv4Address'])).read().decode())
        msend("{} was last on KAG at {}, on {} ({})".format(p['playerInfo']['username'], p['playerStatus']['lastUpdate'], s['serverStatus']['serverName'], p['playerStatus']['server']['serverIPv4Address']))
    except: msend("Can't find user!")
def info(ip):
    try:
        p = json.loads(urllib.request.urlopen("https://api.kag2d.com/server/ip/{}/port/50301/status".format(ip)).read().decode())
        msend("{} has {}/{} connected players and is running {}".format(p['serverStatus']['serverName'], p['serverStatus']['currentPlayers'], p['serverStatus']['maxPlayers'], p['serverStatus']['gameMode']))
    except: msend("Can't find server!")

s=socket.socket()
s.connect((HOST, PORT))
esend("NICK kirbot")
esend("USER kirb {} bla :tmewett/kirb".format(HOST))
print("Logged in.")
readbuffer=""
while 1:
    readbuffer=readbuffer+s.recv(1024).decode()
    temp=readbuffer.split("\n")
    readbuffer=temp.pop()
    for line in temp:
        line=line.rstrip()
#       print(line)
        if line[0:4]=="PING":
            esend("PONG "+line[6:])
            print("Sent PONG.")
        elif "/MOTD" in line:
            esend("JOIN "+CHAN)
            print("Joining {}...".format(CHAN))
        elif ':!' in line:
            cmd = re.search(r"^:([^!]+)!.+?:!(\w+) ?(.+)?$", line)
            if cmd==None: pass
            elif cmd.group(2)=="stalk": stalk(cmd.group(3))
            elif cmd.group(2)=="help": msend("!stalk <player>: Last activity from player; !info <ip>: Server information for IP; !nick <name>: Changes nickname (ADMIN only); !move #<channel>: Moves channel (ADMIN only)")
            elif cmd.group(2)=="info": info(cmd.group(3))
            elif cmd.group(2)=="move" and cmd.group(1)==ADMIN:
                esend("PART "+CHAN)
                CHAN = cmd.group(3)
                esend("JOIN "+CHAN)
            elif cmd.group(2)=="nick" and cmd.group(1)==ADMIN: esend("NICK "+cmd.group(3))
