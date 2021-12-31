from twisted.internet import reactor, endpoints
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import ServerFactory




class P2PChat(LineReceiver):
    def __init__(self, users):
        self.users = users
        self.name_user = False
        self.SelectName = 0

    def connectionMade(self):
        print('connect')
        self.transport.write(b'SERVER CONNECT\n')
        self.transport.write(b'What you name?\n')
        self.users.update({'':self})

    def dataReceived(self, data):

        def SelectUser():
            self.transport.write(b'select user:\n')
            self.transport.write(' '.join(self.users.keys()).encode("utf-8"))
            self.transport.write(b'\n')

        def UserVerification(line):
            name = line.decode("utf-8")
            if name[:-2] in self.users.keys():
                Name = self.users.get(name[:-2])
                self.SelectName = Name
            else:
                self.transport.write(b'User is not found\n')

        def SendMessange(data):
            name = self.SelectName
            for user in self.users.keys():
                if self.users.get(user) == self:
                    user = user.encode("UTF-8")
                    name.transport.write(b'messenge from:')
                    name.transport.write(user)
                    name.transport.write(b'  ')
                    name.transport.write(data)

        def WriteNameUser(data):
            data = data.decode("UTF-8")
            if len(self.users) >0:
                if data in self.users.keys():
                    self.transport.write(b'NAME IS TAKEN, ENTER AGAIN \n')
                else:
                    self.users.pop('')
                    self.users.update({data[:-2]:self})
                    self.name_user = True
            else:
                self.users.update({data[:-2]: self})
                self.name_user= True

        if self.name_user == False:
            WriteNameUser(data)
            if self.name_user == True:
                SelectUser()
        else:
            if self.SelectName == 0:
                UserVerification(data)
            else:
                SendMessange(data)


class P2PChatFactory(ServerFactory):
    def __init__(self):
        self.users = {}
    def buildProtocol(self, addr):
        return P2PChat(self.users)


if __name__=="__main__":
    endpoints.serverFromString(reactor, "tcp:8051").listen(P2PChatFactory())
    reactor.run()