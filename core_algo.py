import random

def generate_random_array(size=20, min_val=10, max_val=200):
    return [random.randint(min_val, max_val) for _ in range(size)]

def bubble_sort_generator(arr):
    """Yields (array_state, [active_indices]) for Pygame to render."""
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            # Yield the elements being compared (for highlighting)
            yield arr, [j, j + 1]
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                # Yield the array after the swap
                yield arr, [j, j + 1] 
        if not swapped:
            break
    yield arr, [] # Finished

def selection_sort_generator(arr):
    """Yields state for Selection Sort."""
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            yield arr, [min_idx, j] # Highlight current min and checking element
            if arr[j] < arr[min_idx]:
                min_idx = j
                
        # Swap the found minimum element with the first element
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield arr, [i, min_idx] # Highlight the swap
    yield arr, [] # Finished

def merge_sort_wrapper(arr):
    """Wrapper function to match the signature of other sorting generators."""
    yield from _merge_sort_recursive(arr, 0, len(arr) - 1)
    yield arr, [] # Finished state

def _merge_sort_recursive(arr, left, right):
    if left < right:
        mid = (left + right) // 2
        
        # Recursively sort both halves, yielding animation frames up the stack
        yield from _merge_sort_recursive(arr, left, mid)
        yield from _merge_sort_recursive(arr, mid + 1, right)
        
        # Merge the sorted halves
        yield from _merge(arr, left, mid, right)

def _merge(arr, left, mid, right):
    temp = []
    i = left
    j = mid + 1

    # Compare and merge
    while i <= mid and j <= right:
        yield arr, [i, j] # Highlight the two elements being compared
        if arr[i] <= arr[j]:
            temp.append(arr[i])
            i += 1
        else:
            temp.append(arr[j])
            j += 1

    # Collect remaining elements
    while i <= mid:
        temp.append(arr[i])
        i += 1
    while j <= right:
        temp.append(arr[j])
        j += 1

    # Write the sorted temporary array back into the main array
    for p, val in enumerate(temp):
        arr[left + p] = val
        yield arr, [left + p] # Highlight the element being placed in its final sorted position