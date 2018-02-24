# coding=utf-8
from ctypes import *
aa="514978574811676514149555364380762716"

i=0
str=""
while i <len(aa):
    str=str+(chr(int(aa[i:i+2],16)))
    i+=2
print(str)