import tensorflow as tf
import numpy as np

# a homemade lstm network
class customized_lstm:

    # input data has the shape of [batch_size, truncated_backprop_length, N]
    def __init__(self, state_size, batch_size, truncated_backprop_length, input_dimension):
        self._state_size = state_size
        self._batch_size = batch_size
        self._truncated_backprop_length = truncated_backprop_length
        self._input_dimension = input_dimension

        # build the lstm network
        self._init_cell_state = tf.constant(0, dtype=tf.float32, shape=[state_size, self._batch_size])
        self._init_hidden_state = tf.constant(0, dtype=tf.float32, shape=[state_size, self._batch_size])

        self._Wf, self._Bf = self._get_w_b()
        self._Wi, self._Bi = self._get_w_b()
        self._Wo, self._Bo = self._get_w_b()
        self._Ws, self._Bs = self._get_w_b()

    def _get_w_b(self):
        return tf.Variable(np.random.rand(self._state_size, self._state_size + self._input_dimension),
                           dtype=tf.float32), \
               tf.Variable(np.zeros((self._state_size, 1)), dtype=tf.float32)

    def run(self, input_series):
        current_cell_state = self._init_cell_state
        current_hidden_state = self._init_hidden_state
        cell_states = []
        hidden_states = []
        input_series = tf.unstack(input_series, axis=1)
        for current_input in input_series:
            current_input = tf.transpose(current_input)
            # Increasing number of row
            input_and_state_concatenated = tf.concat([current_input, current_hidden_state], axis=0)

            forget_gate = tf.sigmoid(tf.matmul(self._Wf, input_and_state_concatenated) + self._Bf)
            input_gate = tf.sigmoid(tf.matmul(self._Wi, input_and_state_concatenated) + self._Bi)
            output_gate = tf.sigmoid(tf.matmul(self._Wo, input_and_state_concatenated) + self._Bo)

            next_cell_state = forget_gate * current_cell_state + input_gate * \
                              tf.tanh(tf.matmul(self._Ws, input_and_state_concatenated) + self._Bs)
            next_hidden_state = output_gate * tf.tanh(next_cell_state)

            cell_states.append(next_cell_state)
            hidden_states.append(next_hidden_state)

            current_cell_state = next_cell_state
            current_hidden_state = next_hidden_state

        return cell_states, hidden_states
