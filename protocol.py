import common

class Protocol(object):
    def __init__(self):
        self.dh = common.initDH()

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
