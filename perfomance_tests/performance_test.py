import time
import requests
import matplotlib.pyplot as plt
import numpy as np
from faker import Faker
from tqdm import tqdm

# Configuration
BASE_URL = "http://localhost:5000"
SAMPLE_SIZES = [100, 500, 1000, 2000, 5000, 10000]  # Token counts to test
REPEATS_PER_SIZE = 3  # Number of tests per sample size

def generate_sample_text(token_count):
    """Generate sample text with approximate token count using lorem ipsum"""
    fake = Faker()
    text = []
    while len(' '.join(text).split()) < token_count:
        text.append(fake.sentence())
    return ' '.join(text)[:token_count*6]  # Average 6 characters per word

def send_request(text):
    """Send processing request and return response time"""
    start = time.perf_counter()
    response = requests.post(
        f"{BASE_URL}/api/process-text",
        json={
            "text": text,
            "format": "txt"
        }
    )
    if response.status_code != 200:
        raise RuntimeError(f"Request failed: {response.text}")
    return time.perf_counter() - start

def run_performance_test():
    results = {}
    
    for size in tqdm(SAMPLE_SIZES, desc="Testing sizes"):
        times = []
        for _ in range(REPEATS_PER_SIZE):
            text = generate_sample_text(size)
            elapsed = send_request(text)
            times.append(elapsed)
        results[size] = {
            'avg_time': np.mean(times),
            'std_dev': np.std(times)
        }
    
    return results

def plot_results(results):
    sizes = sorted(results.keys())
    avg_times = [results[size]['avg_time'] for size in sizes]
    std_devs = [results[size]['std_dev'] for size in sizes]

    plt.figure(figsize=(10, 6))
    plt.errorbar(sizes, avg_times, yerr=std_devs, fmt='-o', capsize=5)
    plt.title('Text Processing Performance')
    plt.xlabel('Number of Tokens')
    plt.ylabel('Processing Time (seconds)')
    plt.grid(True)
    plt.savefig('performance_plot.png')
    plt.show()

if __name__ == "__main__":
    test_results = run_performance_test()
    print("\nTest Results:")
    for size, data in test_results.items():
        print(f"{size} tokens: {data['avg_time']:.3f}s ± {data['std_dev']:.3f}")
    plot_results(test_results)