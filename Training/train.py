import theano
import theano.tensor as T
from theano_lstm import *
	
def train(test_data, num_iters):
	model = VectorTrainer()
	model.train(test_data, num_iters)
	return model

def sample(model, num_iters):
	return model.sample(num_iters)
	
class VectorTrainer:
	def __init__(self):
		self.model = StackedCells(4, layers=[4,4], activation=T.tanh, celltype=LSTM)
		self.model.layers[0].in_gate2.activation = lambda x: x
		self.model.layers.append(Layer(4, 2, lambda x: T.nnet.softmax(x)[0]))
		
	def step(self, x, *states):
		new_states = self.model.forward(x, prev_hiddens = states)
		return new_states

	def train(self, test_data, num_iters):
		
		initial_obs = T.vector()
		timesteps = T.iscalar()

		result, updates = theano.scan(self.step,
									  n_steps=timesteps,
									  outputs_info=[dict(initial=initial_obs, taps=[-1])] + [dict(initial=layer.initial_hidden_state, taps=[-1]) for layer in self.model.layers if hasattr(layer, 'initial_hidden_state')])

		target = T.vector()

		cost = (result[0][:,[0,2]] - target[[0,2]]).norm(L=2) / timesteps
		print 'got there'
		updates, gsums, xsums, lr, max_norm = create_optimization_updates(cost, self.model.params, method='adadelta')

		update_fun = theano.function([initial_obs, target, timesteps], cost, updates = updates, allow_input_downcast=True)
		predict_fun = theano.function([initial_obs, timesteps], result[0], allow_input_downcast=True)
		print 'got here'
		for i in range(num_iters):
			example = test_data[i]
			label = test_data[i+1]
			c = update_fun(example, label, num_iters)
		
		
	def sample(self, num_iters):
		
		return sample_data

if __name__ == "__main__":
	print 'ok' 
	train([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]*10, 10)
