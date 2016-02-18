import tkinter, socket, time, sys, configparser, threading
from time import localtime, strftime
from threading import Thread

class Chat(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        
        self.LoadConfig()
        host = self.ConfigSectionMap("SectionConnection")['host']
        port = self.ConfigSectionMap("SectionConnection")['port']

        port = int(port)
        type(port)

        self.Connect(host,port)
        self.Initialize()
 
    def Initialize(self):        
        self.grid()
        self.i = 2
        
        self.headerText = tkinter.StringVar()
        self.entryText = tkinter.StringVar()

        label = tkinter.Label(self,textvariable=self.headerText,
                              anchor="w",fg="Black")
        label.grid(column=0,row=0,sticky='EW')
        self.headerText.set(u"Keys: 'Enter' = send, 'Del' = clear text     Commands: '/quit' or '/q' = close program")
        
        self.entry = tkinter.Entry(self,textvariable=self.entryText,width=150)
        self.entry.grid(column=0,row=1,sticky='EW')
        self.entryText.set(u"Enter text here")

        button = tkinter.Button(self, text=u"Send",
                                command=self.Send)
        button.grid(column=1,row=1)

        self.entry.bind("<Return>", self.OnPressEnter)
        self.entry.bind("<Delete>", self.OnPressDelete)

    def OnPressEnter(self,event):
        self.Send()

    def OnPressDelete(self,event):
        self.Clear()

    def Send(self):
        if self.entryText.get() == "":
            print("\nError: attempting to send null value")
        else:
            print("\nSending: ", "'" + self.entryText.get() + "'")
            message = self.entryText.get().encode('utf-8')
            self.s.send(message)
            print(type(message), message)

            self.Clear()

    def Receive(self):
        while True:
            self.r = self.s.recv(128)
            self.a = self.r.decode('utf-8')
            
            if self.a == "/quit":
                self.Exit()
                pass
            elif self.a == "/q":
                self.Exit()
                pass
            
            print("Received: ", "'" + self.a + "' \nEncoding:")
            print(type(self.a), len(self.a))

            self.labelVariable = tkinter.StringVar()
            label = tkinter.Label(self,textvariable=self.labelVariable,
                              anchor="w",fg="Black",bg="White")
            label.grid(column=0,row=self.i,columnspan=2,sticky='EW')
            self.time = strftime("%H:%M:%S", localtime())
            self.labelVariable.set(self.time + ": " + self.a)

            self.i = self.i + 1

    def Clear(self):
        print("\nClearing entry")
        self.entryText.set("")
        return

    def Connect(self,host,port):
        self.s = socket.socket()
        print("Connecting to server...")
        
        while True:
            try:
                self.s.connect((host, port))
                print("Connected to: " + host + ":" + str(port))
                break
            except:
                print("Retrying connection to server...")
                time.sleep(1)

    def LoadConfig(self):
        self.cfg = configparser.ConfigParser()
        self.cfg.read("config.ini")
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

    def Exit(self):
        print("Client stopped...")
        self.s.close()
        app.destroy()
        sys.exit()

if __name__ == "__main__":
    app = Chat(None)
    app.title('Chat')
    app.protocol('WM_DELETE_WINDOW', app.Exit)
    threadReceive = threading.Thread(target=app.Receive)
    threadReceive.start()
    app.mainloop()
