import torch 
import random 
import numpy as np
import mainq as gm
from collections import deque

max_memory = 10000
batch_size = 1000
lr = 0.001

class Agent:

    def __init__(self):
        pass

    def get_state(self, mainq):
        pass

    def remember(self, state, action, reward, next_state, done):
        pass