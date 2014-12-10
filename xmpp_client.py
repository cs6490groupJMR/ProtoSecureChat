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
    recordedMsgs = []
    # s_id is service id number, 0 or 1 
    # s1 is other service. so Ugly! - only used in client0
    def __init__(self, reactor, jid, secret, chatbuddy_jid, s_id):
        global cColor
        self.jid=jid
        self.chatbuddy_jid = chatbuddy_jid
        self.s_id = s_id
        self.textColor = cColor
        cColor +=1
        self.reactor = reactor
        self.proto = protocol.Protocol(self.s_id)
        self.hasAuthenticated = False
        f = client.XMPPClientFactory(jid, secret)
        f.addBootstrap(xmlstream.STREAM_CONNECTED_EVENT, self.connected)
        f.addBootstrap(xmlstream.STREAM_END_EVENT, self.disconnected)
        f.addBootstrap(xmlstream.STREAM_AUTHD_EVENT, self.authenticated)
        f.addBootstrap(xmlstream.INIT_FAILED_EVENT, self.init_failed)
        connector = SRVConnector(reactor, 'xmpp-client', jid.host, f, defaultPort=5222)

        connector.connect()
        self.finished = Deferred()


    def setOtherClass(self, s1):
        self.s1 = s1
    
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
        print 'A message is recieved :'

        for element in message.elements():
          if element.name == 'body':
            body = unicode(element).strip()
            print body
            usertxt, chatbuddytxt = self.proto.processIncomingMSG_and_Answer(body)
            
            
            if (usertxt!=""):
                print usertxt


            for i in range(len(chatbuddytxt)):
                if (chatbuddytxt[i]=="NextSvc"):#so protocol wants to jump to other client
                    assert(self.s1)
                    #this will cause the other one to initiate messages!
                        
                    new_usertxt, new_chatbuddytxt = self.s1.proto.processIncomingMSG_and_Answer(chatbuddytxt[i+1])
                    self.sendMessage(self.s1.chatbuddy_jid, new_chatbuddytxt)
                    
                elif (chatbuddytxt[i]!=""):
                    print 'response to that message : {0}'.format(chatbuddytxt[i])
                    self.sendMessage(self.chatbuddy_jid, chatbuddytxt[i])
                

            #self.send_message(message['from'], 'tetet')
            break

    def disconnected(self, xs):
        screen.set_color(self.textColor, 0)
        print 'Disconnected.'

        self.finished.callback(None)

    # data can be list or string!
    def sendMessage(self, to, data):
        for dt in data if not isinstance(data, basestring) else [data]:
            if (dta==""):
                return

            if (not self.hasAuthenticated):
                self.recordedMsgs.append({'to':to,'data':dt})
                return

            screen.set_color(self.textColor, 0)
            message = domish.Element((None, 'message'))
            message['to'] = to.full()
            #google doesnt like from tag, it should acompany id too! just ignoring it seems to work!
            #message['from'] = self.jid.full()
            message['type'] = 'chat'
            message.addElement('body', content= dt)
            self.xmlstream.send(message)


    def authenticated(self, xs):
        self.hasAuthenticated = True
        screen.set_color(self.textColor, 0)
        print "Authenticated."

        presence = domish.Element((None, 'presence'))
        xs.send(presence)

        # here is like a hack to me. This thing should happen when interactively user enters first message and ask for sending message initiation!
        if (self.chatbuddy_jid.user != None):
            #if it was alreadu authenticated from incoming message it should return "" and we are good!
            usertxt, chatbuddytxt = self.proto.processIncomingMSG_and_Answer("")
            self.sendMessage(self.chatbuddy_jid, chatbuddytxt)
    
        if (self.recordedMsgs != []):
            for msg in self.recordedMsgs:
                self.sendMessage(msg['to'],msg['data'])
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

    services = [Client(reactor, JID(jid1), secret1, JID(chatbuddy1),0), Client(reactor, JID(jid2), secret2, JID(chatbuddy2),1)]
    services[0].setOtherClass(services[1])
    services_finish = [services[0].finished, services[1].finished]
    #services = [Client(reactor, JID(jid1), secret1).finished]

    d = defer.gatherResults(services_finish)
    #d.addCallback(lambda ignored: reactor.stop())

    return d
    #return services[0].finished


if __name__ == '__main__':
    print "\n"
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)
    print "\n"

    if (len(sys.argv) == 2):
        if(sys.argv[1] == "alice"):
            choice1, username1, pass1, choice2, username2, pass2, chatbuddy1, chatbuddy2 = ["2","alice_s0","123456789","2","alice_s1","123456789","bob_s0","bob_s1"]
        elif(sys.argv[1] == "bob"):
            choice1, username1, pass1, choice2, username2, pass2, chatbuddy1, chatbuddy2 = ["2","bob_s0","123456789","2","bob_s1","123456789","",""]
        else:
            print "Must choose alice or bob (python xmpp_client.py alice)"
            sys.exit()

        if (chatbuddy1!=""):
            print "I will connect to {0} and {1}".format(chatbuddy1,chatbuddy2)
        else :
            print "I will wait for incoming connection"

        react(main,[username1+servers[int(choice1)]['url'],pass1,chatbuddy1+servers[int(choice1)]['url'],username2+servers[int(choice2)]['url'],pass2,chatbuddy2+servers[int(choice2)]['url']])
        
    screen.set_color(15, 0)
