# -*- coding: utf-8 -*-

#Práctica 1, Parte Opcional: PABLO FERNÁNDEZ DEL AMO  04231435X

from multiprocessing import Process, current_process
from multiprocessing import Semaphore
from multiprocessing import Manager
from time import sleep 
from random import randint, random


N = 10 # number of integers produced by each producer
NProducers = 5 # Number of producers

Buffer_size = 7 # size of the buffer of each producer, difference with part 1


def delay(factor = 3):
    sleep(random()/factor)


def producer(storage, empty, non_empty, prod_number):
    data = -1
    for iter in range(N): 
        data = randint(data + 1, data + 40) 
        print(f"Producer {current_process().name} has produced the number: {data}")
        empty[prod_number].acquire() # the producer acquires the lock to write to the buffer
        try:
            if storage[prod_number][0] == -2:
                storage[prod_number].pop()
            storage[prod_number].append(data)
            print(f"Producer {current_process().name} has stored the number: {data}")
            delay()
        finally:
            non_empty[prod_number].release() # the producer releases the semaphore to signal to the collector that there is data in the buffer
    
    empty[prod_number].acquire() # acquire the lock to write to the buffer
    try:    
        storage[prod_number].append(-1) # write -1 to indicate that the producer has finished
    finally:
        non_empty[prod_number].release() # release the semaphore to signal to the collector that there is data in the buffer
        print(f"The producer {current_process().name} has finished producing") # print message to indicate that the producer has finished producing


def minimum(storage):
    index = -1 # Initializes the index of the minimum value
    boolean = False # Boolean variable to check if there are elements in the storage
    for pos, val in enumerate(storage):
        if val[0] >= 0:
            if not boolean:
                boolean = True
                index = pos
            elif val[0] < storage[index][0]:
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
            data = storage[n[1]].pop(0)
            if not storage[n[1]]:
                storage[n[1]].append(-2)
            
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
    storage = manager.list()

    # Create a shared list to store merged products
    merged_products = manager.list()

    # Two lists of semaphores foe each task
    non_empty = [Semaphore(0) for _ in range(NProducers)]
    empty = [Semaphore(Buffer_size) for _ in range(NProducers)] # In this section, we change the Lock() and use the Semaphore with size NBuffer,
    processes = []                                                  # as it is going to dictaminate the size of the buffer (array) associated to producer i.
    
    # Create NProd producer processes and append them to processes list
    for prod_number in range(NProducers):
        storage.append(manager.list())
        storage[prod_number].append(-2)
        processes.append(Process(target=producer, name=f"Producer_{prod_number}",
                                  args=[storage, empty, non_empty, prod_number]))
        
    # Create a consumer process and append it to processes list
    processes.append(Process(target=merge, name="Collector",
                             args=[storage, empty, non_empty, merged_products]))
    
    print(f"Merged products before execution: {list(merged_products)}")
    print("Storage before execution: \n[", end = ' ')
    for i in storage:
        print(i[:], end =' ')
    print(']')

    # Start all processes
    for p in processes:
        p.start()
    # Wait for all processes to finish
    for p in processes:
        p.join()

    # Print the storage and merged products lists before and after execution
    print("Storage after execution: \n[", end = ' ')
    for i in storage:
        print(i[:], end =' ')
    print(']')
    

    # Print the merged products list after execution
    print(f"Merged products after execution: {list(merged_products)}")



if __name__ == '__main__':
    main()