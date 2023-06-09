# -*- coding: utf-8 -*-

#Práctica 1, Parte Obligatoria: PABLO FERNÁNDEZ DEL AMO  04231435x

from multiprocessing import Process, current_process
from multiprocessing import Semaphore, Lock, Value
from multiprocessing import Manager
from time import sleep 
from random import randint, random

N = 8 # number of integers produced by each producer
NProducers = 3 # Number of producers

# Buffer_size = 1 , in this case our buffer is of length one, so using Lock() instead of Semaphore is good.


def delay(factor = 3):
    sleep(random()/factor)



def producer(personal_storage, personal_empty, personal_non_empty):
    data = 0
    for _ in range(N): 
        data = randint(data + 1, data + 40) 
        print(f"Producer {current_process().name} has produced the number: {data}")

       
        personal_storage.value = data
        print(f"Producer {current_process().name} has stored the number: {data}")
        personal_empty.release()
        personal_non_empty.acquire() # the producer acquires the lock to write to the buffer
        delay()

    try:
        personal_storage.value = -1 # write -1 to indicate that the producer has finished
    finally:
        personal_empty.release() # release the semaphore to signal to the collector that there is data in the buffer
        print(f"The producer {current_process().name} has finished producing") # print message to indicate that the producer has finished producing



def minimum(storage):
    index = -1 # Initializes the index of the minimum value
    finished = True # Boolean variable to check if there are elements in the storage
    for pos, val in enumerate(storage):
        if val.value >= 0:
            if finished:
                finished = False
                index = pos
            elif val.value < storage[index].value:
                index = pos

    return finished, index, storage[index].value # Returns a tuple with a boolean indicating if there are non-negative values in the storage and the index of the smallest value.



def merge(storage, empty, non_empty, merged_products):
    # Wait for all producers to produce something
    for sem in empty:
        sem.acquire()
    
    # Iterate while there are still producers producing numbers
    finished = False
    while not finished:
        finished, index, val = minimum(storage)
        # Print a message indicating that the collector is choosing a number to append
        print('Collector choosing a number from storage to append...')
        if not finished:
            try: 
                # Get the data from the storage array and set it to -2
                merged_products.append(val)
                print(f"Collector has picked up and appended the number: {val}.")
                print('Ordering...')
                delay()
                
            finally:

                non_empty[index].release()
                empty[index].acquire()
                
                
            



def main():
    # Use a Manager() to share information between processes
    manager = Manager()

    # Create shared array with NProd elements initialized to 0
    storage = [Value('i', 0) for i in range(NProducers)]

    # Create a shared list to store merged products
    merged_products = manager.list()

    # One list of semaphores and the other of Locks
    non_empty = [Semaphore(0) for _ in range(NProducers)] # marks if the storage for Prod_i is full
    empty = [Semaphore(0) for _ in range(NProducers)] # marks if the storage for Prod_i is empty
    processes = []

    # Create NProd producer processes and append them to processes list
    for prod_number in range(NProducers):
        processes.append(Process(target=producer, name=f"Prod_{prod_number}",
                                  args=[storage[prod_number], empty[prod_number], non_empty[prod_number]]))
        
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
