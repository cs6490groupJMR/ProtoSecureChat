import common

class Protocol(object):
    msgAuth = "Authenticate"

    # s_id is service id number, 0 or 1 
    def __init__(self,s_id):
        self.dh = common.initDH()
        self.msgLevel = 0
        self.s_id = s_id

    # This should be the main communication port of this class. Depending on its level answer and increase the msgLevel
    # return value is (text for user , msg back to chat buddy)
    # so after chat has begun user can see unencrypted messages!
    def processIncomingMSG_and_Answer(self, message):
        if (msgLevel == 0):
            if ((message == msgAuth) or (message == "")):
                self.msgLevel+=1
                return ("", msgAuth)
            else:
                #dont increase msglevel just return
                return ("","")
        #this is template...should be implemented!
        if (msgLevel == 1):
            #so to distinguish is it service0 or service n
            if (s_id==0):
                self.msgLevel+=1
                return ("","")
            else:
                self.msgLevel+=1
                return ("","")



        return ("","")

    # return the standardized protocol hello message.
    def getHelloMessage(self):
        return "Authenticate"

    # return the public DH key, which is g^a mod p.
    def getPublicKeyMessage(self, nextSvc):
        self.myPKey = common.getGHPublicKey(dh)
        if not nextSvc:
            return myPKey
        else:
            return myPKey+":"+nextSvc

    # determine the full DH key, which is g^ab mod p. Must be given the remote DH public key, g^b mod p.
    def computeDHkey(self, pubKey):
        self.sharedKey = common.computeDHkey(self.dh, pubKey)

    # gives a random nonce encrypted with the DH key.
    def getEncryptedNonce(self):
        self.DHKey = common.generateKey(self.sharedKey)
        self.myNonce = common.getNonce()
        return common.encrypt(self.DHKey, nonce)

    # decrypt the nonce received and combine it with our nonce and create a session key.
    def computeSessionKey(self, nonceReceived):
        nonceReceivedDec = common.decrypt(self.DHKey, nonceReceived)
        combinedNonces = self.myNonce+nonceReceivedDec+self.myNonce+nonceReceivedDec
        self.sessionkey = common.generateKey(combinedNonces)

    def encryptMessage(self, message):
        return common.encrypt(self.sessionkey, message)
