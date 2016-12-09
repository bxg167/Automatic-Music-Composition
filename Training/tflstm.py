import numpy as np
import tensorflow as tf
from File_Conversion import RCFF
from File_Conversion import TimeSlice
import pickle
import sys

vector_size = 139
num_hidden = 64

series = tf.placeholder(tf.float32, [None, None, vector_size])

cell = tf.nn.rnn_cell.LSTMCell(num_hidden,state_is_tuple=True)

val, state = tf.nn.dynamic_rnn(cell, series, dtype=tf.float32) # val is num_sequences x series_length * num_hidden
predict_hidden = val[:,:-1,:]
target = series[0,1:,:] #only use first series
weight = tf.Variable(tf.truncated_normal([num_hidden, vector_size]))
bias = tf.Variable(tf.constant(0.1, shape=[vector_size]))
predict = tf.matmul(predict_hidden[0,:,:], weight) + bias #only use first series
predict_round = tf.where(tf.greater(predict, tf.ones_like(predict)*0.5), tf.ones_like(predict, dtype=tf.int32), tf.zeros_like(predict, dtype=tf.int32))

loss = tf.reduce_mean(tf.square(target - predict))
optimizer = tf.train.AdamOptimizer()
minimize = optimizer.minimize(loss)

init_op = tf.initialize_all_variables()

saver = tf.train.Saver()

sess = tf.Session()
sess.run(init_op)

print('finished init')


def train(rcff, num_iters):
        train_series = []
        for timeslice in rcff.body:
                pitch = int(timeslice.pitch)
                vec = [0] * 128
                vec[pitch] = 1
                vec += [timeslice.volume]
                message_vec= [0]*10
                message_vec[timeslice.message] = 1
                vec += message_vec
                train_series.append(vec)
                
        train_series = [train_series]
        snapshot_num = 0
        for i in range(num_iters):
                for j in range(len(train_series)):
                        this_train_series = train_series[j]
                        sess.run(minimize,{series: [this_train_series]})
                if i % 10 == 0:
                        #TODO: delete last temp snapshot
                        #saver.save(sess, "C:\\temp_snapshot_" + str(snapshot_num))
                        #snapshot_num += 1
                        pass
                print('done iter' + str(i))
                sys.stdout.flush()

def save(save_path):
        saver.save(sess, save_path)

def load(load_path):
        saver.restore(sess, load_path)

def sample(rcff_dest_path, num_iters, seed=None):
        if not seed:
                seed = [[0]*vector_size]
                seed[0][74] = 1
        for i in range(num_iters):
                result = predict.eval(session=sess, feed_dict={series: [seed + [[0]*vector_size]]})
                result_last = result[-1,:]
                seed.append(list(result_last))
        retval = RCFF.RCFF('generated', 120, 0)
        for notes in seed:
                message_vec = notes[129:139]
                ts = TimeSlice.TimeSlice(notes.index(max(notes[0:128])), notes[128], message_vec.index(max(message_vec)))
                retval.body.append(ts)
        with open(rcff_dest_path, 'wb') as rcff_dest_file:
                retval.pickle(rcff_dest_file)
        return retval

if __name__ == '__main__':
        with open('2 Funky 2 - Brothers & Sisters_0.rcff', 'rb') as rcff_file:
                rcff = pickle.load(rcff_file)
                print('unpickled')
                sys.stdout.flush()
                train(rcff, 1)
                print('trained')
                sys.stdout.flush()
                samp = sample('destfile.rcff', 1000)
                print('sampled')
                print(samp)
                sys.stdout.flush()
