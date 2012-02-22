from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

class Connection(LineReceiver):

    def __init__(self, name):
        self.name = name

    def connectionMade(self):
        self.sendLine("Hello client!")
        print(self.name + ' Client connected')

    def connectionLost(self, reason):
        print(self.name + ' Client disconnected')

    def lineReceived(self, line):
        print self.name + ':' + line
        
    def handle_SendData(self,data):
        self.sendLine(data)
'''
    def handle_GETNAME(self, name):
        if self.users.has_key(name):
            self.sendLine("Name taken, please choose another.")
            return
        self.sendLine("Welcome, %s!" % (name,))
        self.name = name
        self.users[name] = self
        self.state = "CHAT"

    def handle_CHAT(self, message):
        message = "<%s> %s" % (self.name, message)
        for name, protocol in self.users.iteritems():
            if protocol != self:
                protocol.sendLine(message)
'''

class ConnectionFactory(Factory):
    def __init__(self,name):
        self.name = name
    def buildProtocol(self, addr):
        return Connection(self.name)