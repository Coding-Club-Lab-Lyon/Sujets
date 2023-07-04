emission = [
    ("Renault", 15),
    ("Peugeot", 16),
    ("Citroen", 17),
    ("Opel", 16),
    ("Volkswagen", 18),
    ("BMW", 20),
    ("Toyota", 15),
    ("Mercedes", 19)
]

with open("embouteillage.txt") as file:
    content = file.readlines()

total_emission = 0

for line in content:
    for brand, emission_rate in emission:
        if brand in line:
            total_emission += emission_rate

print(total_emission)