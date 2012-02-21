import ConfigParser
import serial
import time
from comms import Msg

#==========================================================================
# Main
#==========================================================================
if __name__ == "__main__":
    
    ser = serial.Serial() 
    
    #=========================================================================
    # Config file reading
    #=========================================================================
    
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    
         
    print '---------------------------------------------'
    print 'Reading configuration file...',    
            
    try:
        config.read('config.cfg')
    except ConfigParser.Error, e:
        print e
        exit(1)
    
    if (len(config.sections())==0):
        print '[ERROR]: No sections found on config file'
    else:
        print '[OK]'
        
    print '---------------------------------------------'
    print 'Parsing sections...\n'
        
    for section in config.sections():
        
        if section =="Radio":
            print "### Radio Serial port Section ### \n"
            
            SerialPort  = config.get('Radio', 'SerialPort')
            Baudrate  = config.getint('Radio', 'Baudrate')
            Parity  = config.get('Radio', 'Parity')
            Databits  = config.getint('Radio', 'Databits')
            StopBits  = config.getint('Radio', 'Stopbits')
            
            print 'Port: '+ SerialPort
            print 'BaudRate: '+ str(Baudrate)
            print 'Databits: '+ str(Databits)
            print 'Parity: '+ str(Parity)
            print 'StopBits: '+ str(StopBits)
            
            print 
            
            print 'Opening Serial port...',
            
            # connect to serial port
            ser.port     = SerialPort
            ser.baudrate = Baudrate
            ser.parity   = serial.PARITY_NONE
            ser.rtscts   = False
            ser.xonxoff  = False
            ser.timeout  = 1     # required so that the reader thread can exit
            
            try:
                ser.open()
                ser.flush()
                print "[OK]"
            except serial.SerialException, e:
                print "[FAILED]"
                print(e)
                print("No connection to the QUAD will be made. Debug Mode\n")
                
            print '---------------------------------------------'
                
        elif section.find("Proxy")!=-1:
            #print "PROXY SOCKET CONFIG"       
            print '### ' + section + " Section ###" 
            '''
            ProxyPort  = config.getint(section, 'Port')
            ProxyHeader  = config.get(section, 'Header')
            ProxyProtocol  = config.get(section, 'Protocol')
            
            print "port:" + str(ProxyPort)
            print "Header:" + ProxyHeader
            print "Protocol:" + ProxyProtocol
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("", ProxyPort))


            s.listen(1)            
            
            q[ProxyHeader] = Queue.Queue()
            SocketStatus[ProxyHeader] = 'DISCONNECTED'
             
            t = threading.Thread(target=envia, name='env', args=(s,q[ProxyHeader],ProxyHeader))
            t.start()
            
            #t = threading.Thread(target=recive, name='env', args=(s)
            #t.start()
             
            print
            print 'Thread running'        
            print '---------------------------------------------'
            '''
           
    #=========================================================================
    # Main server thread
    #=========================================================================       
    MsgBuff = Msg()
    
    while ser.isOpen():
    #    m.Send(ser);
        time.sleep(0.0005)
        data = ser.read(1)              # read one, blocking
        if data:
            if (MsgBuff.NewByte(data)):
                MsgBuff.Show()