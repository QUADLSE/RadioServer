import ConfigParser
from comms import Msg
import Connections
from RadioReceiver import RadioConnection
from twisted.internet.serialport import SerialPort
from twisted.internet import reactor
from twisted.application import service, internet

#==========================================================================
# Main
#==========================================================================
if __name__ == "__main__":
    
    from twisted.internet import protocol
    
    #ser = serial.Serial() 
    
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
            
            print "[OK]"
            print '---------------------------------------------'
                
        elif section.find("Proxy")!=-1:
            print '### ' + section + " Section ###" 
            
            ProxyPort  = config.getint(section, 'Port')
            ProxyHeader  = config.get(section, 'Header')
            ProxyProtocol  = config.get(section, 'Protocol')
            
            print "port:" + str(ProxyPort)
            print "Header:" + ProxyHeader
            print "Protocol:" + ProxyProtocol
                  
            f = Connections.ConnectionFactory()
            reactor.listenTCP(ProxyPort, f)
            
            print
            print ProxyHeader + ' Server running'
            print '---------------------------------------------'
            
    SerialPort(RadioConnection(f.clients), Port, reactor, Baudrate)
     
    #=========================================================================
    # Main server thread
    #=========================================================================
    reactor.run()
    
