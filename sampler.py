import json
import random
import csv

def generate_random_samples(json_file, num_samples=15, max_sample_size=10):
    with open(json_file, 'r') as file:
        json_data = json.load(file)

    samples = []

    for datatype, ops_funcs in json_data.items():
        for _ in range(num_samples):
            sample_size = random.randint(1, len(ops_funcs))
            sample_size = min(sample_size, max_sample_size)
            random_sample = random.sample(ops_funcs, sample_size)
            samples.append((datatype, random_sample))

    return samples

def write_to_csv(samples, output_file="random_samples.csv"):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['datatype', 'ops_funcs'])

        for sample in samples:
            writer.writerow([sample[0], sample[1]])



def sample():
    # Specify the path to your JSON file
    json_file_path = "types.json"

    # Generate random samples from the JSON file
    random_samples = generate_random_samples(json_file_path, num_samples=500, max_sample_size=10)

    # Write samples to CSV
    write_to_csv(random_samples)