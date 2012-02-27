import sys

class Msg:
    TYPE_SYSTEM, TYPE_CONTROL, TYPE_DEBUG, TYPE_TELEMETRY, TYPE_NULL = range(5)
    
    HeaderNames = ['SYSTEM','CONTROL','DEBUG','TELEMETRY']
    NamesToCode = {'SYSTEM':TYPE_SYSTEM,'CONTROL':TYPE_CONTROL,'DEBUG':TYPE_DEBUG,'TELEMETRY':TYPE_TELEMETRY}
    
    SourceAddress = 0;
    DestAddress = 0
    TimeStamp = 0
    DataType = TYPE_NULL
    DataLength = 0
    Payload = "NULL"
    Checksum = 0 
    
    state = "HEADER"
             
    def NewByte(self,data):

        if self.state == "HEADER":
            
            if ord(data) == 0xEA:
                self.bytesReaded = 0
                self.Payload = ""
                self.state = "SOURCE"
            return False
                    
        elif self.state == "SOURCE":
            self.SourceAddress = ord(data)
            self.state = "DEST"
            return False
            
        elif self.state == "DEST":
            self.DestAddress = ord(data)
            self.state = "TIME"
            return False
            
        elif self.state == "TIME":
            self.TimeStamp = ord(data)
            self.state  = "TYPE"
            return False
            
        elif self.state == "TYPE":
            self.DataType = ord(data)
            self.state = "LENGTH"
            return False
        
        elif self.state == "LENGTH":
            self.DataLength = int(ord(data))
            self.state = "PAYLOAD"
            return False
            
        elif self.state == "PAYLOAD":
            self.Payload = self.Payload + data
            self.bytesReaded = self.bytesReaded + 1
            
            if self.bytesReaded == self.DataLength:
                self.state = "CHECKSUM"
            
            return False
        
        elif self.state == "CHECKSUM":
            self.Checksum = ord(data)
            self.state = "HEADER"
        
            #check for correct Checksum
            if self.CalculateChecksum() == self.Checksum:
                return True   
            else:               
                sys.stderr.write("Invalid msg received\r\n")
                return False
                    
    def Show(self):
        print "-----------------------------------------------"
        print "Source:" + hex((self.SourceAddress))
        print "Dest:" + hex((self.DestAddress))
        print "TimeStamp:" + hex((self.TimeStamp))
        print "Data Type:" + self.HeaderNames[self.DataType] #hex((self.DataType))
        print "Data Lenght:" + str((self.DataLength))
        print "Data:" + self.Payload
        print "Checksum:" + hex((self.Checksum)) 
        print "-----------------------------------------------"
    
    def CalculateChecksum(self):
        return (self.SourceAddress + self.DestAddress + self.TimeStamp + self.DataLength)%256
    
    def Fill(self, Dest, Source, DataType, Data):
        self.SourceAddress = Source
        self.DestAddress = Dest
        self.Payload = Data
        self.DataType = DataType
        self.DataLength = len(Data)
        self.TimeStamp = 0x55
        self.Checksum = self.CalculateChecksum()
    '''    
    def Pack(self):
        return pack('bbbbbsb',bytes(self.SourceAddress),bytes(self.DestAddress),bytes(self.TimeStamp),bytes(self.DataType),bytes(self.DataLength),(self.Payload),bytes(self.Checksum))
    '''
            
    def Send(self, method):
        #TODO: Implement! 
        from struct import pack
        """
        print "-----------------------------------------------"
        print "Source:" + hex((self.SourceAddress))
        print "Dest:" + hex((self.DestAddress))
        print "TimeStamp:" + hex((self.TimeStamp))
        print "Data Type:" + hex((self.DataType))
        print "Data Lenght:" + str((self.DataLength))
        print "Data:" + self.Payload
        print "Checksum:" + hex((self.Checksum)) 
        print "-----------------------------------------------"
        """
        method(pack('B',0xEA))
        method(pack('B',self.SourceAddress))
        method(pack('B',self.DestAddress))
        method(pack('B',self.TimeStamp))
        method(pack('B',self.DataType))
        method(pack('B',self.DataLength))
        method((self.Payload))
        method(pack('B',self.Checksum))
        
        