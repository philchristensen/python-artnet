python-artnet
=============
               _   _                         _            _
     _ __ _  _| |_| |_  ___ _ _ ___ __ _ _ _| |_ _ _  ___| |_ 
    | '_ \ || |  _| ' \/ _ \ ' \___/ _` | '_|  _| ' \/ -_)  _|
    | .__/\_, |\__|_||_\___/_||_|  \__,_|_|  \__|_||_\___|\__|
    |_|   |__/

an ArtNET/OpenDMX toolkit for lighting design

So far this project is just a proof of concept, on its way to being a full
ArtNet implementation for Python. However, a first goal is actually to test
out some ideas for an alternative approach to lighting control interfaces,
and for that purpose only needs to send DMX control packets.

Install
-------

From the checkout directory:

    python setup.py install

This will install an 'artnet' script in your python bin path. An easy way to
test simple light rigs is to send 100% on all channels; you can do this with:

    artnet script all_channels_full

By default this will send a broadcast packet through your primary interface. If
broadcast doesn't work for you, you may want to specify your Artnet interface
directly with:

    artnet script all_channels_full --address=192.168.0.88

Sending full power to all channels will do different things on different rigs.
On my testing rig there's just 4 SlimPAR fixtures, so full power just sets them
to sound-sensitive mode (the program channel overriding most of the others). YMMV.

To blackout your lights again, run:

    artnet blackout

Or again with a specific address:

    artnet blackout --address=192.168.0.88


