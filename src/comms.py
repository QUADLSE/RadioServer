
import sys
import serial

class Msg:
    TYPE_SYSTEM, TYPE_CONTROL, TYPE_DEBUG, TYPE_TELEMETRY, TYPE_NULL = range(5)
    
    HeaderNames = ['SYSTEM','CONTROL','DEBUG','TELEMETRY']
    #HeaderNames = {'SYSTEM':TYPE_SYSTEM,'CONTROL':TYPE_CONTROL,'DEBUG':TYPE_DEBUG,'TELEMETRY':TYPE_TELEMETRY}
    
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
        
    def Send(self, ser):
        #TODO: Implement! 
        pass
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
        '''
        ser.write(bytes(self.SourceAddress))
        ser.write(bytes(self.DestAddress))
        ser.write(bytes(self.TimeStamp))
        ser.write(bytes(self.DataType))
        ser.write(bytes(self.DataLength))
        ser.write(bytes(self.Payload))
        ser.write(bytes(self.Checksum))
        '''
        