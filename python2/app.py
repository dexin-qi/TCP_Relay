import socket
import time
import sys

class tcpRelay:
    def __init__(self):
        self.relaySocket=socket.socket()
        
    def openPort(self,serverPort):
        self.serverPort=serverPort
        
        self.serverAddr=("",self.serverPort)
        self.relaySocket.bind(self.serverAddr)
        self.relaySocket.listen(5)
        
        self.connection=0
        self.addr=0
        print("relaylisten working on *:"+str(self.serverPort))   
    
    def closePort(self):
        self.connection.close()
        
        self.relaySocket.shutdown(2)
        self.relaySocket.close()
    
    def hasUserConfigOrder(self):
        try:
            configOrder=input("order you need to give client :")
        except:
            print("wrong input! check if you have \"?")
            return 1
        
        if(configOrder=='exit'):
            print("we will stop server on *:"+str(self.serverPort))
            return 0
        else:
            self.connection.send(bytes(configOrder+"\n"))
            print(self.connection.recv(256))
            return 1
        
    def waitRelay(self):
        self.connection,self.addr=self.relaySocket.accept()
        print("client "+str(self.addr[0])+':'+str(self.addr[1])+" connect!")
        
    def userConfigMode(self):
        while self.hasUserConfigOrder():
            pass
    
    def writeRelay(self,state):
        if state:
            self.connection.send(bytes("AT+STACH0=1\n"))
        else:
            self.connection.send(bytes("AT+STACH0=0\n"))
        relayBack=self.connection.recv(256)
        if(relayBack == "OK\n"):
            print("relay write success")
        else:
            print(relayBack)
    
    def getRelayStatus(self):
        self.connection.send(bytes("AT+STACH0=?\n"))
        relayBack=self.connection.recv(256)
        order,relay=relayBack.split(':')
        status,timer=relay.split(',')
        return status
        
    def toggleRelay(self):
        self.writeRelay(self.getRelayStatus()=="0")

       
class debugger:
    def __init__(self):
        self.debugSocket=socket.socket()
        
    def openPort(self,serverPort):
        self.serverPort=serverPort
        
        self.serverAddr=("",self.serverPort)
        self.debugSocket.bind(self.serverAddr)
        self.debugSocket.listen(5)
        
        self.connection=0
        self.addr=0
        print("debugger working on *:"+str(self.serverPort))   
    
    def closePort(self):
        self.debugSocket.shutdown(2)
        self.debugSocket.close()
    
    def debuggerLeave(self):
        self.connection.close()
        print("debugger "+str(self.addr[0])+':'+str(self.addr[1])+" leave!")
        
    def waitDebugger(self):
        self.connection,self.addr=self.debugSocket.accept()
        print("debugger "+str(self.addr[0])+':'+str(self.addr[1])+" connect!")
    
    def getCmd(self):
        userCmd=self.connection.recv(1024)
        if userCmd == "SL":
            return 0
        elif userCmd == "SH":
            return 1
        elif userCmd == "TG":
            return 2
        elif userCmd == "EX":
            return -1
    

tr=tcpRelay()
db=debugger()

if len(sys.argv) is not 3:
    print("==============Sorry=============")
    print("=we cannot fig your parameters!=")
    trPort=input("=please input your relay_port :")
    dbPort=input("=please input your config_port:")
    print("================================")
else:
    trPort=sys.argv[1]  
    dbPort=sys.argv[2]
    #print(trPort+","+dbPort)

tr.openPort(int(trPort))
db.openPort(int(dbPort))

print("waiting relay connect...")
tr.waitRelay()
print("relay connected sucess!")

while True:
    db.waitDebugger()
    
    while True:
        cmd=db.getCmd()
        
        if(cmd==-1):
            db.debuggerLeave()
            break
        elif(cmd==0):
            tr.writeRelay(False)
        elif(cmd==1):
            tr.writeRelay(True)
        elif(cmd==2):
            tr.toggleRelay()
            
db.closePort()
tr.closePort()