from socket import *
import threading
Host = ''

Port1 = 4790
BEPort1 = 4791
BEPort2 = 4792
BEPort3 = 4793
BEPort4 = 4794
Port3=4792

flagForConnectedPrimaryBEserver1 = 0
flagForconnectedSecondaryBEserver1 = 0
flagForConnectedPrimaryBEserver2 = 0
flagForconnectedSecondaryBEserver2 = 0

# clients
connectedClients=[]

file1=open('configfile1.txt','r')
for line in file1:
	linelist = line.split()
	if linelist[0] == "primary1":
		connectedPrimaryBEserver1 = linelist[1]
	if linelist[0] == "primary2":
		connectedPrimaryBEserver2 = linelist[1]
	if linelist[0] == "secondary1":
		connectedSecondaryBEserver1 = linelist[1]
	else:
		connectedSecondaryBEserver2 = linelist[1]

socket1 = socket(AF_INET, SOCK_DGRAM)
socket2 = socket(AF_INET, SOCK_DGRAM)
# socket1.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# socket2.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
socket1.bind((Host,Port1))
socket2.bind((Host,Port3))
socket1.settimeout(5.0)

def serverside(): 
	# global flagForConnectedPrimaryBEserver, flagForconnectedSecondaryBEserver
	while 1:
		data = "SYN-SENT"
		socket1.sendto(data.encode('utf-8'),(connectedPrimaryBEserver1, BEPort1))

		try:
			data2, address = socket1.recvfrom(2048)
			print(data)
			if data2 == "SYN-RECEIVED":
				flagForConnectedPrimaryBEserver1 = 1
		except Exception:
			flagForConnectedPrimaryBEserver1 = 0

		socket1.sendto(data.encode('utf-8'),(connectedPrimaryBEserver2, BEPort2))
		try:
			data3, address = socket1.recvfrom(2048)
			if data3 == "SYN-RECEIVED":
				flagForConnectedPrimaryBEserver2 = 1
		except Exception:
			flagForConnectedPrimaryBEserver2 = 0

		socket1.sendto(data.encode('utf-8'),(connectedSecondaryBEserver1, BEPort3))
		try:
			data4, address = socket1.recvfrom(2048)
			if data4 == "SYN-RECEIVED":
				flagForconnectedSecondaryBEserver1 = 1
		except Exception:\
			flagForconnectedSecondaryBEserver1 = 0

		socket1.sendto(data.encode('utf-8'),(connectedSecondaryBEserver2, BEPort4))
		try:
			data5, address = socket1.recvfrom(2048)
			if data5 == "SYN-RECEIVED":
				flagForconnectedSecondaryBEserver2 = 1
		except Exception:
			flagForconnectedSecondaryBEserver2 = 0

def clientside():
	global flagForConnectedPrimaryBEserver, flagForconnectedSecondaryBEserver
	while 1:
		data, address = socket2.recvfrom(2048)
   
		if (address not in connectedClients):
			print("New Client is", address)
			connectedClients.append(address)
			update_data="add!"+str(address)
			if flagForConnectedPrimaryBEserver == 1 and flagForconnectedSecondaryBEserver == 1:
				socket1.sendto(update_data.encode('utf-8'),(connectedPrimaryBEserver, BEPort1))
				socket1.sendto(update_data.encode('utf-8'),(connectedSecondaryBEserver, BEPort2))
			elif flagForconnectedSecondaryBEserver == 1 and flagForConnectedPrimaryBEserver == 0:
				socket1.sendto(update_data.encode('utf-8'),(connectedSecondaryBEserver, BEPort2))
			elif flagForConnectedPrimaryBEserver == 1 and flagForconnectedSecondaryBEserver == 0:
				socket1.sendto(update_data.encode('utf-8'),(connectedPrimaryBEserver, BEPort1))
			else:
				print("clientside add::no servers active")

		if flagForConnectedPrimaryBEserver == 1:
			data="message!"+str(address)+"!"+data
			socket1.sendto(data.encode('utf-8'),(connectedPrimaryBEserver, BEPort1))
		elif flagForconnectedSecondaryBEserver == 1:
			data="message!"+str(address)+"!"+data
			socket1.sendto(data.encode('utf-8'),(connectedSecondaryBEserver, BEPort1))
		else:
			data="message!"+str(address)+"!"+data

	
def updateClient():
	global flagForConnectedPrimaryBEserver, flagForconnectedSecondaryBEserver
	while 1:
		for i in range(len(connectedClients)):
			update_data="add!"+str(connectedClients[i])
			socket1.sendto(update_data.encode('utf-8'),(connectedPrimaryBEserver, BEPort1))
			socket1.sendto(update_data.encode('utf-8'),(connectedSecondaryBEserver, BEPort2))
			socket1.sendto(update_data.encode('utf-8'),(connectedSecondaryBEserver, BEPort3))
			socket1.sendto(update_data.encode('utf-8'),(connectedSecondaryBEserver, BEPort4))
		# while threading.active_count() > 150:
		# 	threading.Timer.sleep(5)
	threading.Timer(3,updateClient).start()

first = threading.Thread(target = serverside)
print(connectedClients)
second = threading.Thread(target = clientside)
third = threading.Thread(target = updateClient)

second.start()
third.start()
first.join()
second.join()
third.join()
sys.exit()
