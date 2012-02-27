from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver


class RadioReceiver(LineReceiver):
    from comms import Msg

    MsgBuff = Msg()
    
    def __init__(self, factory):
        self.MetaFactory = factory
        self.setRawMode()
        
    def connectionMade(self):
        print 'SerialPort connected' 
        
    def connectionLost(self, reason):
        print('SerialPort disconnected')

    def rawDataReceived(self,data):
        for c in data:
            if (self.MsgBuff.NewByte(c)):
                #self.MsgBuff.Show()                
                 
                for clientType, protocol in self.MetaFactory.clients.iteritems():
                    
                    #print clientType
                    #print protocol                
                
                    #if protocol != self:
                    if self.MsgBuff.HeaderNames[self.MsgBuff.DataType] == clientType:
                        protocol.sendLine(self.MsgBuff.Payload)
                

class QuadComms(LineReceiver):

    def __init__(self, clients, dataType):
        #self.factory = factory
        self.clients = clients
        self.dataType = dataType
        
    def connectionMade(self):
        print 'Accepted client for ' + self.dataType 
        self.type = self.dataType
        self.clients[self.dataType] = self
        print self.clients
        
    def connectionLost(self, reason):
        print(self.dataType + ' Client disconnected')
        if self.clients.has_key(self.dataType):
            del self.clients[self.dataType]

    def lineReceived(self, line):
        self.handle_Data(line)
            
    def handle_GetDataType(self,DataType):
        
        if self.clients.has_key(DataType):
            self.sendLine("ERROR: " + self.dataType + " ALREADY TAKEN!")
            return
        
    def handle_Data(self,line):
        print '<' + self.dataType + '>'+ line
        '''
        for c in self.clients:
            if self.clients[c]!=self:
                self.clients[c].sendLine(line)
        ''' 
      
         
class TelemetryFactory(ServerFactory):
    protocol = QuadComms
    
    def __init__(self,factory):
        #self.clients = clients
        self.factory = factory
        pass
                
    def buildProtocol(self, addr):
        print addr
        r = QuadComms(self.factory.clients,  'TELEMETRY')
        return r

class DebugFactory(ServerFactory):
    protocol = QuadComms
    
    def __init__(self,factory):
        #self.clients = clients
        self.factory = factory
        pass
               
    def buildProtocol(self, addr):
        print addr
        r = QuadComms(self.factory.clients, 'DEBUG')
        return r
    
class MetaFactory():
    servers = {}
    factories = {}  
    clients = {}
    
    def __init__(self):
        self.factories['TELEMETRY'] = TelemetryFactory(self)
        self.factories['DEBUG'] = DebugFactory(self)
        self.clients =   {}
        
    def getFactory(self,dataType):
        if (self.factories.has_key(dataType)):
            return self.factories[dataType]
        else:
            return None
    
    def addFactory(self,dataType, factory):
        self.factories['TELEMETRY'] = factory