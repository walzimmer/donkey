import numpy as np

channel_one = np.zeros((2, 2, 1))
channel_two = np.ones((2, 2, 1))
stacked = np.dstack((channel_one, channel_two))
