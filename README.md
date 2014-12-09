ProtoSecureChat
===============

Uses python2 and the twisted library. See http://twistedmatrix.com/trac/wiki/Downloads for instructions on how to get twisted.
The license and original file here are from the twisted repo.

Also install pyOpenSSL.

Current Status
===============
To send a facebook message:

python xmpp_client.py

You will be prompted for the xmpp user (eg username@chat.facebook.com) and password.
This will be repeated for the second account you will use.
The facebook friend id will be prompted.

This project includes a DH implementation by Elizabeth Myers, see DH.py for more information.
The main files are based on the twisted library xmpp_client.py example.
