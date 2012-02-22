from twisted.protocols.basic import LineReceiver
from comms import Msg
import struct

class RadioConnection(LineReceiver):
    MsgBuff = Msg()
    
    def __init__(self, clients):
        self.setRawMode()
        self.clients = clients
    
    def rawDataReceived(self,data):
        for c in data:
            if (self.MsgBuff.NewByte(c)):
                #self.MsgBuff.Show()
                
                for clientType, protocol in self.clients.iteritems():
                    if protocol != self:
                        if self.MsgBuff.HeaderNames[self.MsgBuff.DataType] == clientType:
                        #protocol.sendLine(struct.unpack('ffffff', self.MsgBuff.Payload))
                            protocol.sendLine(self.MsgBuff.Payload)