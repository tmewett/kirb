import socket

def esend(message, socket):
#   print(message)
    message += "\r\n"
    socket.send(message.encode())
    
def message(message, channel, socket):
    message = "PRIVMSG %s %s\r\n" % (channel, message)
    socket.send(message.encode())

HOST="irc.uk.quakenet.org"
PORT=6667
CHAN="#bow@testing_bots"
NICK="tobot"
IDENT="dallas-b"
REALNAME="Tom's Bot"
readbuffer=""

s=socket.socket()
s.connect((HOST, PORT))
esend("NICK %s" % NICK, s)
esend("USER %s %s bla :%s" % (IDENT, HOST, REALNAME), s)
while 1:
    readbuffer=readbuffer+s.recv(512).decode()
    temp=readbuffer.split("\n")
    readbuffer=temp.pop()

    for line in temp:
        line=line.rstrip()
#       print(line)
        line=line.split()

        if line[0]=="PING":
            esend("PONG %s" % line[1], s)
            print("Sent PONG.")

        elif "/MOTD" in line:
            esend('JOIN '+CHAN, s)
            print("Joining %s..." % CHAN)

        elif "PRIVMSG" in line:
            msg = "".join(line).split(":")
            msg[1] = msg[1].split("!")[0]
            msg.remove("")
            print(msg)
            
            if msg[1]=="tobot":
                message("I heard you!", CHAN,s)