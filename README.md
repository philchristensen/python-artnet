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

Configure
---------

Creating an INI-format config file in ~/.artnet.conf will allow you to set defaults for any
of the necessary command line options, as well as define rigs used by the logical fixture-
based scripts that come with the distribution.

**Example:**

    [base]
    address = 192.168.0.88


Next create a YAML-format config file in ~/.artnet-rig.yaml to describe your default rig. This
will allow you to run the fixture-based example scripts by describing your logical fixture layout.
A simple example rig might be:

    # Example ~/.artnet-rig.yaml file
    {
        "name": "Example Rig",
        
        "fixtures": {
            "slimpar_1": {
                "address": 1,
                "config": "chauvet/slimpar-64.yaml"
            },
            "slimpar_2": {
                "address": 8,
                "config": "chauvet/slimpar-64.yaml"
            },
            "slimpar_3": {
                "address": 15,
                "config": "chauvet/slimpar-64.yaml"
            },
            "slimpar_4": {
                "address": 22,
                "config": "chauvet/slimpar-64.yaml"
            },
        },
        
        "groups": {
            "all": ["slimpar_1", "slimpar_2", "slimpar_3", "slimpar_4"],
            "odds": ["slimpar_1", "slimpar_3"],
            "evens": ["slimpar_2", "slimpar_4"],
        },
    }


This should be relatively self-explanatory, but to be clear, the 'fixtures' hash defines the available
lighting instruments, while the 'groups' hash gives names to various ordered combinations of fixtures.
Note that several of the example scripts expect the existence of an 'all' group.

Included in the distribution is a more complex example patch that shows off some of the 'layering'
capabilities of python-artnet. It creates three generators:

 1. The first generator is an all-blue patch
 2. Next is a left-to-right white chase that is layered over the blue
 3. Finally is a "bouncing" red chase that is on top of everything

Try it out with:

    artnet script layered_chase



