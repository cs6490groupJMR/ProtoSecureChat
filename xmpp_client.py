#!/usr/bin/python
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
A very simple twisted xmpp-client (Jabber ID)

To run the script:
$ python xmpp_client.py <jid> <secret>
"""
import math
from colorconsole import terminal

screen = terminal.get_terminal()
screen.set_title("ProtoSecureChat")
screen.clear()

screen.set_color(15, 0)

servers = [ {'name':"Facebook",'url':"@chat.facebook.com"},{'name':"Hangouts",'url':"@gmail.com"},{'name':"Dukgo",'url':"@dukgo.com"}]

import sys

from twisted.internet import defer
from twisted.internet.defer import Deferred
from twisted.internet.task import react
from twisted.names.srvconnect import SRVConnector
from twisted.words.xish import domish
from twisted.words.protocols.jabber import xmlstream, client
from twisted.words.protocols.jabber.jid import JID
import protocol

cColor = 1

class Client(object):
    def __init__(self, reactor, jid, secret):
        global cColor
        self.jid=jid
        self.textColor = cColor
        cColor +=1
        self.reactor = reactor
        self.proto = protocol.Protocol()
        f = client.XMPPClientFactory(jid, secret)
        f.addBootstrap(xmlstream.STREAM_CONNECTED_EVENT, self.connected)
        f.addBootstrap(xmlstream.STREAM_END_EVENT, self.disconnected)
        f.addBootstrap(xmlstream.STREAM_AUTHD_EVENT, self.authenticated)
        f.addBootstrap(xmlstream.INIT_FAILED_EVENT, self.init_failed)
        #if (jid.host == "gmail.com"):
        #    connector = SRVConnector(reactor, 'xmpp-client', "talk.google.com", f, defaultPort=5222)
        #else:
        connector = SRVConnector(reactor, 'xmpp-client', jid.host, f, defaultPort=5222)

        connector.connect()
        self.finished = Deferred()


    def rawDataIn(self, buf):
        screen.set_color(self.textColor, 0)
        print "RECV: %s" % unicode(buf, 'utf-8').encode('ascii', 'replace')


    def rawDataOut(self, buf):
        screen.set_color(self.textColor, 0)
        print "SEND: %s" % unicode(buf, 'utf-8').encode('ascii', 'replace')


    def connected(self, xs):
        screen.set_color(self.textColor, 0)
        print 'Connected.'

        self.xmlstream = xs

        # Log all traffic
        xs.rawDataInFn = self.rawDataIn
        xs.rawDataOutFn = self.rawDataOut

        self.xmlstream.addObserver('/message', self.handle_message)

    def handle_message(self, message):
        for element in message.elements():
          if element.name == 'body':
            body = unicode(element).strip()
            print body
            #self.send_message(message['from'], 'tetet')
            break

    def disconnected(self, xs):
        screen.set_color(self.textColor, 0)
        print 'Disconnected.'

        self.finished.callback(None)

    
    def sendMessage(self, to, data):
        screen.set_color(self.textColor, 0)
        message = domish.Element((None, 'message'))
        message['to'] = to
        #google doesnt like from tag, it should acompany id too! just ignoring it seems to work!
        #message['from'] = self.jid.full()
        message['type'] = 'chat'
        message.addElement('body', content= data)
        self.xmlstream.send(message)


    def authenticated(self, xs):
        screen.set_color(self.textColor, 0)
        print "Authenticated."

        presence = domish.Element((None, 'presence'))
        xs.send(presence)

        myPKey = self.proto.getHelloMessage()

        friendid = raw_input("Please enter your friends username/friendid for {0} :".format(self.jid))

        self.sendMessage(friendid+"@"+self.jid.host, myPKey)
        #this makes program terminate!
        self.reactor.callLater(8, xs.sendFooter)


    def init_failed(self, failure):
        screen.set_color(self.textColor, 0)
        print "Initialization failed."
        print failure

        self.xmlstream.sendFooter()



def main(reactor, jid1, secret1, jid2, secret2):
    """
    Connect to the given Jabber ID and return a L{Deferred} which will be
    called back when the connection is over.

    @param reactor: The reactor to use for the connection.
    @param jid: A L{JID} to connect to.
    @param secret: A C{str}
    """

    services = [Client(reactor, JID(jid1), secret1).finished, Client(reactor, JID(jid2), secret2).finished]
    #services = [Client(reactor, JID(jid1), secret1).finished]
    
    d = defer.gatherResults(services)
    #d.addCallback(lambda ignored: reactor.stop())

    return d
    #return services[0].finished


if __name__ == '__main__':
    i =0
    print "Available services are : \n"
    for server in servers:
        print '{0} :{1}'.format(i,server['name'])
        i+=1
    
    print "\n"
    choice1 = raw_input("Please enter your 1st service: ")
    username1 = raw_input("Please enter your user name: ")
    pass1 = raw_input("Please enter your password: ")

    print "\n\n"
    choice2 = raw_input("Please enter your 2st service: ")
    username2 = raw_input("Please enter your user name: ")
    pass2 = raw_input("Please enter your password: ")

    react(main,[username1+servers[int(choice1)]['url'],pass1,username2+servers[int(choice2)]['url'],pass2])
    #react(main,[username1+servers[int(choice1)]['url'],pass1,username1+servers[int(choice1)]['url'],pass1])
        
    screen.set_color(15, 0)
