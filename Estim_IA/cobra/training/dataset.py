import numpy as np


class TrainingDataset:
    def __is_valid(self, dataset: list):
        if not isinstance(dataset, list):
            return False
        if len(dataset) == 0:
            return False
        if not isinstance(dataset[0], tuple):
            return False
        if len(dataset[0]) != 2:
            return False
        ref_input_size = len(dataset[0][0])
        ref_output_size = len(dataset[0][1])
        for data in dataset:
            if not isinstance(data, tuple) or len(data) != 2:
                return False
            if len(data[0]) != ref_input_size or len(data[1]) != ref_output_size:
                return False
        return True


    def __init__(self, dataset: list):
        if not self.__is_valid(dataset):
            raise ValueError("Le jeu de données d'entraînement est invalide")
        self.dataset = dataset

    def create_batches(self, batch_size: int):
        if self.dataset is None:
            raise RuntimeError("Aucun jeu de données d'entraînement traité")
        np.random.shuffle(self.dataset)

        for i in range(0, len(self.dataset), batch_size):
            batch = self.dataset[i:i + batch_size]
            batch_x = np.array([x[0] for x in batch])
            batch_y = np.array([x[1] for x in batch])
            yield batch_x, batch_y

    def __len__(self):
        return len(self.dataset)

    # iterator
    def __iter__(self):
        return iter(self.dataset)
