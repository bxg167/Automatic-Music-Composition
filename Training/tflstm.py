import numpy as np
import tensorflow as tf

vector_size = 4
num_hidden = 64

series1 = [
 [[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]] * 50,
]

series2 = [
 [[0,0,0,1],[1,0,0,0],[0,1,0,0],[0,0,1,0]] * 50,
]

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


def train(train_series, num_iters):
	snapshot_num = 0
	for i in range(num_iters):
		for j in range(len(train_series)):
			this_train_series = train_series[j]
			sess.run(minimize,{series: [this_train_series]})
		if i % 100 == 0:	
			saver.save(sess, "snapshot_" + str(snapshot_num) + ".ckpt")
			snapshot_num += 1
	saver.save(sess, "snapshot_last.ckpt")
	return "snapshot_last.ckpt"

def sample(snapshot_path, num_iters):
	saver.restore(sess, snapshot_path)
	seed = [[0,0,0,1],[1,0,0,0]]
	for i in range(num_iters):
		result = predict_round.eval(session=sess, feed_dict={series: [seed + [[0,0,0,0]]]})
		result_last = result[-1,:]
		seed.append(list(result_last))
	print(str(seed))
	seed = [[0,0,0,1],[0,0,1,0]]
	for i in range(num_iters):
		result = predict_round.eval(session=sess, feed_dict={series: [seed + [[0,0,0,0]]]})
		result_last = result[-1,:]
		seed.append(list(result_last))
	print(str(seed))
	
if __name__ == '__main__':
	nums = [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768]
	for n in nums:
		print(n)
		train(series1, n)
		sample(7)
		print(n)
		train(series2, n)
		sample(7)
		print(n)