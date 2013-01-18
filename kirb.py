import socket
import urllib.request
import json
import re

##### SETTINGS #####
HOST="fr.quakenet.org" # IRC server host
PORT=6667 # IRC port
CHAN="#bow@bots" # Channel to join
ADMIN="tmewett" # User who can use administrative commands

def esend(message):
    message += "\r\n"
    s.sendall(message.encode())
def msend(message):
    message = "PRIVMSG %s :%s\r\n" % (CHAN, message)
    s.sendall(message.encode())
def stalk(player):
    try:
        p = json.loads(urllib.request.urlopen("https://api.kag2d.com/player/%s/status" % player).read().decode())
        s = json.loads(urllib.request.urlopen("https://api.kag2d.com/server/ip/%s/port/50301/status" % p['playerStatus']['server']['serverIPv4Address']).read().decode())
        msend("%s was last on KAG at %s, on %s (%s)" % (p['playerInfo']['username'], p['playerStatus']['lastUpdate'], s['serverStatus']['serverName'], p['playerStatus']['server']['serverIPv4Address']))
    except: msend("Can't find user!")
def info(ip):
    try:
        p = json.loads(urllib.request.urlopen("https://api.kag2d.com/server/ip/%s/port/50301/status" % ip).read().decode())
        msend("%s has %s/%s connected players and is running %s" % (p['serverStatus']['serverName'], p['serverStatus']['currentPlayers'], p['serverStatus']['maxPlayers'], p['serverStatus']['gameMode']))
    except: msend("Can't find server!")

s=socket.socket()
s.connect((HOST, PORT))
esend("NICK kirbot")
esend("USER kirb %s bla :tmewett/kirb" % HOST)
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
            esend("PONG %s" % line[6:])
            print("Sent PONG.")
        elif "/MOTD" in line:
            esend('JOIN '+CHAN)
            print("Joining %s..." % CHAN)
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
