import socket
import urllib.request
import json
import re

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

HOST="fr.quakenet.org"
PORT=6667
CHAN="#bow@bots"
NICK="kirbot"
IDENT="kirb"
readbuffer=""

s=socket.socket()
s.connect((HOST, PORT))
esend("NICK %s" % NICK)
esend("USER %s %s bla :tmewett/kirb" % (IDENT, HOST))
print("Logged in.")
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
            cmd = re.search(r":!(\w+) ?(.+)?$", line)
            if cmd==None: pass
            elif cmd.group(1)=="stalk": stalk(cmd.group(2))
            elif cmd.group(1)=="help": msend("!stalk <player>: Last activity from player; !info <ip>: Server information for IP; !snowman: Advice")
            elif cmd.group(1)=="info": info(cmd.group(2))
            elif cmd.group(1)=="move":
                esend("PART "+CHAN)
                CHAN = cmd.group(2)
                esend("JOIN "+CHAN)
            elif cmd.group(1)=="nick": esend("NICK "+cmd.group(2))
