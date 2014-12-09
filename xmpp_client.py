#!/usr/bin/python
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
import sys
import os
"""
A very simple twisted xmpp-client (Jabber ID)

To run the script:
$ python xmpp_client.py <jid> <secret>
"""

import math
from colorconsole import terminal
from subprocess import Popen, CREATE_NEW_CONSOLE

screen = terminal.get_terminal()
screen.set_title("ProtoSecureChat")
screen.clear()

screen.set_color(15, 0)

servers = [ {'name':"Facebook",'url':"@chat.facebook.com"},{'name':"Hangouts",'url':"@gmail.com"},{'name':"Dukgo",'url':"@dukgo.com"}]


from twisted.internet import defer
from twisted.internet.defer import Deferred
from twisted.internet.task import react
from twisted.names.srvconnect import SRVConnector
from twisted.words.xish import domish
from twisted.words.protocols.jabber import xmlstream, client
from twisted.words.protocols.jabber.jid import JID
import protocol

cColor = 2

class Client(object):
    # s_id is service id number, 0 or 1 
    def __init__(self, reactor, jid, secret, chatbuddy_jid, s_id):
        global cColor
        self.jid=jid
        self.chatbuddy_jid = chatbuddy_jid
        self.s_id = s_id
        self.textColor = cColor
        cColor +=1
        self.reactor = reactor
        self.proto = protocol.Protocol(self.s_id)
        f = client.XMPPClientFactory(jid, secret)
        f.addBootstrap(xmlstream.STREAM_CONNECTED_EVENT, self.connected)
        f.addBootstrap(xmlstream.STREAM_END_EVENT, self.disconnected)
        f.addBootstrap(xmlstream.STREAM_AUTHD_EVENT, self.authenticated)
        f.addBootstrap(xmlstream.INIT_FAILED_EVENT, self.init_failed)
        connector = SRVConnector(reactor, 'xmpp-client', jid.host, f, defaultPort=5222)

        connector.connect()
        self.finished = Deferred()


    def rawDataIn(self, buf):
        screen.set_color(self.textColor, 0)
        #print "RECV: %s" % unicode(buf, 'utf-8').encode('ascii', 'replace')


    def rawDataOut(self, buf):
        screen.set_color(self.textColor, 0)
        #print "SEND: %s" % unicode(buf, 'utf-8').encode('ascii', 'replace')


    def connected(self, xs):
        screen.set_color(self.textColor, 0)
        print 'Connected.'

        self.xmlstream = xs

        # Log all traffic
        xs.rawDataInFn = self.rawDataIn
        xs.rawDataOutFn = self.rawDataOut

        self.xmlstream.addObserver('/message', self.handle_message)

    def handle_message(self, message):
        screen.set_color(self.textColor, 0)
        print 'a message is recieved :'
        print message

        for element in message.elements():
          if element.name == 'body':
            body = unicode(element).strip()
            answer = self.proto.processIncomingMSG_and_Answer(body)
            
            
            if (answer[0]!=""):
                print answer[0]

            for txt in answer[1:]:
                if (txt!=""):
                    self.sendMessage(self.chatbuddy_jid, txt)

            #self.send_message(message['from'], 'tetet')
            break

    def disconnected(self, xs):
        screen.set_color(self.textColor, 0)
        print 'Disconnected.'

        self.finished.callback(None)

    
    def sendMessage(self, to, data):
        if (data==""):
            return
        screen.set_color(self.textColor, 0)
        message = domish.Element((None, 'message'))
        message['to'] = to.full()
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

        # here is like a hack to me. This thing should happen when interactively user enters first message and ask for sending message initiation!
        if (self.chatbuddy_jid.user != None):
            #if it was alreadu authenticated from incoming message it should return "" and we are good!
            usertxt, chatbuddytxt = self.proto.processIncomingMSG_and_Answer("")
            self.sendMessage(self.chatbuddy_jid, chatbuddytxt)

        #this makes program terminate! 60 should be enoguh for debugging purposes!
        self.reactor.callLater(60, xs.sendFooter)


    def init_failed(self, failure):
        screen.set_color(self.textColor, 0)
        print "Initialization failed."
        print failure

        self.xmlstream.sendFooter()



def main(reactor, jid1, secret1, chatbuddy1, jid2, secret2, chatbuddy2):
    """
    Connect to the given Jabber ID and return a L{Deferred} which will be
    called back when the connection is over.

    @param reactor: The reactor to use for the connection.
    @param jid: A L{JID} to connect to.
    @param secret: A C{str}
    """

    services = [Client(reactor, JID(jid1), secret1, JID(chatbuddy1),0).finished, Client(reactor, JID(jid2), secret2, JID(chatbuddy2),1).finished]
    #services = [Client(reactor, JID(jid1), secret1).finished]
    
    d = defer.gatherResults(services)
    #d.addCallback(lambda ignored: reactor.stop())

    return d
    #return services[0].finished


if __name__ == '__main__':
    print "\n"
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)
    print "\n"

    i =0
    
    print "\n"

    if (len(sys.argv) == 9):
        tmp, choice1, username1, pass1, choice2, username2, pass2, chatbuddy1, chatbuddy2 =  sys.argv
    elif (len(sys.argv) == 7):
        tmp, choice1, username1, pass1, choice2, username2, pass2 =  sys.argv
        chatbuddy1 = ""
        chatbuddy2 = ""
    else:
        print "Available services are : \n"
        for server in servers:
            print '{0} :{1}'.format(i,server['name'])
            i+=1

        choice1 = raw_input("Please enter your 1st service: ")
        username1 = raw_input("Please enter your user name: ")
        pass1 = raw_input("Please enter your password: ")
        chatbuddy1 = raw_input("Please enter your chat buddy: ")

        print "\n\n"
        choice2 = raw_input("Please enter your 2st service: ")
        username2 = raw_input("Please enter your user name: ")
        pass2 = raw_input("Please enter your password: ")
        chatbuddy2 = raw_input("Please enter your chat buddy: ")

    

    # now lunch other application!
    if (chatbuddy1!=""):
        print "I will connect to {0} and {1}".format(chatbuddy1,chatbuddy2)
        p = Popen('python xmpp_client.py 2 bob_s0 123456789 2 bob_s1 123456789', creationflags=CREATE_NEW_CONSOLE)
    else :
        print "I will wait for incoming connection"


    react(main,[username1+servers[int(choice1)]['url'],pass1,chatbuddy1+servers[int(choice1)]['url'],username2+servers[int(choice2)]['url'],pass2,chatbuddy2+servers[int(choice2)]['url']])
    #react(main,[username1+servers[int(choice1)]['url'],pass1,username1+servers[int(choice1)]['url'],pass1])
        
    if (p):
        p.terminate()
        
    screen.set_color(15, 0)
