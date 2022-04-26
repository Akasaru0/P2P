from ast import arg
import sys, socket,threading,time

PORT_HOST = sys.argv[3]
PORT_DIST = sys.argv[2]
IP_HOST = "0.0.0.0"
IP_DIST = "192.168.1.98"

client_connect = False

def th_server():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((IP_HOST,int(PORT_HOST)))
    print("Server listen to "+IP_HOST+":"+PORT_HOST)
    server.listen()
    conn, addr = server.accept()

    global IP_DIST
    IP_DIST = ""+addr[0]

    global client_connect
    client_connect = True

    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            print(data.decode())
            if not data:
                break
    print("Client lost")

def th_client():
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((IP_DIST,int(PORT_DIST)))
    print("Client send to :"+IP_DIST+":"+PORT_DIST)    
    global client_connect
    client_connect = True
    while True:
        usr = input("")
        client.sendall(usr.encode())



if __name__ == '__main__':

    if sys.argv[1] == "s":
        thread_server = threading.Thread(target=th_server,args=())
        thread_server.start()
        print("(1) Server Started")
    if sys.argv[1] == "c":
        thread_client = threading.Thread(target=th_client,args=())
        thread_client.start()
        print("(1) Client Started")
    while True:
        if client_connect == True:
            if sys.argv[1] == 'c':
                thread_server = threading.Thread(target=th_server,args=())
                thread_server.start()
                print("(2) Server Started")
                break
            if sys.argv[1] == 's':
                time.sleep(2)
                thread_client = threading.Thread(target=th_client,args=())
                thread_client.start()
                print("(2) Client Started")
                break