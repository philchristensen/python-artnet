python-artnet
=============

an ArtNET/OpenDMX toolkit for lighting design

So far this project is just a proof of concept, on its way to being a full
ArtNet implementation for Python. However, a first goal is actually to test
out some ideas for an alternative approach to lighting control interfaces,
and for that purpose only needs to send DMX control packets.

Install
-------

From the checkout directory:

    python setup.py install

Three scripts are installed to the Python binary directory (if using the system
Python, this is /usr/bin, and should already be in your path):

**artnet_listener**
    
> a simple listener example for ArtNet Poll requests

**artnet_blackout**
    
> sends a blackout DMX packet to a specified address

**artnet_halfup**
    
> sends a DMX packet to a specified address that sets 50% level on all channels