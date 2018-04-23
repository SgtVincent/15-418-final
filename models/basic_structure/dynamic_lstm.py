import tensorflow as tf


# a dynamic lstm built on tensorflow official api
class dynamic_lstm:
    def __init__(self, state_size, batch_size, keep_rate):
        # build the lstm network
        _init_cell_state = tf.constant(0, dtype=tf.float32, shape=[batch_size, state_size])
        _init_hidden_state = tf.constant(0, dtype=tf.float32, shape=[batch_size, state_size])
        self._init_state = tf.nn.rnn_cell.LSTMStateTuple(_init_cell_state, _init_hidden_state)
        self._cell = tf.nn.rnn_cell.LSTMCell(state_size, state_is_tuple=True)
        self._cell = tf.nn.rnn_cell.DropoutWrapper(self._cell, output_keep_prob=keep_rate)

    # run the dynamic lstm
    # input shape [batch_size, max_time, input_dimension]
    # output two variables: hidden_states, last_state
    # hidden_state shape [batch_size, max_time, state_size]
    # last_state shape [batch_size, state_size]
    def run(self, input_series):
        return tf.nn.dynamic_rnn(self._cell, input_series,
                                 initial_state=self._init_state,
                                 dtype=tf.float32)
