import numpy as np
import tensorflow as tf
from File_Conversion import RCFF
from File_Conversion import TimeSlice
import pickle
import sys

class NeuralNetwork():
        def __init__(self):
                vector_size = 139
                num_hidden = 64

                series = tf.placeholder(tf.float32, [None, None, vector_size])

                cell = tf.nn.rnn_cell.LSTMCell(num_hidden, state_is_tuple=True)

                val, state = tf.nn.dynamic_rnn(cell, series, dtype=tf.float32) # val is num_sequences x series_length * num_hidden
                predict_hidden = val[:,:-1,:]
                target = series[0,1:,:] #only use first series
                weight = tf.Variable(tf.truncated_normal([num_hidden, vector_size]))
                bias = tf.Variable(tf.constant(0.1, shape=[vector_size]))
                predict = tf.matmul(predict_hidden[0,:,:], weight) + bias #only use first series
                self.predict_round = tf.where(tf.greater(predict, tf.ones_like(predict)*0.5), tf.ones_like(predict, dtype=tf.int32), tf.zeros_like(predict, dtype=tf.int32))

                loss = tf.reduce_mean(tf.square(target - predict))
                optimizer = tf.train.AdamOptimizer()
                self.minimize = optimizer.minimize(loss)

                init_op = tf.initialize_all_variables()

                self.saver = tf.train.Saver()

                sess = tf.Session()
                sess.run(init_op)

                print('finished init')


        def train(self, rcff, num_iters):
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
                                self.sess.run(self.minimize,{self.series: [this_train_series]})
                        if i % 10 == 0:
                                #TODO: delete last temp snapshot
                                #saver.save(sess, "C:\\temp_snapshot_" + str(snapshot_num))
                                #snapshot_num += 1
                                pass
                        print('done iter' + str(i))
                        sys.stdout.flush()

        def save(self, save_path):
                self.saver.save(self.sess, save_path)

        def load(self, load_path):
                self.saver.restore(self.sess, load_path)

        def sample(self, rcff_dest_path, num_iters, seed=None):
                if not seed:
                        seed = [[0]*self.vector_size]
                        seed[0][74] = 1
                for i in range(num_iters):
                        result = self.predict.eval(session=self.sess, feed_dict={self.series: [seed + [[0]*self.vector_size]]})
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

        # if __name__ == '__main__':
        #         with open('2 Funky 2 - Brothers & Sisters_0.rcff', 'rb') as rcff_file:
        #                 rcff = pickle.load(rcff_file)
        #                 print('unpickled')
        #                 sys.stdout.flush()
        #                 train(rcff, 1)
        #                 print('trained')
        #                 sys.stdout.flush()
        #                 samp = sample('destfile.rcff', 1000)
        #                 print('sampled')
        #                 print(samp)
        #                 sys.stdout.flush()
