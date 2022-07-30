import numpy as np


class Softmax:
    def __init__(self):
        self.inputs = None
        self.outputs = None

    def forward(self, inputs, normalize_input=False):
        self.inputs = inputs.copy()

        if normalize_input:
            self.inputs -= np.max(self.inputs)

        self.outputs = np.exp(self.inputs) / np.sum(np.exp(self.inputs))
        return self.outputs


class ReLU:
    def __init__(self):
        self.inputs = None
        self.outputs = None

        self.d_inputs = None

    def forward(self, inputs):
        self.inputs = inputs.copy()
        self.outputs = np.maximum(0, self.inputs)
        return self.outputs

    def backward(self, gradient):
        self.d_inputs = (self.outputs > 0) * gradient


class DenseLayer:
    # NOTE: training in BATHES in NOT SUPPORTED

    def __init__(self, n_inputs, n_neurons):
        self.n_inputs = n_inputs
        self.n_neurons = n_neurons

        self.inputs = np.random.random((1, n_inputs))
        self.weights = np.random.random((n_neurons, n_inputs))
        self.biases = np.zeros(n_neurons)

        self.outputs = None

        self.d_inputs = None
        self.d_weights = None
        self.d_biases = None

    def forward(self, inputs):
        self.inputs = np.reshape(inputs, (1, self.n_inputs))
        self.outputs = np.dot(self.inputs, self.weights.T) + self.biases

    def backward(self, gradient=None):
        if gradient is None:
            gradient = np.ones(self.n_neurons)

        self.d_inputs = np.dot(gradient, self.weights)
        self.d_weights = np.dot(self.inputs.T, np.reshape(gradient, (1, self.n_neurons))).T
        self.d_biases = gradient.copy()

    def tweak(self, rate: float = 1):
        self.weights -= rate * self.d_weights
        self.biases -= rate * self.d_biases


if __name__ == '__main__':
    test_input = np.random.random(9)

    layer = DenseLayer(9, 9)
    layer.forward(test_input)
    print(layer.outputs)

    layer.backward()
    layer.tweak(rate=1/2)

    layer.forward(test_input)
    print(layer.outputs)

    act1 = Softmax()
    act2 = Softmax()

    act1.forward(layer.outputs)
    act2.forward(layer.outputs, normalize_input=True)

    print(act1.outputs)
    print(act2.outputs)
