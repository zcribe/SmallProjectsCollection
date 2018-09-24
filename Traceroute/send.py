import socket

udp_ip = '127.0.0.1'
port = '5005'
message = 'Test 12'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(message, (udp_ip, port))
