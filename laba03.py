import socket, threading, time



def crypt(encr, key):
    alph = ("abcdefghijklmnopqrstuvwsyzabcdefghijklmnopqrstuvwsyz")
    num = ("1234567890")

    encr = encr + ""

    i = 0
    while i < 1:
        i += 1
        encr2 = ""
        a = ""
        for letter in encr:
            position = alph.find(letter)
            pos = num.find(letter)
            newPosititon2 = pos + key
            newPosititon = position + key
            if letter in alph:
                if a != "":
                    a = int(a)
                    a = a + key
                    a = str(a)
                    encr2 = encr2 + a
                    a = ""

                encr2 = encr2 + alph[newPosititon]
            elif letter in num:
                a = a + letter
            else:
                if a != "":
                    a = int(a)
                    a = a + key
                    a = str(a)
                    encr2 = encr2 + a
                    a = ""
                encr2 = encr2 + letter
        return encr2

key = 1
shutdown = False
join = False

x = input(' Decrypt messages? yes or not: ')


def receving(name, sock):
    while not shutdown:
        try:
            while True:
                data, addr = sock.recvfrom(1024)

                decrypt = " "
                k = False
                if x == "yes":
                    for i in data.decode("utf-8"):
                        if i == ":":
                            k = True
                            decrypt += i
                        elif k == False or i == " ":
                            decrypt += i
                        else:
                            decrypt += crypt(i, -key)
                else:
                    for i in data.decode("utf-8"):
                        if i == ":":
                            k = True
                            decrypt += i
                        elif k == False or i == " ":
                            decrypt += i
                        else:
                            decrypt += i

                print(decrypt)

                time.sleep(0.2)
        except:
            pass


host = socket.gethostbyname(socket.gethostname())
port = 0

server = ("192.168.3.16", 4040)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(False)

alias = input("Name: ")

rT = threading.Thread(target=receving, args=("RecvThread", s))
rT.start()

while shutdown == False:
    if join == False:

        s.sendto(("[" + alias + "] => join chat ").encode("utf-8"), server)
        join = True
    else:
        try:
            encr = input()

            encr = crypt(encr, 1)


            if encr != "":
                s.sendto(("[" + alias + "] :: " + encr).encode("utf-8"), server)

            time.sleep(0.2)
        except:
            s.sendto(("[" + alias + "] <= left chat ").encode("utf-8"), server)
            shutdown = True

rT.join()
s.close()
