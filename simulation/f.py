import numpy as np
import random
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def iterated_functions(x):
    addresses = {x: ''}
    current_address = ''
    for _ in range(1000):  
        while (x < 0.25 or random.choice([True, False])) and len(current_address) < 2000: 
            x = 1/3 * x + 2/3
            current_address += '2'
        else:
            x = 2/3 * x  
            current_address += '1'
        addresses[x] = current_address
    return addresses

find_x = 0.25

def find_k_closest(addresses, target, k):
    sorted_addresses = sorted(addresses.keys(), key=lambda x: abs(x-target))
    return [(addresses[x],x) for x in sorted_addresses[:k]]

all_addresses = {}

with ThreadPoolExecutor(max_workers=10) as executor:
    future_to_addresses = {executor.submit(iterated_functions, x=0.25): _ for _ in range(3000)}
    for future in tqdm(as_completed(future_to_addresses), total=len(future_to_addresses)):
        all_addresses.update(future.result())
        
k=10
k_closest = find_k_closest(all_addresses, find_x, k)
for y in k_closest:
    address = y[0]
    x = y[1]
    print(address[:6],x)