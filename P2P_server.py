from twisted.internet import reactor, endpoints
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import ServerFactory



class P2PChat(LineReceiver):
    def __init__(self, users):
        self.users = users

    def connectionMade(self):
        self.transport.write(b'SERVER CONNECT\n')
        self.transport.write(b'What you name?\n')
        self.users.update({'':self})

    shet =0
    def lineReceived(self, line):

        def WriteNameUser(data):
            data = data.decode("UTF-8")
            if len(self.users) >0:
                if data in self.users.keys():
                    self.transport.write(b'NAME IS TAKEN\n')
                else:
                    self.users.pop('')
                    self.users.update({data:self})
            else:
                self.users.update({data: self})

        if '' in self.users.keys():
            WriteNameUser(line)

        self.transport.write(b'select user\n')
        self.transport.write(' '.join(self.users.keys()).encode("utf-8"))


        def UserVerification(line):
            name = line.decode("utf-8")
            if name in self.users.keys():
                Name = self.users.get(name)
                return Name
            else:
                self.transport.write(b'User is not found')
                return 1

        def SendMessange(name):
            name.transport.write(b'hi')

        if self.shet > 0:
            if UserVerification(line) !=1:
                SendMessange(UserVerification(line))

        self.shet += 1




class P2PChatFactory(ServerFactory):
    def __init__(self):
        self.users = {}
    def buildProtocol(self, addr):
        return P2PChat(self.users)


if __name__=="__main__":
    endpoints.serverFromString(reactor, "tcp:8051").listen(P2PChatFactory())
    reactor.run()