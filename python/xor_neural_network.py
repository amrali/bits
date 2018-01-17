import time
import numpy as np
import numexpr as ne

from itertools import product

np.random.seed(1)

def activation(x, deriv=False):
    # SoftPlus (aprox. ReLU)
    if deriv:
        return ne.evaluate("1 / (1 + exp(-x))")

    return np.log(1 + np.exp(x))

def activation(x, deriv=False):
    # tanh
    if deriv:
        return ne.evaluate("1 - x**2")

    return ne.evaluate("(2 / (1 + exp(-2 * x))) - 1")

def activation(x, deriv=False):
    # Sigmoid (Logistic)
    if deriv:
        return ne.evaluate("x * (1 - x)")

    return ne.evaluate("1 / (1 + exp(-x))")

def activation(x, deriv=False):
    # Linear (powerful for regression)
    if deriv:
        return 1

    return x

def train(synapses, input_array, output_array, cycles=60000):
    for j in range(cycles):

        # calculate forward through the network
        layers = [input_array]
        num_synapses = 0
        for idx, synapse in enumerate(synapses):
            layers.append(activation(np.dot(layers[idx], synapse)))
            num_synapses += 1

        # back propagation of errors using the chain rule
        error_delta = prev_synapse = None
        for idx, synapse in enumerate(reversed(synapses)):
            idx = num_synapses - idx # reverse index
            if idx == num_synapses:
                #error = output_array - layers[-1:][0]
                _ = layers[-1:][0]
                error = ne.evaluate("output_array - _")
                if j % 10000 == 0:
                    print("Error:", str(np.mean(np.abs(error))))
            else:
                error = error_delta.dot(prev_synapse.T)

            error_delta = error * activation(layers[idx], deriv=True)
            synapse += layers[idx - 1].T.dot(error_delta)
            prev_synapse = synapse

def predict(synapses, input_array):
    layers = [input_array]
    for idx, synapse in enumerate(synapses):
        layers.append(activation(np.dot(layers[idx], synapse)))

    return layers[-1:][0]

def generate_synapses(num_of_synapses=2):
    num_of_nodes = 8
    random = lambda x: np.random.randint(-1, 256, size=x, dtype=np.int64)
    input_synapse = 2 * random((3, num_of_nodes)) - 1
    output_synapse = 2 * random((num_of_nodes, 1)) - 1

    synapses = [input_synapse]
    if num_of_synapses <= 2:
        synapses.append(output_synapse)
        return synapses

    for _ in range(num_of_synapses):
        synapses.append(2 * random((num_of_nodes, num_of_nodes)) - 1)
    synapses.append(output_synapse)

    return synapses

# input data
training_range_stop = 8
raw_training_set = product(range(training_range_stop), range(training_range_stop))
input_array = np.array(
        list(map(lambda x: list(x) + [1], raw_training_set)))
input_array = np.array([
    [0,0,1],
    [0,1,1],
    [1,0,1],
    [1,1,1]])

# training output data
output_training_array = np.array([
    [0],
    [1],
    [1],
    [0]])
output_training_array = (input_array[:,0] ^ input_array[:,1])
output_training_array = output_training_array.reshape(len(output_training_array), -1)
print(output_training_array)

# synapses
print("Generating randomized synapses...")
synapses = generate_synapses(9)

print("Training a neural network of {} synapses...".format(len(synapses)))
t1 = time.monotonic()
train(synapses, input_array, output_training_array)
t2 = time.monotonic()
print("Training took {} seconds".format(t2 - t1))

print("Test training input prediction result:")
t1 = time.monotonic()
result = predict(synapses, input_array)
t2 = time.monotonic()
print(result)
print("Prediction took {} microseconds".format((t2 - t1) * 1e6))
