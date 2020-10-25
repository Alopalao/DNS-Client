import socket

def dictionary(response):
    count = 0
    queries = 1
    answers = 1
    authority = 4
    additional = 6
    #Info
    print(response[0:12])
    #Questions
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
#print(response[0])
dictionary(str(response[0]))