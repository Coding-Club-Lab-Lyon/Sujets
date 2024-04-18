import csv
import faker
from concurrent.futures import ThreadPoolExecutor

fake = faker.Faker()

def compute_price(house):
    return house['bed'] * 7000 + house['bath'] * 12000 + house['house_size'] * 2000

def create_house():
    return {
        'agency': fake.company(),
        'date': fake.date_this_year(),
        'bed': fake.random_int(1, 5),
        'bath': fake.random_int(1, 5),
        'house_size': fake.random_int(50, 400),
        'adress':  fake.address().replace('\n', ' '),
        'owner': fake.name(),
        'phone_number': fake.phone_number(),
    }

def create_houses(batch_size):
    batch = []
    for _ in range(batch_size):
        house = create_house()
        price = compute_price(house)
        house['price'] = price
        batch.append(house)
    return batch

def create_dataset_multithreaded(total_houses, num_threads):
    houses_per_thread = total_houses // num_threads
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(create_houses, houses_per_thread) for _ in range(num_threads)]
        result = []
        for future in futures:
            result.extend(future.result())
    return result

# Parameters
total_houses = 100000
num_threads = 10  # Number of threads

# Generate dataset
dataset = create_dataset_multithreaded(total_houses, num_threads)

# Write dataset to CSV
with open('real-estate-data.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['agency', 'date', 'bed', 'bath', 'house_size', 'adress', 'owner', 'phone_number', 'price'])
    writer.writeheader()
    for house in dataset:
        writer.writerow(house)
