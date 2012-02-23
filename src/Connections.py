from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

class QuadComms(LineReceiver):

    def __init__(self, clients):
        self.radio = None
        self.clients = clients
        self.type = "NONE"
        self.state = "GET_DATA_TYPE"
        
    def connectionMade(self):
        print('Client connected. Asking for data type')
        #self.sendLine("What data do you want?")
        

    def connectionLost(self, reason):
        print(self.type + ' Client disconnected')
        if self.clients.has_key(self.type):
            del self.clients[self.type]

    def lineReceived(self, line):
        if self.state == "GET_DATA_TYPE":
            self.handle_GetDataType(line)
        else:
            self.handle_Data(line)
            
    def handle_GetDataType(self,DataType):
        
        if self.clients.has_key(DataType):
            self.sendLine("ERROR: " + DataType + " ALREADY TAKEN!")
            return
        
        print 'Accepted client for ' + DataType 
        self.type = DataType
        self.clients[DataType] = self
        self.state = "DATA"
        
    def handle_Data(self,line):
        print '<' + self.type + '>'+ line
      
         

class ConnectionFactory(Factory):
    RadioConn = None
    def __init__(self):
        self.clients = {} 
        
    def buildProtocol(self, addr):
        r = QuadComms(self.clients)
        self.RadioConn = r
        return r
