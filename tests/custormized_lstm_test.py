from __future__ import print_function, division

import sys

import numpy as np
import tensorflow as tf
from os import path
current_path = path.dirname(path.abspath(__file__))
parent_path = path.dirname(current_path)
sys.path.append(parent_path)
from models.basic_structure import custormized_lstm

num_epochs = 100
total_series_length = 50000
truncated_backprop_length = 15
state_size = 4
num_classes = 2
echo_step = 3
batch_size = 5
num_batches = total_series_length // batch_size // truncated_backprop_length

# generate data
x = np.random.rand(batch_size * truncated_backprop_length)
x = np.array(x.tolist(), dtype='f')
x = x.reshape((batch_size, -1))

# construct data map
lstm = custormized_lstm.customized_lstm(state_size, batch_size, truncated_backprop_length, 1)
cell_states, hidden_states = lstm.run(x)

# start session
with tf.Session() as sess:
    sess.run(tf.initialize_all_variables())
    print(sess.run(cell_states[0]))
