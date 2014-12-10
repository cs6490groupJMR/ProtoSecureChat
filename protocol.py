import common

class Protocol(object):
    msgAuth = "Authenticate"

    # s_id is service id number, 0 or 1 
    def __init__(self,s_id):
        self.dh = common.initDH()
        self.msgLevel = 0
        self.s_id = s_id

    # This should be the main communication port of this class. Depending on its level answer and increase the msgLevel
    # return value is (text for user , msg back to chat buddy0, msg to chat buddy1)
    # so after chat has begun user can see unencrypted messages!
    # xmpp_client expects at least two elements inside the result list
    def processIncomingMSG_and_Answer(self, message):
        result = []
        if (self.msgLevel == 0):
            self.msgLevel+=1
            if (self.s_id == 0):# this is service 0
                if (message==""): #this is alice
                    self.getPublicKeyMessage("")
                    result.append(self.myPKey)
                    result.append("NextSvc") #when sent to bob1, bob1 will create g^b mod p
                    return ("",result)
                else:#this is bob
                    otherPKey = message
                    result.append("NextSvc") #when sent to bob1, bob1 will create g^b mod p
                    result.append(otherPKey)
                    return ("",result)

            else:# this is service 1
                if (message==""): #this is alice
                    return ("","")
                else:
                #dont increase msglevel just return
                    self.getPublicKeyMessage("")
                    self.computeDHkey(message.split(":"))

                    return ("I have a shared key now!!","")
        #this is template...should be implemented!
        if (self.msgLevel == 1):
            #so to distinguish is it service0 or service n
            if (s_id==0):
                self.msgLevel+=1

                return ("","")
            else:
                self.msgLevel+=1

                return ("","")



        return ("","")

    # return the public DH key, which is g^a mod p.
    def getPublicKeyMessage(self, nextSvc):
        self.myPKey = common.getGHPublicKey(self.dh)
        if not nextSvc:
            return self.myPKey
        else:
            return self.myPKey+":"+nextSvc

    # determine the full DH key, which is g^ab mod p. Must be given the remote DH public key, g^b mod p.
    def computeDHkey(self, pubKey):
        self.sharedKey = common.computeDHkey(self.dh, pubKey)

    # gives a random nonce encrypted with the DH key.
    def getEncryptedNonce(self):
        self.DHKey = common.generateKey(self.sharedKey)
        self.myNonce = common.getNonce()
        return common.encrypt(self.DHKey, self.myNonce)

    # decrypt the nonce received and combine it with our nonce and create a session key.
    def computeSessionKey(self, nonceReceived):
        nonceReceivedDec = common.decrypt(self.DHKey, nonceReceived)
        combinedNonces = (self.myNonce+nonceReceivedDec+self.myNonce+nonceReceivedDec).replace("=", "")
        self.sessionkey = common.generateKey(combinedNonces)

    # encrypts a message with the session key.
    def encryptMessage(self, message):
        return common.encrypt(self.sessionkey, message)

    # decrypts a message with the session key.
    def decryptMessage(self, message):
        return common.decrypt(self.sessionkey, message)
