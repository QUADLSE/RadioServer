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
                            #data = struct.unpack('ffffff', self.MsgBuff.Payload)
                            #print(data)
                            #data2 = struct.pack('ffffff', data[0],data[1],data[2],data[3],data[4],data[5])                     
                            protocol.sendLine(self.MsgBuff.Payload)
                            #print(data2)