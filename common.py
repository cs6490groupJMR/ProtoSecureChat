from Crypto import Random
from Crypto.Cipher import DES3
from itertools import izip
import base64
import DH

# This returns a 192 bit nonce using a good random number generator.
def getNonce():
    # This generator takes in bytes, so 24 bytes = 192 bits
    return base64.b64encode(Random.new().read(24))

# Using the given key, encrypt the given data with DES3 and CBC.
def encrypt(key, data):

    enc = DES3.new(base64.b64decode(key[0]), DES3.MODE_CBC, base64.b64decode(key[1]))

    # Pad the data properly
    data = setPadding(data)

    # encrypt the data
    return base64.b64encode(enc.encrypt(data))

# Using the given key, decrypt the given data with DES3 and CBC if set, otherwise uses ECB.
def decrypt(key, data):

    dec = DES3.new(base64.b64decode(key[0]), DES3.MODE_CBC, base64.b64decode(key[1]))

    # decrypt the data
    decrypted = dec.decrypt(base64.b64decode(data))

    # remove any padding if any
    return decrypted.strip()

# Since our data needs to properly padded to 8 bytes boundries, add characters to the end until it is padded.
def setPadding(data):
    # until we mod by 8 to zero, keep adding spaces
    while(len(data) % 8 != 0):
        data += ' '
    return data

def xorNonces(nonce1, nonce2):
    xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(nonce1,nonce2))
    return base64.encodestring(xored).strip()

# Generate a key pair of an iv and a key, encoded in base 64, from a given key.
def generateKey(key):
    return (base64.b64encode(base64.b64decode(key[:22]+'==')), base64.b64encode(base64.b64decode(key[22:33]+'=')))

# initialize a new DiffieHellman exchange.
def initDH():
    return DH.DiffieHellman()

# Get the public key that is to be sent to the other client.
def getGHPublicKey(dh):
    return base64.b64encode(dh.generateKeys())

# Get the shared key using the public key sent from the other client, as well as our key.
def computeDHkey(dh, pubKey):
    skey = base64.b64decode(pubKey)
    return base64.b64encode(dh.computeKey(skey))
