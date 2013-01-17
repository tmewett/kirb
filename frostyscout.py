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

HOST="fr.quakenet.org"
PORT=6667
CHAN="#bow@bots"
NICK="frosty-scout"
IDENT="frs"
REALNAME="Frosty Scout"
readbuffer=""

s=socket.socket()
s.connect((HOST, PORT))
esend("NICK %s" % NICK)
esend("USER %s %s bla :%s" % (IDENT, HOST, REALNAME))
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
            if cmd.group(1)=="snowman":
                msend("Kill it with fire!")
            elif cmd.group(1)=="stalk":
                try:
                    p = json.loads(urllib.request.urlopen("https://api.kag2d.com/player/%s/status" % cmd.group(2)).read().decode())
                    msend("%s was last on KAG at %s, on server %s" % (p['playerInfo']['username'], p['playerStatus']['lastUpdate'], p['playerStatus']['server']['serverIPv4Address']))
                except urllib.request.HTTPError: msend("Can't find user!")
