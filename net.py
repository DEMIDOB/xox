import numpy as np


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
        self.d_weights = np.dot(self.inputs.T, gradient).T
        self.d_biases = gradient.copy()

    def tweak(self, rate: float = 1):
        self.weights -= rate * self.d_weights
        self.biases -= rate * self.d_biases


if __name__ == '__main__':
    layer = DenseLayer(3, 1)
    layer.forward([0.9, 0.1, 0.043])
    print(layer.outputs)
    layer.backward()
    layer.tweak(rate=1/2)
    layer.forward([0.9, 0.1, 0.043])
    print(layer.outputs)
