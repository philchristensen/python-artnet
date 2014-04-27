STANDARD_PORT = 6454

OPCODES = dict(
	# This is an ArtPoll packet, no other data is contained in this UDP packet. 
	OpPoll = 0x0020,
	# This is an ArtPollReply Packet. It contains device status information. 
	OpPollReply = 0x0021,
	# Diagnostics and data logging packet. 
	OpDiagData = 0x0023,
	# Used to send text based parameter commands. 
	OpCommand = 0x0024,
	# This is an ArtDmx data packet. It contains zero start code DMX512 information for a single Universe. 
	OpOutput = 0x0050,
	# This is an ArtDmx data packet. It contains zero start code DMX512 information for a single Universe. 
	OpDmx = 0x0050,
	# This is an ArtNzs data packet. It contains non-zero start code (except RDM) DMX512 information for a single Universe. 
	OpNzs = 0x0051,
	# This is an ArtAddress packet. It contains remote programming information for a Node. 
	OpAddress = 0x0060,
	# This is an ArtInput packet. It contains enable  disable data for DMX inputs. 
	OpInput = 0x0070,
	# This is an ArtTodRequest packet. It is used to request a Table of Devices (ToD) for RDM discovery. 
	OpTodRequest = 0x0080,
	# This is an ArtTodData packet. It is used to send a Table of Devices (ToD) for RDM discovery. 
	OpTodData = 0x0081,
	# This is an ArtTodControl packet. It is used to send RDM discovery control messages. 
	OpTodControl = 0x0082,
	# This is an ArtRdm packet. It is used to send all non discovery RDM messages. 
	OpRdm = 0x0083,
	# This is an ArtRdmSub packet. It is used to send compressed, RDM Sub-Device data. 
	OpRdmSub = 0x0084,
	# This is an ArtVideoSetup packet. It contains video screen setup information for nodes that implement the extended video features. 
	OpVideoSetup = 0x10a0,
	# This is an ArtVideoPalette packet. It contains colour palette setup information for nodes that implement the extended video features. 
	OpVideoPalette = 0x20a0,
	# This is an ArtVideoData packet. It contains display data for nodes that implement the extended video features. 
	OpVideoData = 0x40a0,
	# This is an ArtMacMaster packet. It is used to program the Node's MAC address, Oem device type and ESTA manufacturer code.
	# This is for factory initialisation of a Node. It is not to be used by applications. 
	OpMacMaster = 0x00f0,
	# This is an ArtMacSlave packet. It is returned by the node to acknowledge receipt of an ArtMacMaster packet. 
	OpMacSlave = 0x00f1,
	# This is an ArtFirmwareMaster packet. It is used to upload new firmware or firmware extensions to the Node.
	OpFirmwareMaster = 0x00f2,
	# This is an ArtFirmwareReply packet. It is returned by the node to acknowledge receipt of an ArtFirmwareMaster packet or ArtFileTnMaster packet. 
	OpFirmwareReply = 0x00f3,
	# Uploads user file to node. 
	OpFileTnMaster = 0x00f4,
	# Downloads user file from node. 
	OpFileFnMaster = 0x00f5,
	# Node acknowledge for downloads. 
	OpFileFnReply = 0x00f6,
	# This is an ArtIpProg packet. It is used to reprogramme the IP, Mask and Port address of the Node. 
	OpIpProg = 0x00f8,
	# This is an ArtIpProgReply packet. It is returned by the node to acknowledge receipt of an ArtIpProg packet. 
	OpIpProgReply = 0x00f9,
	# This is an ArtMedia packet. It is Unicast by a Media Server and acted upon by a Controller. 
	OpMedia = 0x0090,
	# This is an ArtMediaPatch packet. It is Unicast by a Controller and acted upon by a Media Server. 
	OpMediaPatch = 0x0091,
	# This is an ArtMediaControl packet. It is Unicast by a Controller and acted upon by a Media Server. 
	OpMediaControl = 0x0092,
	# This is an ArtMediaControlReply packet. It is Unicast by a Media Server and acted upon by a Controller. 
	OpMediaContrlReply = 0x0093,
	# This is an ArtTimeCode packet. It is used to transport time code over the network. 
	OpTimeCode = 0x0097,
	# Used to synchronise real time date and clock 
	OpTimeSync = 0x0098,
	# Used to send trigger macros 
	OpTrigger = 0x0099,
	# Requests a node's file list 
	OpDirectory = 0x009a,
	# Replies to OpDirectory with file list
	OpDirectoryReply = 0x9b00
)

NODE_REPORT_CODES = dict(
	RcDebug = ('0x0000', "Booted in debug mode"),
	RcPowerOk = ('0x0001', "Power On Tests successful"),
	RcPowerFail = ('0x0002', "Hardware tests failed at Power On"),
	RcSocketWr1 = ('0x0003', "Last UDP from Node failed due to truncated length, Most likely caused by a collision."),
	RcParseFail = ('0x0004', "Unable to identify last UDP transmission. Check OpCode and packet length."),
	RcUdpFail = ('0x0005', "Unable to open Udp Socket in last transmission attempt"),
	RcShNameOk = ('0x0006', "Confirms that Short Name programming via ArtAddress, was successful."),
	RcLoNameOk = ('0x0007', "Confirms that Long Name programming via ArtAddress, was successful."),
	RcDmxError = ('0x0008', "DMX512 receive errors detected."),
	RcDmxUdpFull = ('0x0009', "Ran out of internal DMX transmit buffers."),
	RcDmxRxFull = ('0x000a', "Ran out of internal DMX Rx buffers."),
	RcSwitchErr = ('0x000b', "Rx Universe switches conflict."),
	RcConfigErr = ('0x000c', "Product configuration does not match firmware."),
	RcDmxShort = ('0x000d', "DMX output short detected. See GoodOutput field."),
	RcFirmwareFail = ('0x000e', "Last attempt to upload new firmware failed."),
	RcUserFail = ('0x000f', "User changed switch settings when address locked by remote programming. User changes ignored.")
)

STYLE_CODES = dict(
	#  A DMX to / from Art-Net device 
	StNode = 0x00,
	#  A lighting console. 
	StController = 0x01,
	#  A Media Server. 
	StMedia = 0x02,
	#  A network routing device. 
	StRoute = 0x03,
	#  A backup device. 
	StBackup = 0x04,
	#  A configuration or diagnostic tool. 
	StConfig = 0x05,
	#  A visualiser. 	
	StVisual = 0x06
)
 
