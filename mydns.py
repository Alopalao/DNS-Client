import socket
from array import *


def hextoLetter(number):
    ko = 43

def hextoDeci(number, base):
    return 
    
def messages(x_count, number):
    switch = {
        3: (number + ' Queries'),
        5: (number + ' Answers'),
        7: (number + ' Intermediate Name Servers'),
        9: (number + ' Additional Information Records')
    }
    return switch.get(x_count, "wut")

def dictionary(response, server):
    print('DNS server to query: ' + server)
    print('Reply received. Content overview:')
    found = 0
    x_count = 0
    current = ''
    queries = 0
    answers = 1
    authority = 4
    additional = 6
    while(found != -1):
        found = response.find('x')
        #print(found)
        print(x_count)
        if(x_count == 3 or x_count == 5 or x_count == 7 or x_count == 9): #Questions
            print('-------------------------------------------')
            number = response[found - 3:found - 1] + '' + response[found + 1:found + 3]
            number1 = int(number, 16)
            print(messages(x_count, str(number1)))
            response = response[found + 3:len(response)]
            x_count = x_count + 1
        elif(found):
            x_count = x_count + 1
            response = response[found+1:len(response)]


    #Info
    print(response[0:12])
    #Questions
    current = response[12:len(response)]
    print(response[12:20])

    #Answers RRs
    print(response[20:28])
    #Authority RRs
    print(response[28:36])
    #Additional RRs
    print(response[36:44])
    #Queries
    #Name && Name Length && Label Count
    print(response[44:68])
    #Type
    print(response[68:76])
    #Class
    print(response[76:84])
    rest = response[84:(len(response))]
    #Answer* (1 in this case)
    if(answers > 0):
        #Name
        print(response[84:92])
        #Type
        print(response[92:100])
        #Class
        print(response[100:108])
        #Time to live
        print(response[108:121])
        #Data length
        print(response[121:129])
        #Address
        print(response[129:142])
    #Authoritative nameservers (4 in this case)
    if(authority > 0):
        #5 first types of data is the same as in Answer*
        #Instead of Address there is Name Server
        print('nada')

    #Additional records (6 in this case)
    if(additional > 0):
        #The same as in Answer*
        print('nada')
    print(response[142:len(response)])

def ip_decoder(message1, message2, message3, message4):
    ip1 = ord(message1) if len(message1) == 1 else int(message1, 16)
    ip2 = ord(message2) if len(message2) == 1 else int(message2, 16)
    ip3 = ord(message3) if len(message3) == 1 else int(message3, 16)
    ip4 = ord(message4) if len(message4) == 1 else int(message4, 16)
    ip = str(ip1) + '.' + str(ip2) + '.' + str(ip3) + '.' + str(ip4)
    return ip


def name_decoder(message, pos, length):
    if(message[pos] == '0c'):
        return('cs.fiu.edu')
    else:
        pos = message.index('c0', pos)
        word = ''
        if(message[pos] == message[pos + 2]):
            while(len(message[pos - 1]) != 2):
                pos -= 1
                word = message[pos] + word
            word = word + '.cs.fiu.edu'
            return(word)
        else:
            return('FIX THIS decoder')


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
    pos = 0
    pos_list = []
    while(Answers != 0):
        pos = message.index('c0', pos)
        pos_list.append(pos)
        pos += 1
        name = name_decoder(message, pos, 0)
        pos = message.index('c0', pos)
        ip = ip_decoder(message[pos-4], message[pos-3], message[pos-2], message[pos-1])
        print('\tName : ' + name + '\t' + 'IP : ' + ip)
        Answers -= 1
        
    print('Authoritive section:')
    while(INS != 0):
        pos = message.index('c0', pos)
        pos_list.append(pos) #Look at the position since 'c0' is repeated
        pos += 1
        name = name_decoder(message, pos, 0)
        pos += 1
        server = name_decoder(message, pos, 0)
        print('\tName : ' + name + '\t' + 'Name Server : ' + server)
        aux = message.index('c0', pos)
        pos = aux if (message[aux] != message[aux+2]) else (aux+1)
        INS -= 1
    
    print('Additional Information section:')
    while(AIR != 0):

        AIR -= 1



def organize(response, extra):
    message = []
    message.append(response[2])
    message.append(response[3])
    count = 0
    word = ''
    while(count < len(response) - 1):
        count = count + 1
        if(response[count] == 'x'):
            word = response[count + 1:count + 3]
            message.append(word)
            count = count + 3
            if(response[count] != '\\'):
                while((response[count] != '\\') & (count < len(response) - 1)):
                    message.append(response[count])
                    count = count + 1
    #display(message, extra)
    print(message)
    #print(len(message))
    #print(message[56])


print('---------------------')
Name = 'cs.fiu.edu'
Port = 53
#extra = '202.12.27.33'
#extra = 'c.edu-servers.net'
#extra = 'nameserver2.fiu.edu'

extra = 'sagwa-ns.cs.fiu.edu'
extra2 = '131.94.130.238'

mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
request = bytes.fromhex('43470100000100000000000002637303666975036564750000010001')
mysocket.sendto(request,(extra, Port))
#response = bytes.decode(mysocket.recvfrom(1024))
response = (mysocket.recvfrom(521))
print(response)
#dictionary(str(response[0]), extra)
organize(str(response[0]), extra)