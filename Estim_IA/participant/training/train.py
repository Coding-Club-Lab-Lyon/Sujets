import numpy as np
from logger.logger import LogType, logger
from model.model import Model
from training.dataset import TrainingDataset


class AdamOptimizer:
    def __init__(self, learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        self.lr = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.t = 0
        self.m = {}
        self.v = {}

    def update(self, layer_id, weight, grad_weight, bias, grad_bias):
        self.t += 1

        if layer_id not in self.m:
            self.m[layer_id] = {
                "weight": np.zeros_like(weight),
                "bias": np.zeros_like(bias)
            }
            self.v[layer_id] = {
                "weight": np.zeros_like(weight),
                "bias": np.zeros_like(bias)
            }

        self.m[layer_id]["weight"] = self.beta1 * \
            self.m[layer_id]["weight"] + (1 - self.beta1) * grad_weight
        self.v[layer_id]["weight"] = self.beta2 * \
            self.v[layer_id]["weight"] + \
            (1 - self.beta2) * np.square(grad_weight)

        self.m[layer_id]["bias"] = self.beta1 * \
            self.m[layer_id]["bias"] + (1 - self.beta1) * grad_bias
        self.v[layer_id]["bias"] = self.beta2 * \
            self.v[layer_id]["bias"] + (1 - self.beta2) * np.square(grad_bias)

        m_weight_hat = self.m[layer_id]["weight"] / (1 - self.beta1 ** self.t)
        v_weight_hat = self.v[layer_id]["weight"] / (1 - self.beta2 ** self.t)

        m_bias_hat = self.m[layer_id]["bias"] / (1 - self.beta1 ** self.t)
        v_bias_hat = self.v[layer_id]["bias"] / (1 - self.beta2 ** self.t)

        weight -= self.lr * m_weight_hat / \
            (np.sqrt(v_weight_hat) + self.epsilon)
        bias -= self.lr * m_bias_hat / (np.sqrt(v_bias_hat) + self.epsilon)


class Trainer:
    def __init__(self, model: Model, dataset: list, learning_rate=0.001, batch_size=32):
        self.model = model
        self.dataset = TrainingDataset(dataset)
        self.optimizer = AdamOptimizer(learning_rate)
        self.batch_size = batch_size
        logger("Initialisation de l'entrainement avec un taux d'apprentissage = %f, taille du lot = %d et optimiseur = %s" % (
            learning_rate, batch_size, self.optimizer.__class__.__name__))

    def train(self, num_epochs):
        logger("Entrainement du modèle sur %d epochs" % num_epochs)
        for epoch in range(num_epochs):
            total_loss = 0
            for batch_x, batch_y in self.dataset.create_batches(self.batch_size):
                predictions = self.model.forward(batch_x)

                loss = self.loss(predictions, batch_y)
                total_loss += loss

                grad_output = self.loss_gradient(predictions, batch_y)
                self.model.backward(grad_output)

                for i, layer in enumerate(self.model.layers):
                    if layer.trainable:
                        self.optimizer.update(
                            i, layer.weight, layer.grad_weight, layer.bias, layer.grad_bias)

            logger("Epoch #%d: loss = %f" % (epoch + 1, total_loss /
                   len(self.dataset)), type=LogType.INDICATION)
        logger("Entrainement terminé !", type=LogType.SUCCESS)

    @staticmethod
    def loss(predictions, targets):
        return np.mean(np.square(predictions - targets))

    @staticmethod
    def loss_gradient(predictions, targets):
        return 2.0 * (predictions - targets) / len(predictions)
