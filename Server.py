import socket, time, configparser, threading
from time import localtime, strftime
from threading import Thread

class Config(object):
    def __init__(self):
        self.LoadConfig()
        self.host = self.ConfigSectionMap("SectionConnection")['host']
        self.port = self.ConfigSectionMap("SectionConnection")['port']

        self.port = int(self.port)
        type(self.port)

    def LoadConfig(self):
        self.cfg = configparser.ConfigParser()
        self.cfg.read("server_config.ini")
        self.cfg.sections()
    
    def ConfigSectionMap(self,section):
        dic = {}
        options = self.cfg.options(section)
        for option in options:
            try:
                dic[option] = self.cfg.get(section, option)
            except:
                print("exception on %s!" % option)
                dic[option] = None
        return dic

class Server():
    print("Server started")
    time = strftime("%d-%m-%Y %H:%M:%S: ", localtime())
    print("\n" + time + "Server started", file=open("server.log",'a'))

    def Connect(self,host,port):
        config = Config()
        self.s = socket.socket()
        self.s.bind((config.host, config.port))

    def Listener(self):        
        while True:
            try:
                self.s.listen(1)
                print("Connection Waiting...")
                
                self.sc, self.addr = self.s.accept()
                print("Connection Matched!")

                self.s.listen(1)
                print("Connection2 Waiting...")

                self.sc2, self.addr2 = self.s.accept()
                print("Connection2 Matched!")
                break
            except Exception as se:
                print(type(se), se)
                time.sleep(1)
            
    def DataHandler(self):            
        while True:
            try:
                self.received = self.sc.recv(128)                
                print(type(self.received), self.received)
                
                a = self.received.decode('utf-8')
                print(type(a), len(a))
                print(self.time + a, file=open("server.log",'a'))
                
                message = self.received
                self.Send(message)
    
                if a == "/quit":
                    self.sc.close()
                elif a == "/q":
                    self.sc.close()                                
            except:
                time.sleep(1)

    def DataHandler2(self):
        while True:
            try:
                self.received2 = self.sc2.recv(128)
                print(type(self.received2), self.received2)

                a2 = self.received2.decode('utf-8')
                print(type(a2), len(a2))
                print(self.time + a2, file=open("server.log",'a'))
                
                message = self.received2
                self.Send(message)

                if a2 == "/quit":
                    self.sc2.close()
                elif a2 == "/q":
                    self.sc2.close()
            except:
                time.sleep(1)

    def Send(self,message):
        self.sc.send(message)
        self.sc2.send(message)

    def Exit(self):
        print("\nServer closed")
        print(self.time + "Server closed", file=open("server.log",'a'))
        self.s.close()

if __name__ == "__main__":
    server = Server()
    
    config = Config()
    host = config.host
    port = config.port
    server.Connect(host,port)
    
    threadListener = threading.Thread(target=server.Listener)
    threadDataHandler = threading.Thread(target=server.DataHandler)
    threadDataHandler2 = threading.Thread(target=server.DataHandler2)
    threadListener.start()
    threadDataHandler.start()
    threadDataHandler2.start()
    
