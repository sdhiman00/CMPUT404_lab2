#!/usr/bin/env python3
import socket
import time
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#create a tcp socket
def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def main():
    host = 'www.google.com'
    port = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            
            #create a new socket 
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:
                remote_ip = get_remote_ip(host)
                proxy_socket.connect((remote_ip, port))

                p = Process(target=echo_handler, args=(proxy_socket, conn, addr))
                p.daemon = True
                p.start()
                print("Started Process", p)

            conn.close()

def echo_handler(proxy_socket, conn, address):
    #recieve data, wait a bit, then send it back
    send_full_data = conn.recv(BUFFER_SIZE)
    proxy_socket.sendall(send_full_data)
    proxy_socket.shutdown(socket.SHUT_WR)
    data = proxy_socket.recv(BUFFER_SIZE)
    time.sleep(0.5)
    conn.sendall(data)

if __name__ == "__main__":
    main()
