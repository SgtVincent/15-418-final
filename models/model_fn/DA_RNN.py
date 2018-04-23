import tensorflow as tf
import numpy as np
from os import path
import sys

current_path = path.dirname(path.abspath(__file__))
parent_path = path.dirname(current_path)
sys.path.append(parent_path)
from models.basic_structure import dynamic_lstm


# shape of feature X: [batch_size, truncated_backprop_length, exogenous_number]
# shape of feature Y: [batch_size, truncated_backprop_length, target_dimension]
# shape of label : [batch_size, 1]
def da_rnn_fn(features, labels, mode, params):
    X = features['X']
    Y = features['Y']
    Xt = tf.unstack(X, axis=1)
    Xn = tf.unstack(X, axis=2)

    # build compute network
    batch_size = params['batch_size']
    state_size = params['state_size']
    truncated_backprop_length = params['truncated_backprop_length']
    exogenous_number = params['exogenous_number']
    target_dimension = params['target_dimension']
    num_classes = params['num_classes']
    keep_rate = params['keep_rate']

    # first lstm for attention of exogenous
    lstm0 = dynamic_lstm.dynamic_lstm(state_size=state_size, batch_size=batch_size, keep_rate=keep_rate)
    hidden_states, last_state = lstm0.run(X)
    last_hidden_state = hidden_states[-1]
    attention_hidden_states = hidden_states[0:-1]

    # first attention network
    W0 = tf.Variable(np.random.rand(state_size, truncated_backprop_length), dtype=tf.float32)
    U0 = tf.Variable(np.random.rand(truncated_backprop_length, truncated_backprop_length), dtype=tf.float32)
    V0 = tf.Variable(np.random.rand(truncated_backprop_length, 1), dtype=tf.float32)

    # build exogenous attention
    for h in attention_hidden_states:
        for x in Xn:
            # e's shape [b, 1]
            e = tf.matmul(tf.nn.tanh(tf.matmul(h, W0) + tf.matmul(x, U0)), V0)








    return 0
