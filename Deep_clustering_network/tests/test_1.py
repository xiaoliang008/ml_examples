#!/usr/bin/python

from DCN import *
import numpy as np
from numpy import genfromtxt



#	load data
data = genfromtxt('datasets/data_4.csv', delimiter=',')

dcn = DCN(data,4)
print dcn.run()
