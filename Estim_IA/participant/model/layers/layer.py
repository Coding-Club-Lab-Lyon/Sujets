import numpy as np

class Layer:
    def __init__(self):
        self.trainable = False

    def forward(self, x: np.ndarray):
        raise NotImplementedError

    def backward(self, grad_output: np.ndarray):
        raise NotImplementedError

    def update(self, lr: float):
        pass

    def __call__(self, x: np.ndarray):
        return self.forward(x)

    def __repr__(self):
        return self.__class__.__name__