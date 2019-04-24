#Back End server 

from socket import *

Host = ''
Port = 4595
socket1 = socket(AF_INET, SOCK_DGRAM)
socket1.bind((Host,Port))
connectedClients=[]
   
while 1:
	data, address = socket1.recvfrom(2048)
	request = data.split("!")
	if request[0] == "add":
		new_client = eval(request[1])
		if new_client not in connectedClients:
			connectedClients.append(new_client)
	elif request[0] == "message":
		print(data)
		for i in range(len(connectedClients)):
			if (connectedClients[i] != eval(request[1])):
				socket1.sendto(request[1]+":"+request[2],connectedClients[i])
	elif request[0] == "SYN-SENT":
		socket1.sendto("SYN-RECEIVED", address)
	else:
		print("no case matched")
