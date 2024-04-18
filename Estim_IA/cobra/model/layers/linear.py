from model.layers.layer import Layer
import numpy as np

class Linear(Layer):
    def __init__(self, in_features: int, out_features: int):
        self.in_features = in_features
        self.out_features = out_features
        self.weight = np.random.randn(out_features, in_features) / np.sqrt(in_features)
        self.bias = np.random.randn(out_features) / np.sqrt(in_features)
        self.grad_weight = np.zeros_like(self.weight)
        self.grad_bias = np.zeros_like(self.bias)
        self.trainable = True

    def forward(self, x: np.ndarray):
        self.x = x
        return np.matmul(x, self.weight.T) + self.bias

    def backward(self, grad_output: np.ndarray):
        self.grad_weight = np.dot(grad_output.T, self.x)
        self.grad_bias = np.sum(grad_output, axis=0)
        return np.dot(grad_output, self.weight)

    def update(self, lr: float):
        self.weight -= lr * self.grad_weight
        self.bias -= lr * self.grad_bias

    def __str__(self) -> str:
        return "Linear" + " (%d -> %d)" % (self.in_features, self.out_features)
    
    def __repr__(self) -> str:
        return self.__str__()