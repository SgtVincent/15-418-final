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
            current_input = tf.reshape(current_input, [self._input_dimension, self._batch_size])
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


# lstm model fn
def lstm_model_fn(features, labels, mode, params):
    """LSTM model with a single lstm layer"""
    # Create three fully connected layers each layer having a dropout
    # probability of 0.1.
    net = tf.feature_column.input_layer(features, params['feature_columns'])
    for units in params['hidden_units']:
        net = tf.layers.dense(net, units=units, activation=tf.nn.relu)

    # create input tensor
    # input_series's shape [batch_size, time_step, input_dimension]
    # label_series's shape [batch_size, 1]
    input_series = features['feature']
    label_series = labels

    # build compute network
    batch_size = params['batch_size']
    state_size = params['state_size']
    truncated_backprop_length = params['truncated_backprop_length']
    input_dimension = params['input_dimension']
    num_classes = params['num_classes']

    lstm = customized_lstm(state_size=state_size, batch_size=batch_size, \
                           truncated_backprop_length=truncated_backprop_length, input_dimension=input_dimension)

    cell_states, hidden_states = lstm.run(input_series)

    # final_hidden_states's shape [state_size, batch_size]
    fianl_hidden_states = hidden_states[-1]

    W = tf.Variable(np.random.rand(num_classes, num_classes), dtype=tf.float32)
    b2 = tf.Variable(np.zeros((1, num_classes)), dtype=tf.float32)

    # Compute logits (1 per class).
    logits = tf.layers.dense(net, params['n_classes'], activation=None)

    # Compute predictions.
    predicted_classes = tf.argmax(logits, 1)
    if mode == tf.estimator.ModeKeys.PREDICT:
        predictions = {
            'class_ids': predicted_classes[:, tf.newaxis],
            'probabilities': tf.nn.softmax(logits),
            'logits': logits,
        }
        return tf.estimator.EstimatorSpec(mode, predictions=predictions)

    # Compute loss.
    loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

    # Compute evaluation metrics.
    accuracy = tf.metrics.accuracy(labels=labels,
                                   predictions=predicted_classes,
                                   name='acc_op')
    metrics = {'accuracy': accuracy}
    tf.summary.scalar('accuracy', accuracy[1])

    if mode == tf.estimator.ModeKeys.EVAL:
        return tf.estimator.EstimatorSpec(
            mode, loss=loss, eval_metric_ops=metrics)

    # Create training op.
    assert mode == tf.estimator.ModeKeys.TRAIN

    optimizer = tf.train.AdagradOptimizer(learning_rate=0.1)
    train_op = optimizer.minimize(loss, global_step=tf.train.get_global_step())
    return tf.estimator.EstimatorSpec(mode, loss=loss, train_op=train_op)
