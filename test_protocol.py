import protocol

#init the DH
protoA = protocol.Protocol(0)
protoB = protocol.Protocol(1)

firstA = protoA.getPublicKeyMessage("Svc1")
print "Alice First Message: "+firstA

pkeyA = firstA.split(':')[0]

firstB = protoB.getPublicKeyMessage("Svc2")
print "Bob First Message: "+firstB

pkeyB = firstB.split(':')[0]

protoA.computeDHkey(pkeyB)
protoB.computeDHkey(pkeyA)

nonceA = protoA.getEncryptedNonce()
print "Alice Nonce: "+nonceA

nonceB = protoB.getEncryptedNonce()
print "Bob Nonce: "+nonceB

protoA.computeSessionKey(nonceB)
protoB.computeSessionKey(nonceA)

testmessageA = "This is a message!"
print "Alice Message: "+testmessageA

testmessageAenc = protoA.encryptMessage(testmessageA)
print "Alice Message Encoded: "+testmessageAenc

messageB = protoB.decryptMessage(testmessageAenc)
print "Bob Message: "+messageB
