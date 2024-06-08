import sys 
import numpy as np
from collections import defaultdict
import pickle
from time import sleep, time
import main

if sys.argv[1] == "p":
    mode = 0
if sys.argv[1] == "t":
    mode = 1

rewardFood = 500
rewardDeath = -50000
alpha = 0.1
alpha_decay = 0.999
gamma = 0.9

if mode == 0:
    pass
if mode == 1:
    pass
