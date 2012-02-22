from twisted.protocols.basic import LineReceiver
from comms import Msg
import struct

class RadioConnection(LineReceiver):
    MsgBuff = Msg()
    
    def __init__(self):
        print 'created'
        self.setRawMode()
    
    def rawDataReceived(self,data):
        for c in data:
            if (self.MsgBuff.NewByte(c)):
                #self.MsgBuff.Show()
                if (self.MsgBuff.DataType==self.MsgBuff.TYPE_TELEMETRY):
                    print struct.unpack('ffffff', self.MsgBuff.Payload)
