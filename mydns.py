import socket
from array import *


def ip_decoder(message1, message2, message3, message4):
    ip1 = ord(message1) if len(message1) == 1 else int(message1, 16)
    ip2 = ord(message2) if len(message2) == 1 else int(message2, 16)
    ip3 = ord(message3) if len(message3) == 1 else int(message3, 16)
    ip4 = ord(message4) if len(message4) == 1 else int(message4, 16)
    ip = str(ip1) + '.' + str(ip2) + '.' + str(ip3) + '.' + str(ip4)
    return ip

def copy(message, pos):
    name = ''
    pos = int(message[pos+1], 16) if len(message[pos+1]) == 2 else ord(message[pos+1])
    pos += 1
    while(message[pos] != '00'):
        if(message[pos] == 'c0'):
            name = name + '.' + copy(message, pos)
            return (name)
        elif(len(message[pos]) == 2):
            name = name + '.'
        else:
            name = name + message[pos]
        pos += 1
    return(name)

def name_decoder(message, pos, length):
    if(message[pos] == 'c0'):
        return (copy(message, pos))
    else:
        pos += 1
        length -= 1
        name = ''
        while(length > 0):
            if(message[pos] == 'c0'):
                length -= 2
                name = name + '.' + copy(message, pos)
            else:
                if(len(message[pos]) == 2):
                    name = name + '.'
                else:
                    name = name + message[pos]
                length -= 1
                pos += 1
        return (name)

def display(message, extra):
    print('----------------------------------------')
    print('DNS server to query: ' + extra)
    print('Reply received. Content overview:')
    print('\t' + str(int(message[4]+message[5], 16)) + ' Queries')
    Answers = int(message[6]+message[7], 16)
    print('\t' + str(Answers) + ' Answers')
    INS = int(message[8]+message[9], 16)
    print('\t' + str(INS) + ' Intermediate Name Server')
    AIR = int(message[10]+message[11], 16)
    print('\t' + str(AIR) + ' Additional Information Records')
    print('Answer section:')
    pos = 11
    pos = message.index('c0', pos)
    name = ''
    while(Answers != 0):
        name = ''
        if(message[pos] == 'c0'):
            name = name_decoder(message, pos, 0)
        pos += 1
        pos = message.index('c0', pos)
        ip = ip_decoder(message[pos-4], message[pos-3], message[pos-2], message[pos-1])
        print('\tName : ' + name + '\t' + 'IP : ' + ip)
        Answers -= 1
        
    print('Authoritive section:')
    while(INS != 0):
        name = ''
        if(message[pos] == 'c0'):
            name = name_decoder(message, pos, 0)
        pos += 10
        digit1 = message[pos] if (len(message[pos])) == 2 else str(ord(message[pos]))
        pos += 1
        digit2 = message[pos] if (len(message[pos])) == 2 else str(ord(message[pos]))
        pos += 1
        length = int((digit1 + digit2), 16)
        server = name_decoder(message, pos, length)
        pos += length
        print('\tName : ' + name + '\t' + 'Name Server : ' + server)
        INS -= 1
    
    print('Additional Information section:')
    while(AIR != 0):
        name = ''
        if(message[pos] == 'c0'):
            name = name_decoder(message, pos, 0)
        pos = pos + 2
        serverType = int((message[pos+1]), 16)
        pos += 10
        if(serverType == 1):
            pos += 4
            ip = ip_decoder(message[pos-4], message[pos-3], message[pos-2], message[pos-1])
            print('\tName : ', name, '\t', 'IP : ', ip)

        else:
            pos += 16
            print('\tName : ', name)
        AIR -= 1
    if(int(message[6]+message[7], 16) > 0):
        return (str(int(message[6]+message[7], 16)))
    else:
        return (name)


def organize(response, extra):
    message = []
    message.append(response[2])
    message.append(response[3])
    count = 4
    word = ''
    while(count < len(response) - 1):
        if(response[count] == '\\'):
            count += 1
            if(response[count] == 'x'):
                count += 1
                word = response[count:count+2]
                message.append(word)
                count += 2
                if(response[count] != '\\'):
                    while((response[count] != '\\') & (count < len(response) - 1)):
                        message.append(response[count])
                        count += 1
            else:
                if(response[count] == 't'):
                    message.append('09')
                elif(response[count] == 'n'):
                    message.append('0a')
                elif(response[count] == 'r'):
                    message.append('0d')
                elif(response[count] == 'v'):
                    message.append('0b')
                elif(response[count] == 'f'):
                    message.append('0c')
                else:
                    message.append('5c')
                count += 1
    return(display(message, extra))


print('---------------------')
Name = 'facilities.fiu.edu'
Port = 53
extra = '202.12.27.33'
#extra = 'c.edu-servers.net'
#extra = 'nameserver2.fiu.edu'
#extra = 'sagwa-ns.cs.fiu.edu'
extra2 = '131.94.130.238'

#extra = 'a.edu-servers.net'
#extra = 'nameserver1.fiu.edu'
#extra = 'offsite.cs.fiu.edu'

mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
result = False
while (result == False):
    request = bytes.fromhex('43470100000100000000000002637303666975036564750000010001')

    mysocket.sendto(request,(extra, Port))
    response = (mysocket.recvfrom(521))
    extra = organize(str(response[0]), extra)
    if(len(extra) == 1):
        result = True