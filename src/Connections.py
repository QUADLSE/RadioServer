from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

class QuadComms(LineReceiver):

    def __init__(self, clients):
        self.clients = clients
        self.type = "NONE"
        self.state = "GET_DATA_TYPE"

    def connectionMade(self):
        print('Client connected. Asking for data type')
        self.sendLine("What data do you want?")
        

    def connectionLost(self, reason):
        print(self.type + ' Client disconnected')
        if self.clients.has_key(self.type):
            del self.clients[self.type]

    def lineReceived(self, line):
        if self.state == "GET_DATA_TYPE":
            self.handle_GetDataType(line)
        else:
            self.handle_Data(line)
            
    def handle_GetDataType(self,type):
        
        if self.clients.has_key(type):
            self.sendLine("ERROR: " + type + " ALREADY TAKEN!")
            return
        
        print 'Accepted client for ' + type 
        self.type = type
        self.clients[type] = self
        self.state = "DATA"
        
    def handle_Data(self,line):
        print '<' + self.type + '>'+ line
         

class ConnectionFactory(Factory):
    def __init__(self):
        self.clients = {}
        
    def buildProtocol(self, addr):
        return QuadComms(self.clients)
