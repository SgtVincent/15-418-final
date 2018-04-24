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
    hidden_states = tf.unstack(hidden_states, axis=1)
    last_hidden_state = hidden_states[-1]
    attention_hidden_states = hidden_states[0:-1]

    # first attention network
    W0 = tf.Variable(np.random.rand(state_size, truncated_backprop_length), dtype=tf.float32)
    U0 = tf.Variable(np.random.rand(truncated_backprop_length, truncated_backprop_length), dtype=tf.float32)
    V0 = tf.Variable(np.random.rand(truncated_backprop_length, 1), dtype=tf.float32)

    # build exogenous attention
    weights = []
    for h in attention_hidden_states:
        attention_matrix = 0
        # x's shape [batch_size, max_time]
        for x in Xn:  # exogenous_number
            # e's shape [b, 1]
            e = tf.matmul(tf.nn.tanh(tf.matmul(h, W0) + tf.matmul(x, U0)), V0)
            if attention_matrix == 0:
                attention_matrix = e
            else:
                attention_matrix = tf.concat([attention_matrix, e], axis=1)
        attention_matrix = tf.nn.softmax(attention_matrix)
        weights.append(attention_matrix)

    weighted_Xt = []
    for i in range(0, truncated_backprop_length):
        weighted_Xt.append(weights[i] * Xt[i])

    # reshape the weighted_x
    weighted_Xt = tf.stack(weighted_Xt)
    weighted_Xt = tf.unstack(weighted_Xt, axis=1)
    weighted_Xt = tf.stack(weighted_Xt)

    # get all hidden vector again
    hidden_states, last_state = lstm0.run(weighted_Xt)
    attention_hidden_states = hidden_states[1:]  # shape [batch_size, max_time, state_size]

    # build second attention network
    



    return 0
