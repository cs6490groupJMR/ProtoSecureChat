ProtoSecureChat
===============

Uses python2 and the twisted library. See http://twistedmatrix.com/trac/wiki/Downloads for instructions on how to get twisted.
The license and original file here are from the twisted repo.

Also requires pyOpenSSL and pyCrypto.

Current Status
===============
We have dukgo accounts that are currently hardcoded into the code.

You can test with our alice and bob users as follows:

python xmpp_client.py bob
python xmpp_client.py alice

This project includes a DH implementation by Elizabeth Myers, see DH.py for more information.
The main files are based on the twisted library xmpp_client.py example.
