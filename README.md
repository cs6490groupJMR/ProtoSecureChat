ProtoSecureChat
===============

Uses python2 and the twisted library. See http://twistedmatrix.com/trac/wiki/Downloads for instructions on how to get twisted.
The license and original file here are from the twisted repo.

Also install pyOpenSSL.

Current Status
===============
To send a facebook message:

replace the friendid in the string '-friendid@chat.facebook.com' with the friend id of who will receive message

python xmpp_client.py fbusername@chat.facebook.com fbpassword
