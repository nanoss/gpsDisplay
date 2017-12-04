#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import socket
import struct
import random
import time

# typedef struct 
# {
# 	int tgtID;
# 	int tgtLong;
# 	int tgtLat;
# }TGT_SIM_TS_ONE_ST;
# typedef struct
# { 
# 	int tgtNum;
# 	TGT_SIM_TS_ONE_ST stTgt[3];
# }TGT_SIM_TS_ONE_ST;



address = ('127.0.0.1', 31500)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ltgtData = [2, 100, 12400, 3200, 101, 12400, 3200]
ltgtData[2] = random.randrange(12400, 12700, 1)
ltgtData[3] = random.randrange(3200, 3500, 1)
ltgtData[5] = random.randrange(12400, 12700, 1)
ltgtData[6] = random.randrange(3200, 3500, 1)

while True:
	# msg = input("=")
	# if not msg:
	# 	break
	# num = int(msg)
	time.sleep(1)
	ltgtData[0] = 2
	ltgtData[1] = random.randrange(101, 103, 1)
	#ltgtData[4] = random.randrange(101, 103, 1)
	ltgtData[4] = 0
	ix = random.randrange(1, 6, 1);
	ltgtData[2] = ltgtData[2] * (ltgtData[1]-100 +1000 +ix) //1000
	ix = random.randrange(1, 6, 1);
	ltgtData[3] = ltgtData[3] * (ltgtData[1]-100 +1000 +ix) //1000
	ix = random.randrange(1, 6, 1);
	ltgtData[5] = ltgtData[5] * (ltgtData[4]-100 +1000 +ix) //1000
	ix = random.randrange(1, 6, 1);
	ltgtData[6] = ltgtData[6] * (ltgtData[4]-100 +1000 +ix) //1000

	print(ltgtData)
	yztgt = tuple(ltgtData)
	tgtMsg = struct.pack("!7i", *yztgt)
	s.sendto(tgtMsg, address)

s.close()
