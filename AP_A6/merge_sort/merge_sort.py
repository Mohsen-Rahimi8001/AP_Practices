import concurrent.futures
import math
import multiprocessing
import random
import time

def merge(args:list[list]):
    """Merge two sorted lists"""
    assert len(args) == 2

    left, right = args
    result = [0] * (len(left) + len(right))
    i = j = k = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result[k] = left[i]
            i += 1
        else:
            result[k] = right[j]
            j += 1
        k += 1
    
    while i < len(left):
        result[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        result[k] = right[j]
        j += 1
        k += 1

    return result

def merge_sort(data):
    """basic merge sort function"""
    if len(data) > 1:
        mid = len(data) // 2
        left, right = merge_sort(data[:mid]), merge_sort(data[mid:])
        return merge((left, right))
    else:
        return data

def merge_chunks(results):
    """stick sorted chunks togheter"""

    # base case
    if len(results) == 1:
        return results[0]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        zipped_res = zip(results[::2], results[1::2]) # zipped result is in this shape zip_object((chunk1, chunk2), (chunk3, chunk4), ...)
        res = tuple(executor.map(merge, zipped_res)) # map the merge function to each pair of chunks
    
    # recursive step
    return merge_chunks(res)

def multiprocess_merge_sort(data):
    """Manages processes"""
    number_of_cores = 2 ** int(math.log2(multiprocessing.cpu_count())) # it should be a power of 2 --> in my computer it's 8
    
    # preform simple merge sort if the length of data is short
    if len(data) < 2 * number_of_cores:
        return merge_sort(data)

    len_of_subdata = len(data) // number_of_cores

    with concurrent.futures.ProcessPoolExecutor(max_workers=number_of_cores) as executor:
        chunks_of_data = []
        
        for i in range(number_of_cores-1):
            chunks_of_data.append(data[i* len_of_subdata : (i+1) * len_of_subdata])

        # if the length of data is not a multiple of number_of_cores, the last chunk will be different.
        chunks_of_data.append(data[(number_of_cores-1) * len_of_subdata :])

        start = time.perf_counter() 
        results = executor.map(merge_sort, chunks_of_data) # map the merge sort to each chunk
        print(f'Multiprocess sort done: {time.perf_counter() - start}') 

        return merge_chunks(tuple(results)) # merge the chunks and return
        

if __name__ == "__main__":
    # evaluation of the algorithm
    
    data = list(random.randint(1, 654321) for _ in range(745623))
    
    print('started ... ')

    start = time.perf_counter()
    res2 = multiprocess_merge_sort(data)
    print(f'Multiprocess merge sort spent {time.perf_counter() - start} seconds.')

    start = time.perf_counter()
    res1 = merge_sort(data)
    print(f'Simple merge sort spent {time.perf_counter() - start} seconds.')
    
    print(res1 == res2 == sorted(data))
