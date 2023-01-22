import numpy as np


class NeuralNetwork():

    def __init__(self, layer_sizes):
        # TODO
        # layer_sizes example: [4, 10, 2]
        self.w = []
        self.b = []
        self.input_layer_size = layer_sizes[0]
        self.hidden_layer_size = layer_sizes[1]
        self.output_layer_size = layer_sizes[2]

        for i in range(len(layer_sizes) - 1):
            self.w.append(np.random.normal(size=(layer_sizes[i + 1], layer_sizes[i])))
            self.b.append(np.zeros((layer_sizes[i + 1], 1)))


    def activation(self, x):
        
        # TODO
        s = 1 / (1 + np.exp(-x))
        return s

    def forward(self, x):
        
        # TODO
        # x example: np.array([[0.1], [0.2], [0.3]])
        # initialization
        input_layer = x
        w2 = self.w[0]
        b2 = self.b[0]
        w3 = self.w[1]
        b3 = self.b[1]

        # hidden layer 
        a2 = self.activation((w2 @ input_layer + b2))
        hidden_layer_output = np.transpose(a2)[0].reshape(self.hidden_layer_size, 1)

        # output layer 
        a3 = self.activation(w3 @ hidden_layer_output + b3)
        output_layer_output = np.transpose(a3)[0].reshape(self.output_layer_size, 1)

        return output_layer_output
