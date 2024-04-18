from model import Model
from training import Trainer, TrainingDataset
import csv


def create_dataset():
    dataset = []

    with open('real-estate-data.csv', 'r') as file:
        datas = csv.DictReader(file)

        # Remplir le dataset
    return dataset



dataset = create_dataset()
