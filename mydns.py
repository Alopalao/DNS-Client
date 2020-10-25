import socket

def dictionary(response):


Name = 'cs.fiu.edu'
Port = 53
#53
#extra = '202.12.27.33'
#extra = 'c.edu-servers.net'
#extra = 'nameserver2.fiu.edu'
extra = 'sagwa-ns.cs.fiu.edu'
extra2 = '131.94.130.238'

mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#request = str.encode('Standard query 0x4347 A cs.fiu.edu')
#request = str.encode('dsmaf')
#request = str.encode('(' + Name + ', ' + extra2 + ', A, ttl')
#request = str.encode('CG..........cs.fiu.edu.....')
request = bytes.fromhex('43470100000100000000000002637303666975036564750000010001')
mysocket.sendto(request,(extra, Port))
#response = bytes.decode(mysocket.recvfrom(1024))
#print(response)
response = (mysocket.recvfrom(521))
#print(response)
dictionary(response[0])