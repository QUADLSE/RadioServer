from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver


class RadioReceiver(LineReceiver):
    from comms import Msg

    MsgBuff = Msg()
    
    def __init__(self, factory):
        self.MetaFactory = factory
        self.setRawMode()
        self.MetaFactory.radio = self
        
    def connectionMade(self):
        print 'SerialPort connected' 
        
    def connectionLost(self, reason):
        print('SerialPort disconnected')

    def rawDataReceived(self,data):
        for c in data:
            if (self.MsgBuff.NewByte(c)):
                #self.MsgBuff.Show()                 
                for clientType, protocol in self.MetaFactory.clients.iteritems():
                    if self.MsgBuff.HeaderNames[self.MsgBuff.DataType] == clientType:
                        #protocol.sendLine(self.MsgBuff.Payload)
                        protocol.transport.write(self.MsgBuff.Payload)             

class QuadComms(LineReceiver):

    def __init__(self, factory, dataType, address):
        #self.factory = factory
        self.LocalAdress = address
        self.clients = factory.clients
        self.dataType = dataType
        self.radio = factory.radio
        
    def connectionMade(self):
        print 'Accepted client for ' + self.dataType 
        self.type = self.dataType
        self.clients[self.dataType] = self
        
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
        from comms import Msg
        
        print '<' + self.dataType + '>'+ line
        MsgBuff = Msg()
        MsgBuff.Fill(0xBB, self.LocalAdress, Msg.NamesToCode[self.dataType], line)
        
        MsgBuff.Send(self.radio.transport.write)        
        #self.radio.sendLine('HOLA!')
        #self.radio.transport.write('ABC')
        #self.radio.sendLine("A!")
        '''
        for c in self.clients:
            if self.clients[c]!=self:
                self.clients[c].sendLine(line)
        ''' 
      
         
class TelemetryFactory(ServerFactory):
    protocol = QuadComms
    
    def __init__(self,factory):
        #self.clients = clients
        self.LocalAdress = 0xAA
        self.factory = factory
        pass
                
    def buildProtocol(self, addr):
        print addr
        r = QuadComms(self.factory,  'TELEMETRY', self.LocalAdress)
        return r

class DebugFactory(ServerFactory):
    protocol = QuadComms
    
    def __init__(self,factory):
        #self.clients = clients
        self.LocalAdress = 0xAA
        self.factory = factory        
               
    def buildProtocol(self, addr):
        print addr
        r = QuadComms(self.factory, 'DEBUG', self.LocalAdress)
        return r

class ControlFactory(ServerFactory):
    protocol = QuadComms
    
    def __init__(self,factory):
        #self.clients = clients
        self.LocalAdress = 0xAA
        self.factory = factory        
               
    def buildProtocol(self, addr):
        print addr
        r = QuadComms(self.factory, 'CONTROL', self.LocalAdress)
        return r    
    
class MetaFactory():
    factories = {}  
    clients = {}
    radio = None
        
    def __init__(self):
        #self.factories['TELEMETRY'] = TelemetryFactory(self, self.LocalAdress)
        #self.factories['DEBUG'] = DebugFactory(self, self.LocalAdress)
        self.factories['TELEMETRY'] = TelemetryFactory        
        self.factories['DEBUG'] = DebugFactory
        self.factories['CONTROL'] = ControlFactory
        self.clients =   {}
        
    def getFactory(self,dataType):
        if (self.factories.has_key(dataType)):
            return self.factories[dataType]
        else:
            return None