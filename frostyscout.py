import socket
import urllib.request
import json

def esend(message):
#   print(message)
    message += "\r\n"
    s.sendall(message.encode())
    
def msend(message):
#   print(message)
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
        line=line.split()

        if line[0]=="PING":
            esend("PONG %s" % line[1])
            print("Sent PONG.")

        elif "/MOTD" in line:
            esend('JOIN '+CHAN)
            print("Joining %s..." % CHAN)

        elif "PRIVMSG" in line:
            
            if line[3]==":snowman":
                msend("Kill it with fire!")
                
            elif len(line)>3 and line[3]==":!stalk":
                p = json.loads(urllib.request.urlopen("https://api.kag2d.com/player/%s/status" % line[4]).read().decode())
                msend("%s was last on KAG at %s, on server %s" % (p['playerInfo']['username'], p['playerStatus']['lastUpdate'], p['playerStatus']['server']['serverIPv4Address']))
