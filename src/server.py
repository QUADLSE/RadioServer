import ConfigParser
import Connections
from twisted.internet.serialport import SerialPort

#==========================================================================
# Main
#==========================================================================
if __name__ == "__main__":
    
    #HeadersPorts = {'SYSTEM':TYPE_SYSTEM,'CONTROL':TYPE_CONTROL,'DEBUG':TYPE_DEBUG,'TELEMETRY':TYPE_TELEMETRY}       
    #ser = serial.Serial() 
    
    M=Connections.MetaFactory()
    
    #=========================================================================
    # Config file reading
    #=========================================================================
    
    config = ConfigParser.RawConfigParser()
         
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
            
            Port  = config.get('Radio', 'SerialPort')
            Baudrate  = config.getint('Radio', 'Baudrate')
            Parity  = config.get('Radio', 'Parity')
            Databits  = config.getint('Radio', 'Databits')
            StopBits  = config.getint('Radio', 'Stopbits')
            
            print 'Port: '+ Port
            print 'BaudRate: '+ str(Baudrate)
            print 'Databits: '+ str(Databits)
            print 'Parity: '+ str(Parity)
            print 'StopBits: '+ str(StopBits)
            
            print 
            
            print 'Opening Serial port...',

            from twisted.internet import reactor          
            SerialPort(Connections.RadioReceiver(M), Port, reactor, baudrate=Baudrate)
            
            print '---------------------------------------------'
                
        elif section.find("Proxy")!=-1:
            print '### ' + section + " Section ###" 
            
            ProxyPort  = config.getint(section, 'Port')
            ProxyHeader  = config.get(section, 'Header')
            ProxyProtocol  = config.get(section, 'Protocol')
            
            print "port:" + str(ProxyPort)
            print "Header:" + ProxyHeader
            print "Protocol:" + ProxyProtocol
          

            from twisted.internet import reactor            
            f = M.getFactory(ProxyHeader)
            p = reactor.listenTCP(ProxyPort, f)
            #p = reactor.connectTCP( '',ProxyPort, factory=f)
            
            print
            print ProxyHeader + ' Server running'
            print '---------------------------------------------'
            
    #r = RadioConnection(f.clients)
    #SerialPort(r, Port, reactor, Baudrate)
    
    #=========================================================================
    # Main server thread
    #=========================================================================

    reactor.run()
    
