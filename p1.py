#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
#import numpy as np
import socket
import time
import struct
import math
import sys


MAX_DRAW_TGT_NUM = 10
MAX_DRAW_TGT_POINT_NUM = 10

recvTime = time.time()
dictTgtPara = { recvTime:  [12400,3200], }
dictTgt={100:dictTgtPara, 101:dictTgtPara}

plt.ion()
plt.figure()


address = ('127.0.0.1', 31500)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)


while True:
	curTime = time.time()

	# del timeout tgt
	print(list(dictTgt.keys()))
	for tgtKey in list(dictTgt.keys()):
		print(list(dictTgt[tgtKey].keys()))
		for timekey in list(dictTgt[tgtKey].keys()):
			if curTime - timekey > 30:
				del dictTgt[tgtKey][timekey]
		if len(dictTgt[tgtKey]) == 0:
			del dictTgt[tgtKey]



	#draw all Tgt
	plt.cla()
	plotCommtetList = []
	plotCommtetTuple = ()

	for oneTgt in dictTgt.items():
		lx = []
		ly = []
		for onePoint in oneTgt[1].items():
			lx.append(onePoint[1][0]) #lon
			ly.append(onePoint[1][1]) #lat
			if curTime - onePoint[0] > 30:
				del oneTgt[1][onePoint[0]]
		if len(oneTgt[1]) == 0:
			del dictTgt[oneTgt[0]]			
		#print(lx,ly)
		if oneTgt[0]%7 == 0:
			plotrt = plt.plot(lx, ly, "bo-")
		elif oneTgt[0]%7 == 1:
			plotrt = plt.plot(lx, ly, "go-")
		elif oneTgt[0]%7 == 2:
			plotrt = plt.plot(lx, ly, "ro-")
		elif oneTgt[0]%7 == 3:
			plotrt = plt.plot(lx, ly, "co-")
		elif oneTgt[0]%7 == 4:
			plotrt = plt.plot(lx, ly, "mo-")
		elif oneTgt[0]%7 == 5:
			plotrt = plt.plot(lx, ly, "yo-")
		else:
			plotrt = plt.plot(lx, ly, "ko-")

		plotCommtetList.append(str("t=" + str(oneTgt[0])))
		plt.pause(0.01)

	plotCommtetTuple = tuple(plotCommtetList)
	print(plotCommtetTuple)
	plt.pause(0.01)
	plt.draw()


#socket
	data, addr = s.recvfrom(2048)
	if not data:
		sys.exit()
	#print( "received:", data, "from", addr)
	yz1 = struct.unpack("!7i", data)
	#print(yz1)

	if yz1[0] > 2:
		break
	for i in range(yz1[0]):
		if yz1[1+(i*3) + 0] == 0:
			break;
		newTgtNo = yz1[1+(i*3) + 0]
		newTgtLon = yz1[1+(i*3) + 1]
		newTgtLat = yz1[1+(i*3) + 2]
		#addtgt
		# add 100 time 124.01,3201
		# dictTgt >3 exit
		# dictTgtPara >3 pop
		newTgtRecvTime = time.time()
		if newTgtNo in dictTgt:
			# pring("---tgt in=", newTgtNo)
			dictNewTgtPara = dictTgt.get(newTgtNo)
			if len(dictNewTgtPara) > MAX_DRAW_TGT_POINT_NUM:
				keyList = list(dictNewTgtPara.keys())
				# print(keyList)
				keyList.sort()
				del dictNewTgtPara[keyList[0]]
				dictNewTgtPara[newTgtRecvTime] = [newTgtLon, newTgtLat]
			else:
				dictNewTgtPara[newTgtRecvTime] = [newTgtLon, newTgtLat]
		
		elif len(dictTgt) > MAX_DRAW_TGT_NUM:
			print("TODO:::::: return")
		else:
			dictTgt[newTgtNo] = {newTgtRecvTime : [newTgtLon, newTgtLat]}

s.close()