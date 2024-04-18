import numpy as np
from model.layers import Layer, Linear
import pickle
from logger.logger import LogType, logger

class Model:
    def __init__(self):
        self.layers = []
        self.loss = None
        self.optimizer = None
        self.metrics = None

    def shape(self, layers: list):
        logger("Création du modèle suivant: %s" % layers)
        self.layers = []
        self.add(Linear(layers[0], layers[1]))
        for i in range(2, len(layers)):
            self.add(Linear(layers[i - 1], layers[i]))
        logger("Modèle créé: %s" % self.layers, type=LogType.SUCCESS)
    
    def save(self, file: str):
        try:
            logger("Sauvegarde du modèle vers: %s" % file)
            model = {
                "layers": self.layers,
                "loss": self.loss,
                "metrics": self.metrics
            }
            with open(file, "wb") as f:
                pickle.dump(model, f)
            logger("Model saved", type=LogType.SUCCESS)
        except Exception as e:
            raise RuntimeError("Error while saving model: %s" % e)
    
    def load(self, file: str):
        try:
            logger("Chargement du modèle depuis %s" % file)
            with open(file, "rb") as f:
                model = pickle.load(f)
                self.layers = model["layers"]
                self.loss = model["loss"]
                self.metrics = model["metrics"]
            logger("Modèle chargé: %s" % self.layers, type=LogType.SUCCESS)
        except Exception as e:
            raise RuntimeError("Fichier de modèle invalide: %s" % e)

    def add(self, layer: Layer):
        self.layers.append(layer)
    
    def forward(self, x: np.ndarray):
        for layer in self.layers:
            x = layer(x)
        return x
    
    def backward(self, grad_output: np.ndarray):
        for layer in reversed(self.layers):
            grad_output = layer.backward(grad_output)
        return grad_output
    
    def update(self, lr: float):
        for layer in self.layers:
            layer.update(lr)
