import time
import random

def benchmark_sorting():
    print("--- Sorting Algorithm Benchmark ---")
    sizes = [1000, 5000, 10000]
    
    for size in sizes:
        print(f"\nArray Size: {size}")
        arr = [random.randint(1, 1000) for _ in range(size)]
        
        # Test Python's built-in sort (as a baseline)
        arr_copy = arr.copy()
        start = time.time()
        arr_copy.sort()
        print(f"Built-in Sort: {time.time() - start:.4f} seconds")

        # Test Your Selection Sort (Warning: O(n^2) will be slow on 10k!)
        # You would import your core_algo sorting logic here to run purely (without Pygame yield statements)
        # Example: 
        # arr_copy = arr.copy()
        # start = time.time()
        # core_algo.pure_selection_sort(arr_copy) 
        # print(f"Selection Sort: {time.time() - start:.4f} seconds")

if __name__ == "__main__":
    benchmark_sorting()