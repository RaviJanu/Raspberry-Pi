from socket import *
import sys
import time



class socket_class:
    def setupServer(self,host,port):
            self.s = socket(AF_INET,SOCK_STREAM)
            print("Socket created.")
            try:
                    self.s.bind((host, port))
                    print 'Server Init done with IP "' + host + '" PORT ' + str(port)
            except error as msg:
                    print(msg)
            print("Socket bind complete.")
            self.s.listen(5)                         # Allows 5 connection
            time.sleep(2)
            

    def setupConnection(self):
            print("Waiting for connection...")
            self.conn, address = self.s.accept()
            print("Connected to: " + address[0] + ":" + str(address[1]))
            time.sleep(2)

    def send_data_conn(self,data):
            self.conn.sendall(data)
            

    def close_connection(self):
            print ('connction closed')
            self.s.close()
            

if __name__ == "__main__":              # this is testing for server setup
    iot = socket_class()
    iot.setupServer('192.168.0.109',1234)
    iot.setupConnection()
    try:
        while True:
            iot.send_data_conn("hello world_")
            time.sleep(5)
    except KeyboardInterrupt:
        iot.close_connection()
