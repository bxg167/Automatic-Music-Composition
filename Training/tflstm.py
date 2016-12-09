import numpy as np
import tensorflow as tf
from File_Conversion import RCFF
from File_Conversion import TimeSlice
import pickle
import sys
import traceback

class NeuralNetwork():
    def __init__(self):
        self.vector_size = 139
        self.num_hidden = 8

        self.series = tf.placeholder(tf.float32, [None, None, self.vector_size])

        cell = tf.nn.rnn_cell.LSTMCell(self.num_hidden, state_is_tuple=True)

        val, state = tf.nn.dynamic_rnn(cell, self.series, dtype=tf.float32) # val is num_sequences x series_length * num_hidden
        predict_hidden = val[:,:-1,:]
        target = self.series[0,1:,:] #only use first series
        weight = tf.Variable(tf.truncated_normal([self.num_hidden, self.vector_size]))
        bias = tf.Variable(tf.constant(0.1, shape=[self.vector_size]))
        self.predict = tf.matmul(predict_hidden[0,:,:], weight) + bias #only use first series
        self.predict_round = tf.where(tf.greater(self.predict, tf.ones_like(self.predict)*0.5), tf.ones_like(self.predict, dtype=tf.int32), tf.zeros_like(self.predict, dtype=tf.int32))

        loss = tf.reduce_mean(tf.square(target - self.predict))
        optimizer = tf.train.AdamOptimizer()
        self.minimize = optimizer.minimize(loss)

        init_op = tf.initialize_all_variables()

        self.saver = tf.train.Saver()

        self.sess = tf.Session()
        self.sess.run(init_op)

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
            try:
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
            except RuntimeException:
                with open('error.log', 'w') as logfile:
                    logfile.write(traceback.format_exc())

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
            ts = TimeSlice.TimeSlice(int(notes.index(max(notes[0:128]))), int(notes[128]), int(message_vec.index(max(message_vec))))
            
            retval.body.append(ts)
        with open(rcff_dest_path, 'wb') as rcff_dest_file:
            retval.pickle(rcff_dest_file)
        return retval   

    def validate_rcff(rcff):
        mode = 'ready' # ready, something, note, rest
        in_note = -1
        rcff_new = RCFF.RCFF('generated', 120, 0)
        for ts in rcff.body:
            if mode == 'ready':
                if ts.message == 0: # REST
                    rcff_new.body.append(TimeSlice.TimeSlice(0, 0, 9))
                    rcff_new.body.append(ts)
                    mode = 'rest'
                elif ts.message == 1: # BEAT
                    rcff_new.body.append(TimeSlice.TimeSlice(0, 0, 9))
                    rcff_new.body.append(ts)
                    mode = 'note'
                elif ts.message == 9: # BEGIN
                    rcff_new.body.append(ts)
                    mode = 'something'
                elif ts.message == 8: # END
                    pass
            elif mode == 'note':
                if ts.message == 0: # REST
                    pass
                elif ts.message == 1: # BEAT
                    rcff_new.body.append(ts)
                elif ts.message == 9: # BEGIN
                    rcff_new.body.append(TimeSlice.TimeSlice(0, 0, 8))
                    rcff_new.body.append(ts)
                    mode = 'something'
                elif ts.message == 8: # END
                    rcff_new.body.append(ts)
                    mode = 'ready'
            elif mode == 'rest':
                if ts.message == 0: # REST
                    rcff_new.body.append(ts)
                elif ts.message == 1: # BEAT
                    pass
                elif ts.message == 9: # BEGIN
                    rcff_new.body.append(TimeSlice.TimeSlice(0, 0, 8))
                    rcff_new.body.append(ts)
                    mode = 'something'
                elif ts.message == 8: # END
                    rcff_new.body.append(ts)
                    mode = 'ready'
            elif mode == 'something':
                if ts.message == 0: # REST
                    rcff_new.body.append(ts)
                    mode = 'rest'
                elif ts.message == 1: # BEAT
                    rcff_new.body.append(ts)
                    mode = 'note'
                elif ts.message == 9: # BEGIN
                    pass
                elif ts.message == 8: # END
                    rcff_new.body.append(ts)
                    mode = 'ready'
            with open('destfile.rcff', 'wb') as rcff_dest_file:
                rcff_new.pickle(rcff_dest_file)