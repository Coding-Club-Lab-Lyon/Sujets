import random

models = {
    "Renault": ["Clio", "Megane", "Scenic"],
    "Peugeot": ["208", "308", "508"],
    "Citroen": ["C3", "C4", "C5"],
    "Opel": ["Corsa", "Astra", "Insignia"],
    "Volkswagen": ["Polo", "Golf", "Passat"],
    "BMW": ["Serie 1", "Serie 3", "Serie 5"],
    "Toyota": ["Yaris", "Corolla", "Camry"],
    "Mercedes": ["Classe A", "Classe C", "Classe E"],
}

colors = ["Red", "Blue", "Green", "Yellow", "Black", "White", "Grey"]

def generate_cars(n):
    cars = []
    for i in range(n):
        brand = random.choice(list(models.keys()))
        model = random.choice(models[brand])
        color = random.choice(colors)
        cars.append("{} {} {}".format(color, brand, model))
    return cars

if __name__ == "__main__":
    print("\n".join(generate_cars(1024)))
