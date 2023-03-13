# -*- coding: utf-8 -*-

#Práctica 1, Parte Obligatoria: PABLO FERNÁNDEZ DEL AMO  04231435x

from multiprocessing import Process, current_process
from multiprocessing import Semaphore, Lock
from multiprocessing import Manager
from time import sleep 
from random import randint, random

N = 8 # number of integers produced by each producer
NProducers = 3 # Number of producers

# Buffer_size = 1 , in this case our buffer is of length one, so using Lock() instead of Semaphore is good.


def delay(factor = 3):
    sleep(random()/factor)



def producer(storage, empty, non_empty, prod_number):
    data = -1
    for iter in range(N): 
        data = randint(data + 1, data + 40) 
        print(f"Producer {current_process().name} has produced the number: {data}")
        empty[prod_number].acquire() # the producer acquires the lock to write to the buffer
        try:
            storage[prod_number] = data
            print(f"Producer {current_process().name} has stored the number: {data}")
            delay()
        finally:
            non_empty[prod_number].release() # the producer releases the semaphore to signal to the collector that there is data in the buffer
    
    empty[prod_number].acquire() # acquire the lock to write to the buffer
    try:
        storage[prod_number] = -1 # write -1 to indicate that the producer has finished
    finally:
        non_empty[prod_number].release() # release the semaphore to signal to the collector that there is data in the buffer
        print(f"The producer {current_process().name} has finished producing") # print message to indicate that the producer has finished producing



def minimum(storage):
    index = -1 # Initializes the index of the minimum value
    boolean = False # Boolean variable to check if there are elements in the storage
    for pos, val in enumerate(storage):
        if val >= 0:
            if not boolean:
                boolean = True
                index = pos
            elif val < storage[index]:
                index = pos

    return (boolean, index) # Returns a tuple with a boolean indicating if there are non-negative values in the storage and the index of the smallest value.



def merge(storage, empty, non_empty, merged_products):
    # Wait for all producers to produce something
    for sem in non_empty:
        sem.acquire()
    
    # Iterate while there are still producers producing numbers
    while (n:=minimum(storage))[0]:
        # Print a message indicating that the collector is choosing a number to append
        print('Collector choosing a number from storage to append...')
        try: 
            # Get the data from the storage array and set it to -2
            data = storage[n[1]]
            storage[n[1]] = -2
            
            # Append the data to the merged products list and print a message indicating it was appended
            merged_products.append(data)
            print(f"Collector has picked up and appended the number: {data}.")
            delay()
            
        finally:
            # Release the empty lock for the chosen index
            empty[n[1]].release()
            
            # Acquire the non_empty semaphore for the chosen index
            non_empty[n[1]].acquire()



def main():
    # Use a Manager() to share information between processes
    manager = Manager()

    # Create shared array with NProd elements initialized to -2
    storage = manager.Array('i', [-2] * NProducers)

    # Create a shared list to store merged products
    merged_products = manager.list()

    # One list of semaphores and the other of Locks
    non_empty = [Semaphore(0) for _ in range(NProducers)] # marks if the storage for Prod_i is full
    empty = [Lock() for _ in range(NProducers)] # marks if the storage for Prod_i is empty
    processes = []

    # Create NProd producer processes and append them to processes list
    for prod_number in range(NProducers):
        processes.append(Process(target=producer, name=f"Prod_{prod_number}",
                                  args=[storage, empty, non_empty, prod_number]))
        
    # Create a consumer process and append it to processes list
    processes.append(Process(target=merge, name="Collector",
                             args=[storage, empty, non_empty, merged_products]))
    
    print(f"Merged products before execution: {list(merged_products)}")
    print(f"Storage before execution: {list(storage)}")

    # Start all processes
    for p in processes:
        p.start()
    # Wait for all processes to finish
    for p in processes:
        p.join()

    # Print the storage and merged products lists before and after execution
    print(f"Storage after execution: {list(storage)}")
    

    # Print the merged products list after execution
    print(f"Merged products after execution: {list(merged_products)}")



if __name__ == '__main__':
    main()