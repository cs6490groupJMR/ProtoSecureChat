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
                    #result.append("NextSvc") #when sent to bob1, bob1 will create g^b mod p
                    return ("",result)
                else:#this is bob
                    otherPKey = message
                    result.append("NextSvc") #when sent to bob1, bob1 will create g^b mod p
                    result.append(otherPKey)
                    return ("",result)

            else:# this is service 1
                if (message==""): #this is alice

                    return ("",[""])
                else:#this is bob
                    #this is like a fake recieved msg to get complete DH
                    self.getPublicKeyMessage("")
                    self.computeDHkey(message)
                    #increase one more msg to ease my life!!
                    self.msgLevel+=1
                    return ("I have a shared key now!! :"+self.sharedKey,[self.myPKey])


        if (self.msgLevel == 1):
            self.msgLevel+=1
            if (self.s_id==0):# this is service 0
                self.msgLevel-=1
                #so meaning ignore all messages in this service!
                return ("",[""])
            else:#this is service 1
                if (message!=""):#this is alice
                    self.computeDHkey(message)
                    self.msgLevel+=1
                    N_a = self.getEncryptedNonce()
                    return ("I have a shared key now!! :"+self.sharedKey,[N_a])
                else:#this is bob - but shouldnt happened
                    
                    return ("Errr - shouldnt be called :",[""])


        if (self.msgLevel == 2):
            self.msgLevel+=1
            if (self.s_id==0):# this is service 0
                self.msgLevel-=1
                #so meaning ignore all messages in this service!
                return ("",[""])
            else:#this is service 1
                if (message!=""):#this is bob
                    N_b = self.getEncryptedNonce()
                    self.computeSessionKey(message)
                    self.msgLevel+=1 #this is 4 now for bob
                    return ("I have a session key now!! :",[N_b])
                else:#this is ???!!!

                    return ("Errrr ",[""])

        if (self.msgLevel == 3):
            self.msgLevel+=1
            if (self.s_id==0):# this is service 0
                self.msgLevel-=1
                #so meaning ignore all messages in this service!
                return ("",[""])
            else:#this is service 1
                if (message!=""):#this is Alice
                    self.computeSessionKey(message)

                    return ("I have a session key now!!\n sending my first msg! :",[self.encryptMessage("test message 1")])
                else:#this is ???!!!

                    return ("Errrr",[""])

        if (self.msgLevel == 4):
            txt = self.decryptMessage(message)
            return (txt,[self.encryptMessage("test message - rest!!")])


        return ("",[""])

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
        combinedNonces = common.xorNonces(self.myNonce, nonceReceivedDec)
        self.sessionkey = common.generateKey(combinedNonces)

    # encrypts a message with the session key.
    def encryptMessage(self, message):
        return common.encrypt(self.sessionkey, message)

    # decrypts a message with the session key.
    def decryptMessage(self, message):
        return common.decrypt(self.sessionkey, message)
