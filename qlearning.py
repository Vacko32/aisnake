import sys 
import numpy as np
from collections import defaultdict
from PIL import Image
import cv2
import matplotlib.pyplot as plt
from matplotlib import style
import pickle
from time import sleep, time
import main
import time 





rewardFood = 500
rewardDeath = -50000
epsilon_decay = 0.9998
epsilion = 0.9
gamma = 0.9
size = 10
episodes = 25000
show_every = 1000
startqtable = None # or filename

learning_rate = 0.1
discount = 0.95

player_head_n = 1
player_body_n = 2
food_n = 3

d = {1: (0, 255, 0), 2: (255, 0 ,0), 3: (0, 0, 255)} # bgr colors

if startqtable == None:
    qtable = defaultdict(lambda: [np.random.uniform(-5, 0) for i in range(4)])


