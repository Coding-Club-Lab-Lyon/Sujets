from model import Model
from training import Trainer, TrainingDataset
import csv


def create_dataset():
    dataset = []
    # read data from real-estate-data.csv
    # return a list of tuples for row.bed, row.bath, row.house_size
    with open('real-estate-data.csv', 'r') as file:
        datas = csv.DictReader(file)

        for row in datas:
                input_values = (
                    float(row['bed']),
                    float(row['bath']),
                    float(row['house_size']),
                )
                output_values = (float(row['price']),)

                dataset.append((input_values, output_values))
    return dataset



# Extraire les données interessantes du fichier csv
dataset = create_dataset()

# Créer un modèle avec une forme adéquate
mon_modele = Model()
mon_modele.shape([3, 16, 64, 16, 8, 1])

# Créer un entraineur avec le modèle et le jeu de données
trainer = Trainer(mon_modele, dataset)
trainer.train(10)

# Sauvegarder le modèle entrainé
mon_modele.save("mon_modele.model")
