

from socket import *
import threading 
import sys

server_add=input('Please enter IP add')

data = ''
data = data.ljust(16,'^')

Port = 4690
socket1 = socket(AF_INET, SOCK_DGRAM)
socket1.sendto(data.encode('utf-8'), (server_add, Port))
print("enter data to sent to server")
def send_data():
	while 1:
		data = input("You:")
		data2 = data.upper()
		data3 = data2.ljust(16, '^')
		socket1.sendto(data3.encode('utf-8'), (server_add, Port))
		if data == "EXIT" or data == "exit":
			print("\n Exit chat")
			second.exit()
			socket1.close()
			break

def recv():
	while 1: 
		new_data, address = socket1.recvfrom(2048)
		new_data = new_data.split(':')
		if len(new_data[1]) == 16:
			new_data2 = new_data.split('^')
			print("\n", new_data2[0])
			if new_data2[0] ==  "EXIT" or new_data2[0] == "exit":
				print("\n Exit chat")
				first.exit()
				socket1.close()
				break
		else:
			continue

first = threading.Thread(target=send_data)
second = threading.Thread(target=recv)

first.start()
second.start()

first.join()
second.join()

sys.exit()
