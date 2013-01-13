import socket

def esend(message):
#   print(message)
    message += "\r\n"
    s.sendall(message.encode())
    
def msend(message):
    print(message)
    message = "PRIVMSG %s %s\r\n" % (CHAN, message)
    s.sendall(message.encode())

HOST="uk.quakenet.org"
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
    readbuffer=readbuffer+s.recv(512).decode()
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
            msg = "".join(line).split(":")
            msg[1] = msg[1].split("!")[0]
            del(msg[0])
            print(msg)
            
            if msg[1]=="tobot":
                msend("I heard you!")
