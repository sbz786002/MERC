import random
import json
import re
import secrets
import pandas
#import os,inspect
from os.path import abspath
import base64
from decimal import Decimal
import pdb
def dcrypt(txt):
	sts = txt
	lrn = int(sts[0])
	rrn = int(sts[-1])
	Rn = lrn + rrn
	strg = sts.split("*")
	Ubnd = int(len(strg)-1)
	DeCrypt = ""
	for x in range(len(strg)):
		if x==0:
			continue
		if x==Ubnd:
			DeCrypt = DeCrypt + chr(int(int(strg[x][:len(strg[x])-1]) / Rn))
		else:
			DeCrypt = DeCrypt + chr(int(int(strg[x]) / Rn))
	return DeCrypt

def encrpyt(txt):
	strg = txt
	n=random.randint(1,9)
	l = len(txt)
	valtext = ""
	for x in range(l):
		asc = ord(strg[x])*n
		valtext = valtext + "*"
		valtext = valtext + str(asc)
	rn1 = round(n/2)
	rn2 = n - rn1
	valtext = str(rn1)+str(valtext)+str(rn2)
	return valtext


